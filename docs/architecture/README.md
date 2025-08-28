# Architecture Documentation

This section contains the architecture documentation for the OpalSuite project, including module architecture checks.

## Overall Architecture

OpalSuite is built upon a multi-repo architecture, with a central repository for shared components and separate repositories for each application.

This architecture allows for independent development, versioning, and deployment of each application, while still providing a way to share code and maintain consistency across the ecosystem.

## Multi-Repo Structure

The OpalSuite ecosystem is composed of the following repositories:

*   **`OpalSuite`**: This repository, which serves as a central hub for documentation, guidelines, and architectural standards.
*   **`opal-database`**: Contains the shared database models and connection logic.
*   **`opal-auth-backend`**: Contains the authentication backend service.
*   **`opal-shared-utils`**: Contains shared utilities, such as configuration and secrets management.
*   **`opal-global-ui`**: Contains the shared UI components and styles.
*   **`opal-auth-frontend`**: Contains the authentication-related UI components.
*   **`opal-portal`**: Contains the main portal application, which includes the landing page and the shared backend.
*   **Application Repositories**: Each application (`BuildPilot`, `CalMind`, etc.) has its own repository.

## Module Architecture Checks

To maintain the integrity of the architecture, we use a set of module architecture checks. These checks are implemented as pre-commit hooks and are defined in the `pyproject.toml` file.

The checks ensure that:

*   Applications do not implement their own authentication or database logic.
*   Shared components are only defined in the appropriate shared repositories.
*   Dependencies between repositories are correctly managed.
