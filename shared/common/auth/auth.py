import os
import uuid
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session
import logging

from shared.common.otp.email_sender import EmailOTPSender
from shared.common.otp.otp_manager import generate_otp as otp_generate_code
from shared.common.otp.otp_manager import validate_otp as otp_validate_code
from shared.database_base.database import get_db
from shared.database_base.models.user import User

otp_sender = EmailOTPSender()

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

class UserCreate(BaseModel):
    username: str
    email: str
    first_name: str | None = None
    last_name: str | None = None
    role: str = "user"

class UserResponse(BaseModel):
    username: str
    email: str
    first_name: str | None = None
    last_name: str | None = None
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: int | None = None
    username: str | None = None
    role: str | None = None

class OTPRequest(BaseModel):
    email: str

class OTPLoginRequest(BaseModel):
    email: str
    otp: str

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login-otp")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id") # Assuming user_id is in token payload
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if user_id is None or username is None or role is None:
            raise credentials_exception
        token_data = TokenData(user_id=int(user_id), username=username, role=role)
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.id == int(user_id)).first() # Use User.id
    if user is None:
        raise credentials_exception
    return user

async def require_super_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.role != "super_user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return current_user

@router.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    new_user = User(
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        roles=user.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    try:
        otp_code = otp_generate_code(db, new_user)
        otp_sender.send_otp(new_user.email, otp_code, new_user.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send OTP for verification: {e}",
        )

    return {"message": "User registered. An OTP has been sent to your email for verification."}

@router.post("/request-otp")
async def request_otp(otp_request: OTPRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == otp_request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="If a user with that email exists, an OTP has been sent.",
        )
    otp_code = otp_generate_code(db, user)
    try:
        sent_successfully = await otp_sender.send_otp(otp_request.email, otp_code, user.id)
        if not sent_successfully:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send OTP due to an internal issue.",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send OTP: {e}",
        )
    return {"message": "If a user with that email exists, an OTP has been sent."}

@router.post("/login-otp", response_model=Token)
async def login_with_otp(otp_login_request: OTPLoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == otp_login_request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if not otp_validate_code(db, user, otp_login_request.otp):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid OTP or email",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": str(user.id), "role": user.roles}, expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_refresh_token(
        data={"sub": user.username, "user_id": str(user.id), "role": user.roles}, expires_delta=refresh_token_expires
    )
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
