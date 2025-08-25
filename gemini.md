# OpalSuite Project Context for Gemini LLM

## 1. Project Overview

*   **Project Name:** OpalSuite
*   **Goal:** To create a unified platform by consolidating various independent applications under a single monorepo umbrella. This aims to foster code reuse, ensure consistent user experience, and streamline development and maintenance.
*   **Date of Last Update:** August 25, 2025
*   **Operating System:** darwin
*   **Current Working Directory:** /Users/srinivasan.arulsivam/projects/python/OpalSuite

## 2. Folder Structure

The `OpalSuite` project is structured as a monorepo, containing individual sub-application directories and a `shared/` directory for common components.

```
/OpalSuite/
├───BuildPilot/
├───CalMind/
├───MonitorIQ/
├───RegressionInsight/
├───StandupBot/
├───XrayQC/
├───shared/
│   ├───backend/                # Main FastAPI application for shared services (e.g., authentication)
│   │   └───main.py
│   ├───common/                 # General utilities and shared Python code
│   │   └───auth/               # Centralized authentication service
│   │       ├───__init__.py
│   │       └───auth.py
│   ├───config-base/            # Shared configuration templates and schemas
│   │   └───README.md
│   ├───database-base/          # Common database configurations, base ORM models, and migration scripts
│   │   ├───database.py
│   │   └───models/
│   │       ├───__init__.py
│   │       └───user.py
│   ├───docs/                   # Project-wide documentation
│   │   └───README.md
│   ├───frontend-base/          # Centralized UI components, design system (Bootstrap-based), and shared frontend configurations
│   │   ├───node_modules/
│   │   ├───public/
│   │   ├───src/
│   │   │   ├───App.css
│   │   │   ├───App.js
│   │   │   ├───index.css
│   │   │   ├───index.js
│   │   │   ├───logo.svg
│   │   │   ├───reportWebVitals.js
│   │   │   └───setupTests.js
│   │   └───package.json
│   ├───scripts/                # Common build, deployment, and utility scripts
│   │   └───README.md
│   └───tests/                  # Centralized testing setup and utilities
│       └───README.md
├───landing-page/               # React application for the OpalSuite home/landing page
│   ├───node_modules/
│   ├───public/
│   ├───src/
│   │   ├───App.css
│   │   ├───App.js
│   │   ├───index.css
│   │   ├───index.js
│   │   ├───logo.svg
│   │   ├───reportWebVitals.js
│   │   └───setupTests.js
│   └───package.json
├───init_shared_db.py           # Script to initialize the common OpalSuite database
├───README.md                   # Project README
└───requirements.txt            # Root-level Python dependencies
```

## 3. Project History and Refactoring Log

This section details the evolution of the `OpalSuite` project and significant refactoring efforts.

*   **Initial Setup (August 25, 2025):**
    *   The `OpalSuite` root directory was created.
    *   Independent copies of `release-regression-reporter` and `StandupBot` were placed into `OpalSuite/`.
    *   A base project structure (`common`, `config-base`, `database-base`, `docs`, `frontend-base`, `scripts`, `tests`) was created at the `OpalSuite` root.

*   **Addition of More Sub-Applications:**
    *   Independent copies of `BuildPilot`, `CalMind`, `MonitorIQ`, and `XrayQC` were added to `OpalSuite/`.

*   **Application Renaming:**
    *   The `release-regression-reporter` application within `OpalSuite` was renamed to `RegressionInsight` for better clarity and branding.

*   **Consolidation of Common Modules:**
    *   All base project directories (`common`, `config-base`, `database-base`, `docs`, `frontend-base`, `scripts`, `tests`) were moved into a new `shared/` directory at the `OpalSuite` root to improve organization and clarity.

*   **Creation of Landing Page:**
    *   A `landing-page/` directory was created within `OpalSuite/`.
    *   A basic React application was initialized within `landing-page/` to serve as the `OpalSuite` home page, listing available applications and including a login placeholder.

*   **Refactoring of `StandupBot` (Flask to FastAPI/React Migration):**
    *   **Project Structure:** `StandupBot` was refactored into `shared/`, `backend/`, `frontend/`, and `cli/` directories.
    *   **Backend Migration:** The Flask backend was migrated to FastAPI.
        *   Flask controllers were converted to FastAPI routers (`backend/routers/auth.py`, `backend/routers/main.py`).
        *   `backend/main.py` was set up as the FastAPI entry point.
    *   **Database Integration:** The database setup was updated from Flask-SQLAlchemy to pure SQLAlchemy (`shared/database.py`, `shared/models/user.py`, `backend/init_db.py`).
    *   **Authentication:** Basic JWT authentication was implemented for the `StandupBot` backend.
    *   **CLI Refactoring:** CLI functionality was consolidated and updated.
    *   **Dependencies:** `requirements.txt` was updated, and Flask-related files were removed.

*   **Setup of CSS Consistency (Initial):**
    *   A React project was initialized in `OpalSuite/shared/frontend-base/` to act as a design system library.
    *   `bootstrap` and `react-bootstrap` were installed.
    *   `OpalSuite/shared/frontend-base/src/index.js` was configured to import Bootstrap CSS and a custom `main.css`.
    *   `OpalSuite/shared/frontend-base/src/styles/main.css` was created as a placeholder.

*   **Setup of Common Database (Initial):**
    *   `OpalSuite/shared/database-base/database.py` was created with a central SQLAlchemy configuration.
    *   `OpalSuite/shared/database-base/models/` directory was created.
    *   A basic `User` model was defined in `OpalSuite/shared/database-base/models/user.py` for centralized authentication.

*   **Setup of Centralized Authentication (Backend):**
    *   `OpalSuite/shared/common/auth/auth.py` was created with a basic FastAPI authentication router (register, login with JWT, get current user).
    *   `OpalSuite/backend/main.py` was created as the main FastAPI application for shared services, including the authentication router.
    *   `OpalSuite/requirements.txt` was created for the root project.
    *   `OpalSuite/init_shared_db.py` was created to initialize the shared database.

*   **Code Quality and Pre-Commit Setup:**
    *   `black`, `isort`, `flake8`, and `pre-commit` were installed.
    *   `pyproject.toml` was created for `black`, `isort`, and `flake8` configurations.
    *   `.pre-commit-config.yaml` was created to define pre-commit hooks for formatting and linting.
    *   `pre-commit` hooks were installed into the Git repository.

## 4. Current State of Sub-Applications

*   **RegressionInsight:**
    *   **Status:** Copied into `OpalSuite/`, renamed from `release-regression-reporter`.
    *   **Original Tech Stack:** Python (FastAPI), React, Jira integration, pandas, Docker.
    *   **Note:** Its internal structure and dependencies are still as per its original project.

*   **StandupBot:**
    *   **Status:** Copied into `OpalSuite/`, and has undergone significant refactoring to align with the `OpalSuite` architecture.
    *   **Current Tech Stack:** Python (FastAPI), React, SQLAlchemy (common database), JWT authentication.
    *   **Note:** Its backend has been migrated from Flask to FastAPI, and its database and authentication are now designed to integrate with the shared `OpalSuite` components. Its frontend is a new React app.

*   **BuildPilot, CalMind, MonitorIQ, XrayQC:**
    *   **Status:** Copied into `OpalSuite/`.
    *   **Original Tech Stacks:** (As per their original `gemini.md` or project files, not yet analyzed in detail for `OpalSuite` context).
    *   **Note:** These applications are currently independent within `OpalSuite` and have not yet been refactored to utilize the shared components.

## 5. Proposed Architecture (Detailed)

OpalSuite is designed as a monorepo to foster code reuse, consistency, and streamlined development.

### 5.1. Monorepo Structure

*   **Root Level (`/OpalSuite/`):**
    *   `README.md`: Project overview.
    *   `gemini.md`: Comprehensive project context for LLMs.
    *   `requirements.txt`: Root-level Python dependencies for shared services.
    *   `init_shared_db.py`: Script to initialize the common `OpalSuite` database.
    *   `landing-page/`: The main entry point web application.
    *   Individual sub-application directories (e.g., `RegressionInsight/`, `StandupBot/`).
    *   `shared/`: The core of the monorepo, containing all common and reusable components.

*   **`shared/` Directory:**
    *   **`backend/`:**
        *   `main.py`: The central FastAPI application for `OpalSuite`'s shared services (e.g., authentication, common APIs).
    *   **`common/`:**
        *   `auth/`: Contains the centralized authentication service.
            *   `auth.py`: FastAPI router for user registration, login (JWT token issuance), and token validation.
    *   **`config-base/`:**
        *   Placeholder for shared configuration templates, environment variables, and schema definitions.
    *   **`database-base/`:**
        *   `database.py`: Defines the central SQLAlchemy `engine`, `SessionLocal`, and `Base` for the common database.
        *   `models/`: Contains SQLAlchemy models for entities shared across applications (e.g., `User`).
    *   **`frontend-base/`:**
        *   A React project serving as a design system library. It will export reusable UI components (e.g., `OpalButton`, `OpalCard`) that wrap Bootstrap components and apply `OpalSuite`'s custom styling.
    *   **`docs/`:**
        *   Centralized documentation for the entire `OpalSuite` platform.
    *   **`scripts/`:**
        *   Common build, deployment, and utility scripts applicable across the monorepo.
    *   **`tests/`:**
        *   Centralized testing setup and utilities for shared components and integration tests.

### 5.2. Centralized Authentication

*   **Service Location:** `OpalSuite/shared/common/auth/auth.py`
*   **Technology:** FastAPI, JWT (JSON Web Tokens), `passlib` for password hashing.
*   **Functionality:**
    *   User registration (`/auth/register`).
    *   User login and JWT token issuance (`/auth/token`).
    *   JWT token validation and user retrieval (`get_current_user` dependency).
*   **Database Integration:** Uses the `User` model from `OpalSuite/shared/database-base/models/user.py` and connects to the common database.
*   **Integration:**
    *   The `OpalSuite/backend/main.py` includes this authentication router.
    *   The `landing-page` will interact with these endpoints for user authentication.
    *   Sub-applications will use the `get_current_user` dependency to protect their routes and will send JWT tokens with their requests.

### 5.3. Common Database

*   **Location:** `OpalSuite/shared/database-base/database.py`
*   **Technology:** SQLAlchemy.
*   **Database File:** `opal_suite.db` (SQLite, configurable for other databases like PostgreSQL).
*   **Components:**
    *   `engine`: SQLAlchemy engine for connecting to the database.
    *   `SessionLocal`: Session factory for creating database sessions.
    *   `Base`: Declarative base for defining SQLAlchemy models.
    *   `get_db()`: FastAPI dependency for managing database sessions.
*   **Common Models:** Defined in `OpalSuite/shared/database-base/models/` (e.g., `User` model).
*   **Initialization:** `OpalSuite/init_shared_db.py` script for creating database tables.

### 5.4. Consistent User Interface

*   **Location:** `OpalSuite/shared/frontend-base/`
*   **Technology:** React, Bootstrap, custom CSS.
*   **Purpose:** To provide a unified look and feel across all `OpalSuite` applications.
*   **Components:**
    *   Bootstrap CSS imported centrally.
    *   `OpalSuite/shared/frontend-base/src/styles/main.css` for custom branding.
    *   Will export reusable UI components that wrap Bootstrap components with `OpalSuite`'s design.

### 5.5. Landing Page

*   **Location:** `OpalSuite/landing-page/`
*   **Technology:** React.
*   **Purpose:** Serves as the main entry point for `OpalSuite`, listing all available applications and providing a gateway for centralized authentication.

### 5.6. Routing and Deployment

*   **Central Web Server:** A web server (e.g., Nginx, Traefik) will be used at the `OpalSuite` root to act as a reverse proxy, routing traffic to the `landing-page` and individual sub-applications.
*   **Containerization:** Docker and Docker Compose are recommended for orchestrating all services (shared backend, landing page, and each sub-application's backend/frontend) for simplified development and deployment.

## 6. Key Decisions and Rationale

*   **Monorepo:** Chosen for code reuse, consistent development practices, and easier management of shared components.
*   **FastAPI for Backend:** Selected for its high performance, modern features (async/await, Pydantic for data validation), and built-in API documentation, aligning with `RegressionInsight`'s existing stack.
*   **React for Frontend:** Chosen for its component-based architecture, popularity, and efficiency in building complex UIs, aligning with `RegressionInsight`'s existing stack.
*   **SQLAlchemy for ORM:** Provides a powerful and flexible way to interact with the database, already used in `StandupBot` (after refactoring).
*   **Bootstrap for UI Consistency:** A widely adopted CSS framework that provides a solid foundation for responsive design and can be easily customized for `OpalSuite`'s branding.
*   **Centralized Authentication:** Essential for a suite of applications to provide a single sign-on experience and centralized user management.

## 7. Dependencies

### Root-Level Python Dependencies (`OpalSuite/requirements.txt`):

*   `fastapi`
*   `uvicorn[standard]`
*   `sqlalchemy`
*   `passlib[bcrypt]`
*   `python-jose[cryptography]`

### Shared Frontend Dependencies (`OpalSuite/shared/frontend-base/package.json`):

*   `react`
*   `react-dom`
*   `react-scripts`
*   `bootstrap`
*   `react-bootstrap`

### Landing Page Dependencies (`OpalSuite/landing-page/package.json`):

*   `react`
*   `react-dom`
*   `react-scripts`
*   `bootstrap` (will be added when integrating shared frontend-base)
*   `react-bootstrap` (will be added when integrating shared frontend-base)

### Sub-Application Dependencies:

(These will vary per application and will be updated as they are integrated with shared components.)

## 7.1. Code Quality and Consistency Tools

To maintain high code quality and consistency across the monorepo, the following tools have been integrated:

*   **Black**: An uncompromising Python code formatter.
    *   **Configuration (`pyproject.toml`):**
        ```toml
        [tool.black]
        line-length = 88
        target-version = ['py311']
        include = '\.pyi?

To fully realize the `OpalSuite` vision with consistent look and feel, common database, and centralized authentication, you will need to perform the following tasks:

1.  **Full CSS Integration:**
    *   **Develop `shared/frontend-base/`:** Refactor the `OpalSuite/shared/frontend-base/` project to create and export reusable UI components (e.g., `OpalButton`, `OpalCard`, `OpalNavbar`) that wrap Bootstrap components and apply `OpalSuite`'s custom styling.
    *   **Integrate into Sub-Applications' Frontends:** For each React-based sub-application (`OpalSuite/landing-page`, `OpalSuite/StandupBot/frontend`, `OpalSuite/RegressionInsight/frontend`, etc.):
        *   Configure their build systems (e.g., Webpack/CRA) to correctly resolve imports from `OpalSuite/shared/frontend-base/`.
        *   Modify their `index.js` or `App.js` to import the shared Bootstrap CSS and your custom `OpalSuite` styles.
        *   Gradually replace existing UI components with the `Opal` prefixed components from `OpalSuite/shared/frontend-base/`.

2.  **Full Common Database Integration:**
    *   **Define All Common Models:** Identify any other database models that are truly shared across multiple applications (beyond just `User`) and define them within `OpalSuite/shared/database-base/models/`.
    *   **Integrate into Sub-Applications' Backends:** For each Python-based sub-application's backend (e.g., `OpalSuite/RegressionInsight/backend`, `OpalSuite/StandupBot/backend`, `OpalSuite/BuildPilot`, `OpalSuite/CalMind`, `OpalSuite/MonitorIQ`, `OpalSuite/XrayQC`):
        *   Modify their database connection and session management to use the shared SQLAlchemy `engine`, `SessionLocal`, `Base`, and `get_db` from `OpalSuite/shared/database-base/database.py`.
        *   Refactor their existing database models to inherit from the shared `Base` and utilize the common models where applicable (e.g., replace their local `User` model with the one from `OpalSuite/shared/database-base/models/user.py`).
        *   Plan and execute database migrations (e.g., using Alembic) for the shared database schema.

3.  **Full Centralized Authentication Integration:**
    *   **Run the Shared Backend:** Start the `OpalSuite` shared backend (`uvicorn OpalSuite.backend.main:app --host 0.0.0.0 --port 8000`). This will expose the central authentication endpoints.
    *   **Integrate with Landing Page:** Modify the `OpalSuite/landing-page/` React app to interact with the `/auth/register` and `/auth/token` endpoints of the shared backend for user registration and login. Implement secure storage and usage of the received JWT token.
    *   **Integrate with Sub-Applications' Backends:** Update each sub-application's backend to use the `get_current_user` dependency from `OpalSuite/shared/common/auth/auth.py` to protect its routes.
    *   **Integrate with Sub-Applications' Frontends:** Modify each sub-application's frontend to send the JWT token with its requests to its respective backend for authentication.

4.  **Centralized Routing and Deployment:**
    *   **Central Web Server:** Set up a web server (e.g., Nginx, Traefik) at the `OpalSuite` root. This server will act as a reverse proxy, routing traffic to the `landing-page` and each sub-application based on URL paths (e.g., `/` for the landing page, `/regression-insight` for the `RegressionInsight` app, etc.).
    *   **Containerization (Recommended):** Use Docker and Docker Compose to containerize each sub-application's backend and frontend, as well as the `OpalSuite` shared backend and landing page. This will simplify dependency management, deployment, and local development.

5.  **Comprehensive Testing:**
    *   After each integration step, thoroughly test all functionalities (unit, integration, and end-to-end tests) to ensure that the changes have not introduced regressions and that the new integrated system works as expected.

        exclude = '/(?:\.git|\.venv|node_modules|build|dist|__pycache__)/'
        ```
*   **isort**: A Python utility to sort imports alphabetically and automatically separate them into sections.
    *   **Configuration (`pyproject.toml`):**
        ```toml
        [tool.isort]
        profile = "black"
        multi_line_output = 3
        include_trailing_comma = true
        force_grid_wrap = 0
        use_parentheses = true
        ensure_newline_before_comments = true
        line_length = 88
        skip_glob = [
            "*/.venv/*",
            "*/node_modules/*",
            "*/build/*",
            "*/dist/*",
            "*/__pycache__/*",
        ]
        ```
*   **Flake8**: A tool for enforcing style guide (PEP8) and checking for common programming errors.
    *   **Configuration (`pyproject.toml`):**
        ```toml
        [tool.flake8]
        max-line-length = 88
        extend-ignore = ["E203", "W503"]
        exclude = [
            ".git",
            ".venv",
            "node_modules",
            "build",
            "dist",
            "__pycache__",
        ]
        ```
*   **pre-commit**: Used to manage and maintain pre-commit git hooks, ensuring that code is formatted and linted before every commit.
    *   **Configuration (`.pre-commit-config.yaml`):**
        ```yaml
        repos:
          - repo: https://github.com/pre-commit/pre-commit-hooks
            rev: v4.4.0
            hooks:
              - id: trailing-whitespace
              - id: end-of-file-fixer
              - id: check-yaml
              - id: check-added-large-files

          - repo: https://github.com/psf/black
            rev: 23.3.0
            hooks:
              - id: black

          - repo: https://github.com/PyCQA/isort
            rev: 5.12.0
            hooks:
              - id: isort

          - repo: https://github.com/PyCQA/flake8
            rev: 6.0.0
            hooks:
              - id: flake8
        ```

## 8. Roadmap and Next Steps (Detailed)

To fully realize the `OpalSuite` vision with consistent look and feel, common database, and centralized authentication, you will need to perform the following tasks:

1.  **Full CSS Integration:**
    *   **Develop `shared/frontend-base/`:** Refactor the `OpalSuite/shared/frontend-base/` project to create and export reusable UI components (e.g., `OpalButton`, `OpalCard`, `OpalNavbar`) that wrap Bootstrap components and apply `OpalSuite`'s custom styling.
    *   **Integrate into Sub-Applications' Frontends:** For each React-based sub-application (`OpalSuite/landing-page`, `OpalSuite/StandupBot/frontend`, `OpalSuite/RegressionInsight/frontend`, etc.):
        *   Configure their build systems (e.g., Webpack/CRA) to correctly resolve imports from `OpalSuite/shared/frontend-base/`.
        *   Modify their `index.js` or `App.js` to import the shared Bootstrap CSS and your custom `OpalSuite` styles.
        *   Gradually replace existing UI components with the `Opal` prefixed components from `OpalSuite/shared/frontend-base/`.

2.  **Full Common Database Integration:**
    *   **Define All Common Models:** Identify any other database models that are truly shared across multiple applications (beyond just `User`) and define them within `OpalSuite/shared/database-base/models/`.
    *   **Integrate into Sub-Applications' Backends:** For each Python-based sub-application's backend (e.g., `OpalSuite/RegressionInsight/backend`, `OpalSuite/StandupBot/backend`, `OpalSuite/BuildPilot`, `OpalSuite/CalMind`, `OpalSuite/MonitorIQ`, `OpalSuite/XrayQC`):
        *   Modify their database connection and session management to use the shared SQLAlchemy `engine`, `SessionLocal`, `Base`, and `get_db` from `OpalSuite/shared/database-base/database.py`.
        *   Refactor their existing database models to inherit from the shared `Base` and utilize the common models where applicable (e.g., replace their local `User` model with the one from `OpalSuite/shared/database-base/models/user.py`).
        *   Plan and execute database migrations (e.g., using Alembic) for the shared database schema.

3.  **Full Centralized Authentication Integration:**
    *   **Run the Shared Backend:** Start the `OpalSuite` shared backend (`uvicorn OpalSuite.backend.main:app --host 0.0.0.0 --port 8000`). This will expose the central authentication endpoints.
    *   **Integrate with Landing Page:** Modify the `OpalSuite/landing-page/` React app to interact with the `/auth/register` and `/auth/token` endpoints of the shared backend for user registration and login. Implement secure storage and usage of the received JWT token.
    *   **Integrate with Sub-Applications' Backends:** Update each sub-application's backend to use the `get_current_user` dependency from `OpalSuite/shared/common/auth/auth.py` to protect its routes.
    *   **Integrate with Sub-Applications' Frontends:** Modify each sub-application's frontend to send the JWT token with its requests to its respective backend for authentication.

4.  **Centralized Routing and Deployment:**
    *   **Central Web Server:** Set up a web server (e.g., Nginx, Traefik) at the `OpalSuite` root. This server will act as a reverse proxy, routing traffic to the `landing-page` and each sub-application based on URL paths (e.g., `/` for the landing page, `/regression-insight` for the `RegressionInsight` app, etc.).
    *   **Containerization (Recommended):** Use Docker and Docker Compose to containerize each sub-application's backend and frontend, as well as the `OpalSuite` shared backend and landing page. This will simplify dependency management, deployment, and local development.

5.  **Comprehensive Testing:**
    *   After each integration step, thoroughly test all functionalities (unit, integration, and end-to-end tests) to ensure that the changes have not introduced regressions and that the new integrated system works as expected.
