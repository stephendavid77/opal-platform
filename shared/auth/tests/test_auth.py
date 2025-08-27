import uuid
from datetime import timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from shared.auth.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_DAYS,
    SECRET_KEY,
    OTPLoginRequest,
    OTPRequest,
    UserCreate,
    create_access_token,
    create_refresh_token,
    router,
)

from shared.auth.otp.senders.email.email_sender import EmailOTPSender
from shared.auth.otp.otp_manager import generate_otp, validate_otp
from shared.auth.otp.otp_sender_factory import get_otp_sender
from shared.database_base.database import Base, get_db
from shared.database_base.models.user import User


# Mock the OTP sender to prevent actual email sending during tests
class MockOTPSender(EmailOTPSender):
    async def send_otp(self, recipient: str, otp_code: str, user_id: int) -> bool:
        print(f"Mock OTP sent to {recipient} for user {user_id}")
        return True


# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(name="session")
def session_fixture():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(name="client")
def client_fixture(session):
    def override_get_db():
        yield session

    from fastapi import FastAPI

    test_app = FastAPI()
    test_app.include_router(router)
    test_app.dependency_overrides[get_db] = override_get_db

    # Override the otp_sender in the auth module for testing
    test_app.dependency_overrides[get_otp_sender] = lambda: MockOTPSender()

    client = TestClient(test_app)
    yield client
    test_app.dependency_overrides.clear()


def test_register_user_and_request_otp(client, session):
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "roles": "user",
        },
    )
    assert response.status_code == 200
    assert (
        "User registered. An OTP has been sent to your email for verification."
        in response.json()["message"]
    )

    # Verify user exists in DB
    user = session.query(User).filter(User.email == "test@example.com").first()
    assert user is not None

    # Request OTP for the registered user
    response = client.post("/auth/request-otp", json={"email": "test@example.com"})
    assert response.status_code == 200
    assert (
        "If a user with that email exists, an OTP has been sent."
        in response.json()["message"]
    )


def test_login_with_otp(client, session):
    # Register user
    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "roles": "user",
        },
    )
    user = session.query(User).filter(User.email == "test@example.com").first()

    # Generate and validate OTP directly for testing purposes
    otp_code = generate_otp(session, user)

    # Login with OTP
    response = client.post(
        "/auth/login-otp", json={"email": "test@example.com", "otp": otp_code}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_with_invalid_otp(client, session):
    # Register user
    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "roles": "user",
        },
    )

    # Attempt login with invalid OTP
    response = client.post(
        "/auth/login-otp", json={"email": "test@example.com", "otp": "123456"}
    )
    assert response.status_code == 401
    assert "Invalid OTP or email" in response.json()["detail"]


def test_login_with_nonexistent_user(client):
    response = client.post(
        "/auth/login-otp", json={"email": "nonexistent@example.com", "otp": "123456"}
    )
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]


def test_read_users_me(client, session):
    # Register user and get OTP
    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "roles": "user",
        },
    )
    user = session.query(User).filter(User.email == "test@example.com").first()
    otp_code = generate_otp(session, user)

    # Login to get access token
    login_response = client.post(
        "/auth/login-otp", json={"email": "test@example.com", "otp": otp_code}
    )
    access_token = login_response.json()["access_token"]

    # Access protected endpoint
    response = client.get(
        "/auth/users/me/", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert data["roles"] == "user"


def test_read_users_me_unauthorized(client):
    response = client.get("/auth/users/me/")
    assert response.status_code == 401


def test_refresh_token(client, session):
    # Register user and get OTP
    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "roles": "user",
        },
    )
    user = session.query(User).filter(User.email == "test@example.com").first()
    otp_code = generate_otp(session, user)

    # Login to get refresh token
    login_response = client.post(
        "/auth/login-otp", json={"email": "test@example.com", "otp": otp_code}
    )
    refresh_token = login_response.json()["refresh_token"]

    # Refresh token
    response = client.post(
        "/auth/refresh-token", headers={"Authorization": f"Bearer {refresh_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_refresh_token_invalid(client):
    response = client.post(
        "/auth/refresh-token", headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response.status_code == 401


def test_super_user_access(client, session):
    # Register superuser and get OTP
    client.post(
        "/auth/register",
        json={
            "username": "superuser",
            "email": "super@example.com",
            "first_name": "Super",
            "last_name": "User",
            "roles": "super_user",
        },
    )
    user = session.query(User).filter(User.email == "super@example.com").first()
    otp_code = generate_otp(session, user)

    # Login to get access token
    login_response = client.post(
        "/auth/login-otp", json={"email": "super@example.com", "otp": otp_code}
    )
    access_token = login_response.json()["access_token"]

    # Access superuser-only endpoint
    response = client.get(
        "/auth/users/me/super-user-only/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "superuser"
    assert data["roles"] == "super_user"


def test_regular_user_super_user_access_denied(client, session):
    # Register regular user and get OTP
    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "roles": "user",
        },
    )
    user = session.query(User).filter(User.email == "test@example.com").first()
    otp_code = generate_otp(session, user)

    # Login to get access token
    login_response = client.post(
        "/auth/login-otp", json={"email": "test@example.com", "otp": otp_code}
    )
    access_token = login_response.json()["access_token"]

    # Attempt to access superuser-only endpoint
    response = client.get(
        "/auth/users/me/super-user-only/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 403
    assert "Not enough permissions" in response.json()["detail"]


def test_create_access_token_function():
    token = create_access_token(
        {"sub": "test", "user_id": str(uuid.uuid4()), "roles": "user"}
    )
    assert isinstance(token, str)


def test_create_refresh_token_function():
    token = create_refresh_token({"sub": "test", "user_id": str(uuid.uuid4())})
    assert isinstance(token, str)