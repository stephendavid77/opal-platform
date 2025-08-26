# OpalSuite: A Unified Application Platform

## Overview

OpalSuite is a project designed to consolidate various independent Python productivity applications into a single, unified platform. This monorepo approach aims to streamline development, improve maintainability, and foster extensive code reuse across different tools and services. By centralizing core functionalities like authentication, secret management, and UI components, OpalSuite provides a cohesive and consistent user experience, reducing redundancy and accelerating future development.

## Current Applications

The following applications have been integrated into the OpalSuite monorepo:

*   **RegressionInsight** (formerly `release-regression-reporter`): A robust application for automating regression report generation.
*   **StandupBot**: A tool for managing standup reports, refactored to align with OpalSuite's modern architecture (FastAPI/React).
*   **BuildPilot**: An application for managing build processes.
*   **CalMind**: A calendar and mind management tool.
*   **MonitorIQ**: A system monitoring and intelligence application.
*   **XrayQC**: A quality control tool.

## Architecture

OpalSuite is built upon a monorepo structure, emphasizing shared components and centralized services to achieve consistency, efficiency, and scalability.

### Key Architectural Pillars:

*   **Monorepo Structure:** All projects are stored in a single repository to facilitate shared code, consistent tooling, and atomic commits. The `shared/` directory is the heart of the monorepo, containing all common and reusable components.
*   **Centralized Authentication:** A robust, Google Cloud-ready authentication service (`shared/common/auth/`) provides centralized user management and secure session handling using FastAPI, JWT, and refresh tokens. This service is now fully integrated into the main shared backend (`backend/main.py`).
*   **Centralized Frontend API Client:** A shared API client (`shared/frontend-base/src/api/apiClient.js`) for React applications that automatically handles JWT token injection for authenticated requests, ensuring consistent authorization across frontend tools.
*   **Centralized Secret Management:** A secure and abstracted secret management module (`shared/secrets_manager/`) retrieves secrets from various sources, including local `.env` files, environment variables, OS keychains, and Google Cloud Secret Manager.
*   **Common Database:** A single, shared database instance (`shared/database-base/`) is used across all applications, leveraging SQLAlchemy for ORM.
*   **Consistent User Interface:** A centralized design system (`shared/frontend-base/`) based on React and Bootstrap ensures a unified user experience.
*   **Landing Page:** A single entry point (`landing-page/`) for the entire platform, providing access to all applications and centralized authentication.

## Getting Started

1.  **Clone the Repository:**
    ```bash
    git clone <repository-url>
    cd OpalSuite
    ```

2.  **Install Root Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Initialize Shared Database:**
    ```bash
    python init_shared_db.py
    ```

4.  **Install Pre-Commit Hooks:**
    ```bash
    pre-commit install
    ```

5.  **Run the Architecture Check Script:**
    ```bash
    python scripts/check_architecture.py
    ```

6.  **Start the Services:**
    *   **Run the consolidated backend (standalone):**
        ```bash
        ./run_standalone.sh
        ```
    *   **Run all services (Docker):**
        ```bash
        ./run_webapp_docker.sh
        ```
    *   **Run a specific frontend service (e.g., landing-page) without Docker:**
        ```bash
        cd landing-page
        npm install # Install frontend dependencies, including shared frontend-base
        npm start
        ```
    *   **Run a specific service (e.g., landing-page) with Docker:**
        ```bash
        cd landing-page
        ./run_webapp_docker.sh
        ```

## Code Quality and Architectural Integrity

To maintain high code quality and a consistent architecture, OpalSuite uses a combination of tools and scripts:

*   **Formatting and Linting:** `black`, `isort`, and `flake8` are used to enforce code style and quality. These are managed through pre-commit hooks.
*   **Architectural Checks:** The `scripts/check_architecture.py` script enforces key architectural rules, such as preventing direct Redis imports, ensuring that new authentication or UI modules are not created outside of the designated shared directories, and validating shell scripts for direct `docker` or `gcloud` commands outside of designated common scripts.

For more detailed information, please refer to the `gemini.md` file.