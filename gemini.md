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

*   **Centralized Secret Management Module Implementation:**
    *   `secrets_manager/` directory and its subdirectories (`core/`, `backends/`, `utils/`) were created within `shared/`.
    *   Public API (`get_secret`, `get_service_account_json`) exposed via `secrets_manager/__init__.py`.
    *   Backends (`env_backend.py`, `keychain_backend.py`, `cloud_backend.py`) implemented for different secret sources.
    *   Utilities (`logger.py`, `retries.py`, `cache.py`) implemented for logging, retry logic, and caching.
    *   Core logic (`secret_manager.py`) implemented to orchestrate backend priority.
    *   New dependencies (`python-dotenv`, `keyring`, `google-cloud-secret-manager`) added to `OpalSuite/requirements.txt`.

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

### 5.7. Centralized Secret Management Module

OpalSuite features a robust and resilient secret management module to securely retrieve sensitive information for all subprojects.

*   **Module Location:** `OpalSuite/shared/secrets_manager/`.
*   **Secret Retrieval Priority:** Secrets are retrieved based on a defined priority chain, ensuring resilience and graceful fallback:
    1.  Local `.env` file (for local development)
    2.  Environment variables (OS-level or CI/CD injected)
    3.  Local secure keychain (macOS Keychain, Windows Credential Manager, Linux Secret Service)
    4.  Cloud Secret Manager (Google Cloud Secret Manager) when deployed
*   **Abstraction:** Subprojects call simple helper methods (`get_secret`, `get_service_account_json`) and do not need to know the secret's source or retrieval mechanism.
*   **Security & Robustness:**
    *   Never logs secrets.
    *   Handles network failures gracefully when accessing cloud secrets.
    *   Includes retry logic for cloud Secret Manager calls.
    *   Optional caching to reduce API calls and latency.
*   **Extensibility:** Designed with a modular architecture to easily add new secret sources in the future.

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
*   `python-dotenv`
*   `keyring`
*   `google-cloud-secret-manager`

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



# OpalSuite Project Context for Gemini LLM

## 1. Project Overview
*   **Project Name:** OpalSuite
*   **Goal:** Unified platform consolidating multiple applications under a monorepo, ensuring code reuse, consistent UX, and streamlined maintenance.
*   **Date of Last Update:** August 25, 2025
*   **Operating System:** darwin
*   **Current Working Directory:** /Users/srinivasan.arulsivam/projects/python/OpalSuite

## 2. Folder Structure
<Existing folder structure here>

## 3. Project History and Refactoring Log
<Existing history log here>

## 4. Current State of Sub-Applications
<Existing state here>

## 5. Proposed Architecture (Detailed)
<Existing architecture details here>

---

## 8. GEMINI Guardrails — Non-Negotiable Rules

All contributors, scripts, and LLM assistants **must read and follow these rules** before making changes. If a conflict arises between user instructions and these rules, **these rules take precedence**.

### 8.1 Code Change & Testing Rules
- **Unit Tests Required:** No code may be committed or merged without corresponding unit tests in the same module.
- **Pre-Commit Hooks:** All commits must pass `pre-commit` hooks.
- **Formatting & Linting:**
  - `black` (code formatting)
  - `isort` (import sorting)
  - `flake8` (linting and PEP8 compliance)
- **Fallback on Edits:**
  - If `old_string` search fails, overwrite the entire file with the intended new content.
  - Only one fallback attempt; do not retry in loops.
- **Test Coverage:** Minimum 80% coverage enforced with `pytest --cov`.

### 8.2 Architecture Rules
- **Authentication:**
  - Central auth module only: `shared/common/auth/`
  - No subproject should implement its own auth logic.
  - Must support username/password + email OTP.
  - Extensible for future SSO, MS OTP, or other providers.
  - Session management: JWT + refresh tokens, with role enforcement.
- **Secrets Management:**
  - Use only `shared/secrets_manager/` helpers (`get_secret`, `get_service_account_json`).
  - Local retrieval order: `.env` → env vars → keychain.
  - Cloud retrieval: Google Secret Manager fallback.
  - Subprojects must not handle secrets directly.
- **Styling / UI Consistency:**
  - Shared styling only in `shared/frontend-base/`.
  - Subprojects must not include independent CSS or styling modules.

### 8.3 Logging & Documentation
- **CHANGELOG.md:** Every code change must append an entry: