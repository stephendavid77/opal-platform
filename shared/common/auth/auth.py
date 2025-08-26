import os
import uuid  # Moved import to top
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from shared.database_base.database import get_db
from shared.database_base.models.user import User, pwd_context
from shared.common.otp.otp_manager import generate_otp as otp_generate_code, validate_otp as otp_validate_code
from shared.common.otp.email_sender import EmailOTPSender

otp_sender = EmailOTPSender() # Instantiate the OTP sender

# --- JWT Configuration ---
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
)
REFRESH_TOKEN_EXPIRE_DAYS = int(
    os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7")
)
# -----------------------------------------------------------------


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    first_name: str | None = None
    last_name: str | None = None
    role: str = "user"


class UserResponse(BaseModel):  # New model for responses
    username: str
    email: str
    first_name: str | None = None
    last_name: str | None = None
    role: str

    class Config:
        from_attributes = True  # For Pydantic v2, use from_attributes = True instead of orm_mode = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: uuid.UUID | None = None
    username: str | None = None
    role: str | None = None


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, SECRET_KEY, algorithm=ALGORITHM
    )
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
        user_id: str = payload.get("user_id")
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if user_id is None or username is None or role is None:
            raise credentials_exception
        token_data = TokenData(user_id=uuid.UUID(user_id), username=username, role=role)
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.user_id == str(token_data.user_id)).first()
    if user is None:
        raise credentials_exception
    return user


async def require_super_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.role != "super_user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return current_user


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token)
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
        user_id=str(uuid.uuid4()),  # Convert UUID to string
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
    )
    new_user.set_password(user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "user_id": str(new_user.user_id),
            "sub": new_user.username,
            "role": new_user.role,
        },
        expires_delta=access_token_expires,
    )
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_refresh_token(
        data={"user_id": str(new_user.user_id), "sub": new_user.username},
        expires_delta=refresh_token_expires,
    )
    new_user.refresh_token = pwd_context.hash(refresh_token)
    db.commit()
    db.refresh(new_user)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not user.check_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": str(user.user_id), "sub": user.username, "role": user.role},
        expires_delta=access_token_expires,
    )
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_refresh_token(
        data={"user_id": str(user.user_id), "sub": user.username},
        expires_delta=refresh_token_expires,
    )
    user.refresh_token = pwd_context.hash(refresh_token)
    db.commit()
    db.refresh(user)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh-token", response_model=Token)
async def refresh_access_token(
    refresh_token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        username: str = payload.get("sub")
        if user_id is None or username is None:
            raise credentials_exception
        token_data = TokenData(user_id=uuid.UUID(user_id), username=username)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.user_id == str(token_data.user_id)).first()
    if (
        user is None
        or not user.refresh_token
        or not pwd_context.verify(refresh_token, user.refresh_token)
    ):
        raise credentials_exception

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": str(user.user_id), "sub": user.username, "role": user.role},
        expires_delta=access_token_expires,
    )
    # Optionally, issue a new refresh token as well, and update in DB
    # For simplicity, we are just issuing a new access token here.
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get(
    "/users/me/", response_model=UserResponse
)  # Changed response model to UserResponse
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.get(
    "/users/me/super-user-only/", response_model=UserResponse
)  # Added super user only endpoint
async def read_users_me_super_user_only(
    current_user: Annotated[User, Depends(require_super_user)]
):
    return current_user
