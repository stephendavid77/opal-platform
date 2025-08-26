# OpalSuite Auth Service (Centralized Authentication Module)

## Overview

The `auth_service/` module is a dedicated, centralized authentication and session management service for the `OpalSuite` platform. It is designed to be fully deployable on Google Cloud, providing a robust, modular, and cost-efficient solution for user authentication, session management, and authorization. Subprojects within OpalSuite rely on this service for all login and session-related functionalities, minimizing coupling and ensuring consistent security practices.

## Architecture

### 1. Core Application (`main.py`)

*   **FastAPI Entry Point:** `main.py` initializes the FastAPI application for the authentication service and includes the `auth_routes.router`.
*   **Health Check:** Provides a basic `/health` endpoint for readiness and liveness probes.

### 2. API Endpoints (`api/auth_routes.py`)

*   **FastAPI Router:** Defines all authentication-related API endpoints.
*   **Key Endpoints:**
    *   `/register`: User registration with username, password, and optional email.
    *   `/token`: Username/password login, returning JWT access and refresh tokens.
    *   `/request-otp`: Initiates email OTP verification for a given email.
    *   `/verify-otp`: Verifies OTP code and issues JWT tokens upon success.
    *   `/refresh-token`: Exchanges a refresh token for a new access token.
    *   `/validate-token`: Verifies the validity of an access token and returns user details.

### 3. Database Integration (`db/`)

*   **`database.py`:** Configures the SQLAlchemy engine and session for the authentication service's database. It's designed to connect to Cloud SQL in production and a local SQLite file for development.
*   **`models.py`:** Defines SQLAlchemy ORM models for:
    *   `User`: Stores user details including username, email, hashed password, and roles.
    *   `RefreshToken`: Stores refresh tokens for longer session management.
*   **`migrations/`:** Placeholder for Alembic migration scripts to manage database schema changes.

### 4. Utility Functions (`utils/`)

*   **`jwt_helpers.py`:** Handles JWT creation, encoding, decoding, and validation. Defines JWT configuration (secret key, algorithm, expiration times for access and refresh tokens).
*   **`otp_generator.py`:** Generates random numeric OTP codes.
*   **`email_sender.py`:** A placeholder for email sending functionality (e.g., for OTP delivery). Requires configuration for SMTP or transactional email services.
*   **`password_hasher.py`:** Centralizes password hashing and verification using `passlib` (bcrypt/argon2).

### 5. Adapters (`adapters/`)

*   **`otp.py`:** Implements the core logic for OTP generation, temporary storage (simulated with a dictionary for development, ideally Redis in production), sending via email, and verification.
*   **`sso.py`:** A placeholder for future Single Sign-On (SSO) integrations (e.g., OAuth2 / OpenID Connect, Microsoft OTP / TOTP, Hardware MFA tokens).

### 6. Dockerization (`docker/`)

*   **`Dockerfile`:** Defines the steps to containerize the authentication service, making it deployable on platforms like Google Cloud Run.
*   **`cloud-run-config.yaml`:** A placeholder for Google Cloud Run deployment configuration, including image, ports, and environment variable management via Secret Manager.

## How it Fits into OpalSuite

*   **Centralized Authority:** Acts as the single source of truth for user authentication and authorization across all `OpalSuite` applications.
*   **Reduced Coupling:** Subprojects interact with this service via well-defined API endpoints, abstracting away the complexities of user management and session handling.
*   **Security:** Enforces consistent security practices (secure password storage, JWTs, rate-limiting) platform-wide.
*   **Scalability & Cost-Efficiency:** Leverages stateless JWTs for access tokens, minimizing database lookups and enabling horizontal scaling on serverless platforms like Cloud Run.
*   **Extensibility:** Modular design allows for easy integration of new authentication methods (SSO, MFA) without impacting consuming applications.

## Getting Started (Development)

1.  **Install `auth_service` dependencies:**
    *   Navigate to `OpalSuite/auth_service/`.
    *   Install Python dependencies:
        ```bash
        pip install -r requirements.txt
        ```
2.  **Initialize `auth_service` database:**
    *   From `OpalSuite/auth_service/`:
        ```bash
        python init_db.py
        ```
3.  **Configure Secrets:**
    *   Update `auth_service/utils/jwt_helpers.py` (e.g., `SECRET_KEY`) and `auth_service/utils/email_sender.py` (SMTP details) with actual values. Ideally, these should be managed via environment variables or Google Cloud Secret Manager.
4.  **Run `auth_service`:**
    *   From `OpalSuite/auth_service/`:
        ```bash
        uvicorn main:app --host 0.0.0.0 --port 8001
        ```
    *   The service will be accessible at `http://localhost:8001` (or your chosen port).

## Future Enhancements

*   **Cloud Deployment:** Deploy to Google Cloud Run, utilizing Cloud SQL for persistent storage and Secret Manager for sensitive configurations.
*   **Rate Limiting:** Implement robust rate-limiting for login attempts and OTP requests.
*   **Token Revocation:** Enhance refresh token management and implement JWT blacklisting for immediate token revocation.
*   **Monitoring & Logging:** Integrate with Cloud Logging and Cloud Monitoring.
*   **SMS OTP:** Add support for SMS OTP via a pay-per-use service.
*   **SSO Integration:** Implement adapters for various SSO providers (Google, Microsoft, etc.).
