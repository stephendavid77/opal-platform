# OpalSuite: A Unified Application Platform

## Overview

OpalSuite is an ambitious project designed to consolidate various independent Python productivity applications into a single, unified platform. This monorepo approach aims to streamline development, improve maintainability, and foster extensive code reuse across different tools and services. By centralizing core functionalities like authentication, secret management, and UI components, OpalSuite provides a cohesive and consistent user experience, reducing redundancy and accelerating future development.

## Current Applications

The following applications have been integrated into the OpalSuite monorepo:

*   **RegressionInsight** (formerly `release-regression-reporter`): A robust application for automating regression report generation, now part of the unified suite.
*   **StandupBot**: A tool for managing standup reports, which has undergone significant refactoring to align with OpalSuite's modern architecture (FastAPI/React).
*   **BuildPilot**: An application for managing build processes.
*   **CalMind**: A calendar and mind management tool.
*   **MonitorIQ**: A system monitoring and intelligence application.
*   **XrayQC**: A quality control tool, likely for X-ray related processes.

## Proposed Architecture: Building a Cohesive Platform

OpalSuite is built upon a monorepo structure, emphasizing shared components and centralized services to achieve unparalleled consistency, efficiency, and scalability.

### 1. Monorepo Structure

At its core, OpalSuite is a monorepo, meaning all related projects are stored in a single repository. This facilitates shared code, consistent tooling, and atomic commits across different applications.

*   **Root Level:** Contains global configurations, shared service entry points, and individual application directories.
*   **`shared/` Directory:** This is the heart of the monorepo, housing all common and reusable components that can be inherited or utilized by any sub-application. It includes:
    *   `backend/`: The central FastAPI application for `OpalSuite`'s shared services (e.g., authentication, common APIs).
    *   `common/`: General utilities and shared Python code, including the centralized authentication service.
    *   `config-base/`: Centralized configuration templates and schemas.
    *   `database-base/`: Common database configurations, base ORM models, and migration scripts.
    *   `docs/`: Project-wide documentation.
    *   `frontend-base/`: Centralized UI components, a unified design system (Bootstrap-based), and shared frontend configurations.
    *   `scripts/`: Common build, deployment, and utility scripts.
    *   `tests/`: Centralized testing setup and utilities.
*   **Sub-Application Directories:** Each application (`RegressionInsight`, `StandupBot`, `BuildPilot`, etc.) resides in its own dedicated directory, containing its specific backend, frontend, and other components.

### 2. Centralized Authentication & Session Management

OpalSuite features a robust, Google Cloud-ready authentication service designed for centralized user management and secure session handling.

*   **Service Location:** Implemented as a dedicated service within `OpalSuite/shared/common/auth/`.
*   **Technology:** FastAPI for the API, JWT (JSON Web Tokens) for access tokens, refresh tokens for longer sessions, and `passlib` for secure password storage.
*   **Features:** Username/password login, email OTP verification, role-based authorization (roles in JWT claims), and token revocation.
*   **Stateless Design:** Primarily uses stateless JWTs for scalability and cost efficiency, with optional Redis/DB usage for refresh tokens/revocation.

### 3. Centralized Secret Management

To ensure secure and abstracted secret retrieval, OpalSuite employs a centralized secret management module.

*   **Module Location:** `OpalSuite/shared/secrets_manager/`.
*   **Retrieval Priority:** Secrets are retrieved based on a resilient priority chain: Local `.env` file → Environment variables → Local OS keychain → Google Cloud Secret Manager (in deployment).
*   **Abstraction:** Subprojects call simple helper methods (`get_secret`, `get_service_account_json`) without knowing the secret's source.
*   **Security:** Never logs secrets, handles network failures gracefully, and includes retry logic for cloud access.

### 4. Common Database

All applications within OpalSuite will leverage a single, shared database instance, eliminating data duplication and simplifying data management.

*   **Technology:** SQLAlchemy for robust ORM capabilities.
*   **Central Configuration:** Defined in `OpalSuite/shared/database-base/database.py`.
*   **Shared Models:** Common database models (e.g., `User` for authentication) are defined centrally in `OpalSuite/shared/database-base/models/`.

### 5. Consistent User Interface

OpalSuite prioritizes a unified user experience through a centralized design system.

*   **Location:** `OpalSuite/shared/frontend-base/`.
*   **Technology:** React and Bootstrap, providing a modern and responsive UI framework.
*   **Reusable Components:** This module will export reusable UI components and consistent styling, ensuring a cohesive look and feel across all applications.

### 6. Landing Page

*   **Location:** `OpalSuite/landing-page/`.
*   **Purpose:** Serves as the primary entry point for the entire OpalSuite platform, listing all available applications and providing a gateway for centralized authentication.

### 7. Centralized Routing and Deployment

*   **Central Web Server:** A web server (e.g., Nginx, Traefik) will act as a reverse proxy at the `OpalSuite` root, routing traffic to the landing page and individual sub-applications based on URL paths.
*   **Containerization (Recommended):** Docker and Docker Compose will be used to containerize all services (shared backend, landing page, and each sub-application's backend/frontend) for simplified development, testing, and deployment on platforms like Google Cloud Run.

## Getting Started (High-Level)

To begin working with OpalSuite, follow these high-level steps:

1.  **Clone the Repository:** Obtain the OpalSuite monorepo.
2.  **Install Root Dependencies:** Navigate to the `OpalSuite` root directory and install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Initialize Shared Database:** Set up the common database tables for shared services:
    ```bash
    python init_shared_db.py
    ```
4.  **Install Pre-Commit Hooks:** Ensure code quality checks run automatically before each commit:
    ```bash
    pre-commit install
    ```
5.  **Start Shared Backend:** Launch the main FastAPI application for shared services (e.g., authentication, secrets):
    ```bash
    uvicorn OpalSuite.backend.main:app --host 0.0.0.0 --port 8000
    ```
6.  **Develop/Run Landing Page:** Navigate to `landing-page/`, install Node.js dependencies (`npm install`), and start the development server (`npm start`).
7.  **Develop/Run Sub-Applications:** Each sub-application will have its own setup for running its backend and frontend, which will eventually integrate with the shared components.

## Code Quality and Consistency

To maintain high code quality and consistency across the monorepo, the following tools have been integrated and configured via `pyproject.toml` and `.pre-commit-config.yaml`:

*   **Black**: An uncompromising Python code formatter.
*   **isort**: A Python utility to sort imports alphabetically and automatically separate them into sections.
*   **Flake8**: A tool for enforcing style guide (PEP8) and checking for common programming errors.
*   **pre-commit**: Used to manage and maintain pre-commit git hooks, ensuring that code is formatted and linted before every commit.

For detailed instructions on each module and further development, refer to the `gemini.md` file.
