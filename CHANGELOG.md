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
### Tue Aug 26 06:49:09 PDT 2025
- File edited: landing-page/src/App.js
- Change: Implemented a login form and connected it to the authentication service.
### Tue Aug 26 06:52:33 PDT 2025
- File edited: auth_service/run_standalone.sh, auth_service/run_docker.sh, auth_service/deploy_gcloud.sh
- Change: Created shell scripts for standalone, docker, and gcloud deployment for the auth_service.
### Tue Aug 26 06:53:22 PDT 2025
- File edited: landing-page/run_standalone.sh, landing-page/run_docker.sh, landing-page/deploy_gcloud.sh, landing-page/Dockerfile
- Change: Created shell scripts for standalone, docker, and gcloud deployment for the landing-page.
### Tue Aug 26 06:54:16 PDT 2025
- File edited: BuildPilot/run_standalone.sh, BuildPilot/run_docker.sh, BuildPilot/deploy_gcloud.sh
- Change: Created shell scripts for standalone, docker, and gcloud deployment for the BuildPilot project.
### Tue Aug 26 06:55:22 PDT 2025
- File edited: CalMind/run_standalone.sh, CalMind/run_docker.sh, CalMind/deploy_gcloud.sh, CalMind/Dockerfile
- Change: Created shell scripts for standalone, docker, and gcloud deployment for the CalMind project.
### Tue Aug 26 06:56:40 PDT 2025
- File edited: MonitorIQ/run_standalone.sh, MonitorIQ/run_docker.sh, MonitorIQ/deploy_gcloud.sh, MonitorIQ/Dockerfile
- Change: Created shell scripts for standalone, docker, and gcloud deployment for the MonitorIQ project.
### Tue Aug 26 06:57:48 PDT 2025
- File edited: RegressionInsight/run_standalone.sh, RegressionInsight/docker/run-docker.sh, RegressionInsight/deploy_gcloud.sh
- Change: Created shell scripts for standalone, docker, and gcloud deployment for the RegressionInsight project.
### Tue Aug 26 06:58:50 PDT 2025
- File edited: StandupBot/run_standalone.sh, StandupBot/run_docker.sh, StandupBot/deploy_gcloud.sh
- Change: Created shell scripts for standalone, docker, and gcloud deployment for the StandupBot project.
### Tue Aug 26 07:00:01 PDT 2025
- File edited: XrayQC/run_standalone.sh, XrayQC/run_docker.sh, XrayQC/deploy_gcloud.sh, XrayQC/Dockerfile
- Change: Created shell scripts for standalone, docker, and gcloud deployment for the XrayQC project.
### Tue Aug 26 07:01:05 PDT 2025
- File edited: run_standalone.sh, run_docker.sh, deploy_gcloud.sh
- Change: Created shell scripts for standalone, docker, and gcloud deployment for the root OpalSuite project.
### Tue Aug 26 07:15:44 PDT 2025
- File edited: 
- Change: Refactored all run scripts to be more modular and use common scripts from shared/scripts.
### Tue Aug 26 07:27:21 PDT 2025
- File edited: scripts/check_architecture.py
- Change: Added validation rules for .sh files to prevent architecture violations.
### Tue Aug 26 07:28:15 PDT 2025
- File edited: gemini.md
- Change: Added context about script modularity and architectural validation to gemini.md.
### Tue Aug 26 07:29:08 PDT 2025
- File edited: README.md
- Change: Updated README.md to reflect new script modularity and shell script validation rules.
### Tue Aug 26 07:53:14 PDT 2025
- File edited: auth_service/requirements.txt
- Change: Corrected typos in package names in requirements.txt.
### Tue Aug 26 07:56:04 PDT 2025
- File edited: auth_service/api/auth_routes.py
- Change: Corrected OAuth2PasswordRequestForm usage in get_current_user dependency.
### Tue Aug 26 08:13:49 PDT 2025
- File edited: landing-page/src/App.js
- Change: Corrected syntax error in App.js (apostrophe in string).
