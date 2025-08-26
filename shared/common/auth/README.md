# OpalSuite Centralized Authentication Service

## Overview

The `shared/common/auth/` module provides the core functionality for `OpalSuite`'s centralized authentication and session management. It is designed as a standalone, modular service that handles user registration, login, token issuance, and validation. Subprojects within OpalSuite rely on this service for all authentication-related tasks, ensuring consistency, security, and minimizing coupling.

## Architecture

### 1. API Endpoints (`auth.py`)

*   **FastAPI Router:** The `auth.py` file defines a FastAPI `APIRouter` that exposes all authentication-related API endpoints.
*   **Key Endpoints:**
    *   `/auth/register`: For new user registration.
    *   `/auth/token`: For username/password login, returning JWT access and refresh tokens.
    *   `/auth/request-otp`: Initiates email OTP verification.
    *   `/auth/verify-otp`: Verifies OTP and issues JWT tokens.
    *   `/auth/refresh-token`: Exchanges a refresh token for a new access token.
    *   `/auth/validate-token`: Verifies the validity of an access token.

### 2. Database Integration

*   **Models (`db/models.py`):** Defines SQLAlchemy ORM models for `User` and `RefreshToken` specific to the authentication service. These models interact with the common `OpalSuite` database.
*   **Database Connection (`db/database.py`):** Utilizes a dedicated database connection for the authentication service, pointing to the central `opal_suite.db` (or Cloud SQL in production).

### 3. Utility Functions (`utils/`)

*   **JWT Helpers (`jwt_helpers.py`):** Contains functions for creating, encoding, decoding, and validating JWT access and refresh tokens. It defines JWT configuration (secret key, algorithm, expiration times).
*   **OTP Generator (`otp_generator.py`):** Provides a simple function to generate random OTP codes.
*   **Email Sender (`email_sender.py`):** A placeholder module for sending emails (e.g., for OTP verification). It needs to be configured with actual SMTP details or integrated with transactional email services.
*   **Password Hasher (`password_hasher.py`):** Centralizes password hashing and verification using `passlib` (bcrypt/argon2).

### 4. Adapters (`adapters/`)

*   **OTP Adapter (`otp.py`):** Implements the logic for generating and sending OTPs, and verifying them. It includes temporary storage for OTPs (simulated with a dictionary for development, ideally Redis in production).
*   **SSO Adapter (`sso.py`):** A placeholder for future Single Sign-On (SSO) integrations (e.g., Google OAuth2, Microsoft OTP/TOTP).

## How it Fits into OpalSuite

*   **Centralized Authentication Authority:** This module is the single source of truth for user authentication and authorization within OpalSuite. All subprojects delegate authentication concerns to this service.
*   **Security:** By centralizing authentication, it ensures consistent security practices (password hashing, token management, rate-limiting) across the entire platform.
*   **Scalability:** Designed to be stateless (for access tokens) and deployable as a separate microservice (e.g., on Google Cloud Run), allowing it to scale independently.
*   **Extensibility:** Its modular design with adapters allows for easy integration of new authentication methods (SSO, MFA) without impacting subprojects.

## Getting Started (Development)

To run this authentication service locally:

1.  Ensure you have installed the root-level Python dependencies (`pip install -r requirements.txt` from the `OpalSuite` root).
2.  Navigate to `OpalSuite/auth_service/`.
3.  Install `auth_service` specific dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Initialize the `auth_service` database:
    ```bash
    python init_db.py
    ```
5.  **Configure Secrets:** Update `auth_service/utils/jwt_helpers.py` and `auth_service/utils/email_sender.py` with actual `SECRET_KEY`, SMTP details, etc. (ideally from environment variables or Secret Manager).
6.  Run the FastAPI application:
    ```bash
    uvicorn auth_service.main:app --host 0.0.0.0 --port 8001
    ```

## Future Enhancements

*   **Cloud Deployment:** Deploy to Google Cloud Run, utilizing Cloud SQL for persistent storage and Secret Manager for sensitive configurations.
*   **Rate Limiting:** Implement robust rate-limiting for login attempts and OTP requests.
*   **Token Revocation:** Enhance refresh token management and implement JWT blacklisting for immediate token revocation.
*   **Monitoring & Logging:** Integrate with Cloud Logging and Cloud Monitoring.
*   **SMS OTP:** Add support for SMS OTP via a pay-per-use service.
