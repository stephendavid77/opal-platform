# OpalSuite: A Unified Application Platform

## Overview

OpalSuite is a project designed to consolidate various independent applications under a single, unified umbrella. The goal is to create a cohesive platform where different tools and services can coexist, share common functionalities, and provide a consistent user experience. This monorepo approach aims to streamline development, improve maintainability, and foster code reuse across applications.

## Current Applications

The following applications have been copied into the OpalSuite monorepo:

*   **RegressionInsight** (formerly `release-regression-reporter`): An application for automating regression report generation.
*   **StandupBot**: A tool for managing standup reports, currently undergoing refactoring to align with the new architecture.
*   **BuildPilot**
*   **CalMind**
*   **MonitorIQ**
*   **XrayQC**

## Proposed Architecture

OpalSuite is structured as a monorepo, emphasizing shared components and centralized services to achieve consistency and efficiency.

### 1. Monorepo Structure

*   **Root Level:** Contains the main `OpalSuite` configuration, shared services, and individual application directories.
*   **`shared/` Directory:** Houses all common modules and base components that can be inherited or utilized by sub-applications. This includes:
    *   `common/`: General utilities and shared Python code.
    *   `frontend-base/`: Centralized UI components, design system (Bootstrap-based), and shared frontend configurations.
    *   `database-base/`: Common database configurations, base ORM models, and migration scripts.
    *   `config-base/`: Shared configuration templates and schemas.
    *   `docs/`: Project-wide documentation.
    *   `scripts/`: Common build, deployment, and utility scripts.
    *   `tests/`: Centralized testing setup and utilities.
*   **Sub-Application Directories:** Each application (`RegressionInsight`, `StandupBot`, etc.) resides in its own directory, containing its specific backend, frontend, and other components.

### 2. Centralized Authentication

*   A dedicated authentication service (`OpalSuite/shared/common/auth/`) handles user registration, login, and JWT token management.
*   This service interacts with a common user database.
*   All applications will integrate with this central authentication system.

### 3. Common Database

*   A single, shared database instance (`opal_suite.db` for SQLite, configurable for others) is used across the platform.
*   Common database models (e.g., `User`) are defined in `OpalSuite/shared/database-base/models/`.
*   Applications will connect to and utilize this common database, reducing data duplication.

### 4. Consistent User Interface

*   A central design system based on Bootstrap is established in `OpalSuite/shared/frontend-base/`.
*   This provides reusable UI components and consistent styling across all applications.
*   The `OpalSuite` landing page serves as the primary entry point, listing all available applications.

## Getting Started (High-Level)

1.  **Install Root Dependencies:** Navigate to the `OpalSuite` root and install Python dependencies from `requirements.txt`.
2.  **Initialize Shared Database:** Run `python init_shared_db.py` to set up the common database tables.
3.  **Start Shared Backend:** Run the main FastAPI application for shared services (e.g., authentication).
4.  **Develop/Run Sub-Applications:** Each application will have its own setup for running its backend and frontend, integrating with the shared components.
5.  **Centralized Routing:** Set up a web server (e.g., Nginx) to route traffic to the landing page and individual applications.

## Code Quality and Consistency

To maintain high code quality and consistency across the monorepo, the following tools have been integrated:

*   **Black**: An uncompromising Python code formatter.
*   **isort**: A Python utility to sort imports alphabetically and automatically separate them into sections.
*   **Flake8**: A tool for enforcing style guide (PEP8) and checking for common programming errors.
*   **pre-commit**: Used to manage and maintain pre-commit git hooks, ensuring that code is formatted and linted before every commit.

For detailed instructions and further development, refer to the `gemini.md` file.
