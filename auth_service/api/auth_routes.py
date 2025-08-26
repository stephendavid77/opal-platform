from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from auth_service.adapters.otp import generate_and_send_otp
from auth_service.adapters.otp import verify_otp as verify_otp_code
from auth_service.db.database import get_db
from auth_service.db.models import RefreshToken, User
from auth_service.utils.jwt_helpers import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_DAYS,
    SECRET_KEY,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from auth_service.utils.password_hasher import hash_password, verify_password


class UserCreate(BaseModel):
    username: str
    password: str
    email: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str | None = None


class OTPRequest(BaseModel):
    email: str


class OTPVerification(BaseModel):
    email: str
    otp_code: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


router = APIRouter()


async def get_current_user(
    token: Annotated[str, Depends(OAuth2PasswordRequestForm(tokenUrl="/auth/token"))],
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


@router.post("/register", response_model=Token)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.username, "roles": new_user.roles},
        expires_delta=access_token_expires,
    )
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_refresh_token(
        data={"sub": new_user.username}, expires_delta=refresh_token_expires
    )

    db_refresh_token = RefreshToken(
        user_id=new_user.id,
        token=refresh_token,
        expires_at=datetime.utcnow() + refresh_token_expires,
    )
    db.add(db_refresh_token)
    db.commit()

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "roles": user.roles},
        expires_delta=access_token_expires,
    )
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_refresh_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires
    )

    db_refresh_token = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        expires_at=datetime.utcnow() + refresh_token_expires,
    )
    db.add(db_refresh_token)
    db.commit()

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }


@router.post("/request-otp")
async def request_otp(otp_request: OTPRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == otp_request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email not found",
        )

    otp_code = await generate_and_send_otp(otp_request.email)
    if otp_code:
        return {
            "message": "OTP sent to email.",
            "otp_code": otp_code,
        }  # otp_code for testing only, remove in prod
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send OTP",
        )


@router.post("/verify-otp", response_model=Token)
async def verify_otp(otp_verification: OTPVerification, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == otp_verification.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email not found",
        )

    if await verify_otp_code(otp_verification.email, otp_verification.otp_code):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "roles": user.roles},
            expires_delta=access_token_expires,
        )
        refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        refresh_token = create_refresh_token(
            data={"sub": user.username}, expires_delta=refresh_token_expires
        )

        db_refresh_token = RefreshToken(
            user_id=user.id,
            token=refresh_token,
            expires_at=datetime.utcnow() + refresh_token_expires,
        )
        db.add(db_refresh_token)
        db.commit()

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "refresh_token": refresh_token,
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired OTP"
        )


@router.post("/refresh-token", response_model=Token)
async def refresh_access_token(
    refresh_token_request: RefreshTokenRequest, db: Session = Depends(get_db)
):
    payload = decode_token(refresh_token_request.refresh_token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token payload",
        )

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    db_refresh_token = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token == refresh_token_request.refresh_token,
            RefreshToken.user_id == user.id,
        )
        .first()
    )
    if not db_refresh_token or db_refresh_token.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired or invalid",
        )

    # Optionally, revoke the old refresh token and issue a new one for security
    db.delete(db_refresh_token)
    db.commit()

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "roles": user.roles},
        expires_delta=access_token_expires,
    )
    new_refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    new_refresh_token = create_refresh_token(
        data={"sub": user.username}, expires_delta=new_refresh_token_expires
    )

    new_db_refresh_token = RefreshToken(
        user_id=user.id,
        token=new_refresh_token,
        expires_at=datetime.utcnow() + new_refresh_token_expires,
    )
    db.add(new_db_refresh_token)
    db.commit()

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": new_refresh_token,
    }


@router.get("/validate-token")
async def validate_token(current_user: Annotated[User, Depends(get_current_user)]):
    return {
        "message": "Token is valid",
        "username": current_user.username,
        "roles": current_user.roles,
    }
