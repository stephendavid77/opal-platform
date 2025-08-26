import uuid

from passlib.context import CryptContext
from sqlalchemy import Column, Enum, String, DateTime
from sqlalchemy.dialects.postgresql import (  # Although using SQLite, keep for future compatibility
    UUID,
)

from shared.database_base.database import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    user_id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    username = Column(String(80), unique=True, nullable=False, index=True)
    hashed_password = Column(String(256), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)  # Added email
    first_name = Column(String(80), nullable=True)
    last_name = Column(String(80), nullable=True)
    role = Column(
        Enum("user", "super_user", name="user_role"), default="user", nullable=False
    )
    refresh_token = Column(String(256), nullable=True)  # Store hashed refresh token
    otp_code = Column(String(6), nullable=True)
    otp_expiry = Column(DateTime, nullable=True)

    def set_password(self, password):
        self.hashed_password = pwd_context.hash(password)

    def check_password(self, password):
        return pwd_context.verify(password, self.hashed_password)

    def __repr__(self):
        return f"<User {self.username}>"
