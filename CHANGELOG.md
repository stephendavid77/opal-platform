### Tue Aug 26 06:28:12 PDT 2025
- File edited: auth_service/api/auth_routes.py
- Change: Added datetime import to fix missing dependency.
### Tue Aug 26 06:28:24 PDT 2025
- File edited: auth_service/utils/email_sender.py
- Change: Updated placeholder SMTP settings with more realistic test values.
### Tue Aug 26 06:28:36 PDT 2025
- File edited: auth_service/adapters/otp.py
- Change: Updated placeholder OTP expiration and added a note to use a configuration file.
### Tue Aug 26 06:28:57 PDT 2025
- File edited: auth_service/requirements.txt
- Change: Added redis dependency for OTP store.
### Tue Aug 26 06:29:17 PDT 2025
- File edited: auth_service/adapters/otp.py
- Change: Replaced in-memory OTP store with Redis-based implementation.
### Tue Aug 26 06:33:49 PDT 2025
- File edited: auth_service/adapters/otp_store_interface.py
- Change: Created an abstract base class for the OTP store to improve modularity.
### Tue Aug 26 06:34:07 PDT 2025
- File edited: auth_service/adapters/redis_otp_store.py
- Change: Created a Redis-based implementation of the OTP store.
### Tue Aug 26 06:34:28 PDT 2025
- File edited: auth_service/adapters/otp.py
- Change: Refactored to use the OTP store interface and factory, making it modular.
### Tue Aug 26 06:35:53 PDT 2025
- File edited: scripts/check_architecture.py
- Change: Created a script to check for architectural violations, such as direct Redis imports.
### Tue Aug 26 06:38:20 PDT 2025
- File edited: scripts/check_architecture.py
- Change: Merged the new Redis import check with the existing architecture checks.
### Tue Aug 26 06:39:33 PDT 2025
- File edited: README.md
- Change: Updated and cleaned up the README.md file, adding a section on architectural integrity and improving the getting started guide.
