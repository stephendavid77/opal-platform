# OpalSuite Project Documentation

## 1. Project Overview

**OpalSuite** is a unified platform designed to consolidate various independent Python productivity applications under a single monorepo umbrella. This strategic approach aims to:

*   **Foster Code Reuse:** Centralize common functionalities and components.
*   **Ensure Consistent User Experience:** Provide a cohesive look, feel, and interaction across all applications.
*   **Streamline Development and Maintenance:** Simplify dependency management, build processes, and updates.

By centralizing core functionalities like authentication, secret management, and UI components, OpalSuite reduces redundancy and accelerates future development of new tools and services.

## 2. Key Architectural Pillars

OpalSuite is built upon a robust monorepo structure, emphasizing shared components and centralized services to achieve consistency, efficiency, and scalability.

*   **Monorepo Structure:** All projects reside in a single repository, facilitating shared code, consistent tooling, and atomic commits. The `shared/` directory is the core, housing all common and reusable components.
*   **Centralized Authentication:** A robust authentication service (`shared/auth/`) provides centralized user management and secure session handling using FastAPI, JWT, and refresh tokens. It supports OTP-based authentication and is designed for future extensibility.
*   **Centralized Secret Management:** A secure and abstracted secret management module (`shared/secrets_manager/`) retrieves sensitive information from various sources (local `.env` files, environment variables, OS keychains, and Google Cloud Secret Manager).
*   **Common Database:** A single, shared database instance (`shared/database_base/`) is used across all applications, leveraging SQLAlchemy for ORM.
*   **Consistent User Interface:** A centralized design system (`shared/frontend-base/`) based on React and Bootstrap ensures a unified user experience across all frontend applications.
*   **Centralized Frontend API Client:** A shared API client (`shared/frontend-base/src/api/apiClient.js`) for React applications automatically injects JWT tokens for authenticated requests, ensuring consistent authorization.
*   **Landing Page:** A single entry point (`landing-page/`) for the entire platform, providing access to all applications and centralized authentication.

## 3. Technology Stack

OpalSuite leverages a modern and robust technology stack to ensure high performance, scalability, and a consistent developer experience.

### Frontend

*   **React**: A declarative, component-based JavaScript library for building user interfaces. Chosen for reusability, maintainability, and its extensive ecosystem.
*   **Bootstrap**: A popular CSS framework for developing responsive, mobile-first websites. Provides a solid foundation for rapid UI development and consistent design.
*   **Custom CSS**: Tailored stylesheets for OpalSuite's unique branding and design elements, ensuring adherence to specific brand guidelines.

### Backend

*   **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. Offers excellent performance, automatic API documentation, and asynchronous capabilities.
*   **Python**: A versatile, high-level, interpreted programming language. Chosen for its readability, extensive libraries, and productivity in backend development.

### Database

*   **SQLAlchemy**: A powerful and flexible SQL toolkit and Object Relational Mapper (ORM) for Python. Provides a robust way to interact with relational databases using Python objects.
*   **SQLite** (for local development): A self-contained, serverless, zero-configuration, transactional SQL database engine. Ideal for local development due to its simplicity.
*   **PostgreSQL** (for cloud deployment): A powerful, open-source object-relational database system. Renowned for its reliability, features, scalability, and performance in production environments.

## 4. Current Applications

The following applications have been integrated into the OpalSuite monorepo:

*   **RegressionInsight**: Automates regression report generation.
*   **StandupBot**: Manages standup reports, refactored to FastAPI/React.
*   **BuildPilot**: Manages build processes.
*   **CalMind**: A calendar and mind management tool.
*   **MonitorIQ**: Provides intelligent system monitoring and alerts.
*   **XrayQC**: A quality control tool for X-ray images.

## 5. Getting Started

To set up and run the OpalSuite project locally:

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
    *   **Run the shared backend (standalone):**
        ```bash
        ./shared/scripts/run_standalone_backend.sh
        ```
    *   **Run the shared backend (Docker):**
        ```bash
        ./shared/scripts/run_docker_backend.sh
        ```
    *   **Deploy the shared backend to GCP (Cloud Run):**
        ```bash
        ./shared/scripts/deploy_gcp_backend.sh
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

## 6. Code Quality and Architectural Integrity

To maintain high code quality and a consistent architecture, OpalSuite uses a combination of tools and scripts:

*   **Formatting and Linting:** `black`, `isort`, and `flake8` are used to enforce code style and quality. These are managed through pre-commit hooks.
*   **Architectural Checks:** The `scripts/check_architecture.py` script enforces key architectural rules, such as preventing direct Redis imports, ensuring that new authentication or UI modules are not created outside of the designated shared directories, and validating shell scripts for direct `docker` or `gcloud` commands outside of designated common scripts.

For more detailed information, please refer to the `gemini.md` file.
