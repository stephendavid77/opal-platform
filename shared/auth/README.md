# `auth` Module

## Purpose

The `auth` module provides the centralized authentication services for the entire OpalSuite platform. It handles user registration, login, and token management, ensuring a consistent and secure authentication experience across all integrated applications.

## Location

`shared/auth/`

## Key Components

*   **`auth.py`**: The main authentication logic, including FastAPI routes for user registration, OTP-based login, JWT token issuance and validation, and user retrieval.
*   **`otp/`**: This subdirectory contains the One-Time Password (OTP) related functionalities:
    *   `otp_manager.py`: Handles OTP generation and validation.
    *   `otp_sender.py`: Defines the abstract base class (interface) for OTP senders.
    *   `senders/email/email_sender.py`: Concrete implementation for sending OTPs via email.
    *   `senders/sms/sms_sender.py`: Concrete implementation for sending OTPs via SMS, utilizing an adapter pattern for different SMS providers (e.g., Twilio, Amazon SNS).
    *   `sms_adapters.py`: Contains provider-specific adapters (e.g., `TwilioAdapter`, `SNSAdapter`) that implement a common interface for sending SMS messages.
    *   `otp_sender_factory.py`: A factory function that returns the appropriate OTP sender instance (email or SMS) based on configuration.
*   **`tests/`**: Contains dedicated unit and integration tests for the authentication module, ensuring its functionality and adherence to architectural guidelines.

## Authentication Flow

The authentication process is primarily OTP-based:

1.  **Registration/Request OTP**: Users register or request an OTP by providing their email address.
2.  **OTP Generation & Sending**: An OTP is generated and sent to the user's email or phone number via the configured OTP sender (Email or SMS).
3.  **Login with OTP**: Users provide their email and the received OTP to log in.
4.  **Token Issuance**: Upon successful OTP validation, JWT access and refresh tokens are issued.
5.  **Token Validation**: Access tokens are used to authenticate requests to protected endpoints. Refresh tokens can be used to obtain new access tokens without re-authenticating.

## Configuration

All sensitive and configurable values within the `auth` module, such as API keys, secrets, and service endpoints, are retrieved exclusively from the `shared/secrets_manager` module. This ensures that no hardcoded properties are present in the codebase, enhancing security and flexibility across different environments.

Key configuration variables (retrieved via `secrets_manager`):

*   `SECRET_KEY`: Used for JWT signing.
*   `ALGORITHM`: JWT algorithm.
*   `ACCESS_TOKEN_EXPIRE_MINUTES`: Expiration time for access tokens.
*   `REFRESH_TOKEN_EXPIRE_DAYS`: Expiration time for refresh tokens.
*   `OTP_SENDER_TYPE`: Specifies the type of OTP sender to use (e.g., "email", "sms").
*   **For Email Sender:** `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USER`, `EMAIL_PASS`.
*   **For SMS Sender (Twilio):** `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`.
*   **For SMS Sender (Amazon SNS):** `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`.

## Extensibility

The `auth` module is designed with extensibility in mind, particularly for OTP sending mechanisms. New OTP providers (e.g., different SMS gateways, voice OTP) can be integrated by creating new adapter classes that adhere to the `OTPSender` interface and updating the `otp_sender_factory.py` to include the new provider.
