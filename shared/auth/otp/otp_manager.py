import random
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from shared.database_base.models.user import User


def generate_otp_code():
    """Generates a random 6-digit OTP code."""
    return str(random.randint(100000, 999999))


def generate_otp(db: Session, user: User, expiry_minutes: int = 5):
    """Generates an OTP for a user and stores it in the database."""
    otp_code = generate_otp_code()
    otp_expiry = datetime.utcnow() + timedelta(minutes=expiry_minutes)

    user.otp_code = otp_code
    user.otp_expiry = otp_expiry
    db.add(user)
    db.commit()
    db.refresh(user)
    return otp_code


def validate_otp(db: Session, user: User, otp_code: str):
    """Validates an OTP for a user."""
    if not user.otp_code or not user.otp_expiry:
        return False

    if user.otp_code == otp_code and datetime.utcnow() < user.otp_expiry:
        # Clear OTP after successful validation
        user.otp_code = None
        user.otp_expiry = None
        db.add(user)
        db.commit()
        db.refresh(user)
        return True
    return False
