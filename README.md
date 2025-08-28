# OpalSuite: A Unified Application Platform

## Overview

OpalSuite is a project designed to consolidate various independent Python productivity applications into a single, unified platform. The project has recently been refactored from a monorepo to a multi-repo architecture to enable independent development, versioning, and deployment of each application.

The core of the platform is the `opal-shared` repository, which contains all the shared code, including backend services, frontend components, and database models. Each application in the OpalSuite now consumes this shared code as a versioned dependency.

## Current Applications

The following applications are part of the OpalSuite platform:

*   **RegressionInsight**: A robust application for automating regression report generation.
*   **StandupBot**: A tool for managing standup reports.
*   **BuildPilot**: An application for managing build processes.
*   **CalMind**: A calendar and mind management tool.
*   **MonitorIQ**: A system monitoring and intelligence application.
*   **XrayQC**: A quality control tool.
*   **landing-page**: The main entry point for the entire platform.

## Architecture

OpalSuite is built upon a multi-repo architecture, with a central repository for shared components and separate repositories for each application.

### `opal-shared` Repository

The `opal-shared` repository is the heart of the OpalSuite platform. It contains all the common and reusable components, including:

*   **`opal_shared` Python Package:** A pip-installable package that provides:
    *   **Centralized Authentication:** A robust authentication service using FastAPI, JWT, and refresh tokens.
    *   **Centralized Secret Management:** A secure and abstracted secret management module.
    *   **Common Database Models:** Shared SQLAlchemy models for the common database.
*   **`@opal/shared-ui` NPM Package:** A design system and component library based on React and Bootstrap for a consistent user experience across all applications.

### Application Repositories

Each application resides in its own repository and consumes the `opal_shared` and `@opal/shared-ui` packages as versioned dependencies. This allows each application to be developed, tested, and deployed independently.

## Technology Stack

OpalSuite leverages a modern and robust technology stack to ensure high performance, scalability, and a consistent developer experience.

### Frontend

*   **React**
*   **Bootstrap**
*   **Custom CSS**

### Backend

*   **FastAPI**
*   **Python**

### Database

*   **SQLAlchemy**
*   **SQLite** (for local development)
*   **PostgreSQL** (for cloud deployment)

## Getting Started

1.  **Clone the Repositories:**
    ```bash
    # Clone the opal-shared repository
    git clone https://github.com/opalsuite/opal-shared.git

    # Clone the OpalSuite application repository
    git clone https://github.com/opalsuite/OpalSuite.git
    ```

2.  **Install `opal-shared` Dependencies:**
    ```bash
    # Install Python package in editable mode
    cd opal-shared
    pip install -e .

    # Install NPM package
    cd frontend-base
    npm install
    ```

3.  **Install Application Dependencies:**
    ```bash
    cd ../OpalSuite
    pip install -r requirements.txt
    ```

4.  **Initialize Shared Database:**
    ```bash
    python init_shared_db.py
    ```

5.  **Install Pre-Commit Hooks:**
    ```bash
    pre-commit install
    ```

6.  **Run the Services:**
    *   **Run the shared backend:**
        ```bash
        # In the opal-shared repository
        uvicorn opal_shared.backend.main:app --host 0.0.0.0 --port 8001
        ```
    *   **Run a specific frontend service (e.g., landing-page):**
        ```bash
        cd landing-page
        npm install
        npm start
        ```

## Code Quality and Architectural Integrity

To maintain high code quality and a consistent architecture, OpalSuite uses a combination of tools and scripts:

*   **Formatting and Linting:** `black`, `isort`, and `flake8` are used to enforce code style and quality. These are managed through pre-commit hooks.

For more detailed information, please refer to the `gemini.md` file.
