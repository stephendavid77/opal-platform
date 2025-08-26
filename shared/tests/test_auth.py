import uuid  # Added import

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from shared.common.auth.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_DAYS,
    SECRET_KEY,
    create_access_token,
    create_refresh_token,
    pwd_context,
    router,
)
from shared.database_base.database import Base, get_db
from shared.database_base.models.user import User

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

    from fastapi import FastAPI  # Import FastAPI here

    test_app = FastAPI()
    test_app.include_router(router)  # Include the router in the test app
    test_app.dependency_overrides[
        get_db
    ] = override_get_db  # Set dependency_overrides on the app directly

    client = TestClient(test_app)
    print(f"Type of client: {type(client)}")  # Added print statement
    yield client
    test_app.dependency_overrides.clear()  # Clear dependency_overrides on the app


def test_create_user(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User",
            "role": "user",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_create_super_user(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "superuser",
            "email": "super@example.com",
            "password": "superpassword",
            "first_name": "Super",
            "last_name": "User",
            "role": "super_user",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_duplicate_username_registration(client):
    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User",
            "role": "user",
        },
    )
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "another@example.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User",
            "role": "user",
        },
    )
    assert response.status_code == 400
    assert "Username already registered" in response.json()["detail"]


def test_duplicate_email_registration(client):
    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User",
            "role": "user",
        },
    )
    response = client.post(
        "/auth/register",
        json={
            "username": "anotheruser",
            "email": "test@example.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User",
            "role": "user",
        },
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_login_for_access_token(client):
    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User",
            "role": "user",
        },
    )
    response = client.post(
        "/auth/token", data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_incorrect_password(client):
    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User",
            "role": "user",
        },
    )
    response = client.post(
        "/auth/token", data={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_login_nonexistent_user(client):
    response = client.post(
        "/auth/token", data={"username": "nonexistent", "password": "password"}
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_read_users_me(client):
    register_response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User",
            "role": "user",
        },
    )
    access_token = register_response.json()["access_token"]
    response = client.get(
        "/auth/users/me/", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert data["role"] == "user"


def test_read_users_me_unauthorized(client):
    response = client.get("/auth/users/me/")
    assert response.status_code == 401


def test_refresh_token(client):
    register_response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User",
            "role": "user",
        },
    )
    refresh_token = register_response.json()["refresh_token"]

    response = client.post(
        "/auth/refresh-token", headers={"Authorization": f"Bearer {refresh_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data  # Refresh token is returned again
    assert data["token_type"] == "bearer"


def test_refresh_token_invalid(client):
    response = client.post(
        "/auth/refresh-token", headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response.status_code == 401


def test_super_user_access(client):
    register_response = client.post(
        "/auth/register",
        json={
            "username": "superuser",
            "email": "super@example.com",
            "password": "superpassword",
            "first_name": "Super",
            "last_name": "User",
            "role": "super_user",
        },
    )
    access_token = register_response.json()["access_token"]
    response = client.get(
        "/auth/users/me/super-user-only/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "superuser"
    assert data["role"] == "super_user"


def test_regular_user_super_user_access_denied(client):
    register_response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User",
            "role": "user",
        },
    )
    access_token = register_response.json()["access_token"]
    response = client.get(
        "/auth/users/me/super-user-only/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 403
    assert "Not enough permissions" in response.json()["detail"]


def test_create_access_token_function():
    token = create_access_token(
        {"sub": "test", "user_id": str(uuid.uuid4()), "role": "user"}
    )
    assert isinstance(token, str)


def test_create_refresh_token_function():
    token = create_refresh_token({"sub": "test", "user_id": str(uuid.uuid4())})
    assert isinstance(token, str)
