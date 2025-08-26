# OpalSuite Shared Database Base

## Overview

The `shared/database_base/` module establishes the foundation for `OpalSuite`'s common database. Its primary goal is to eliminate data duplication across sub-applications and provide a single, consistent mechanism for database connectivity and ORM model definition. This centralization simplifies data management, ensures data integrity, and facilitates cross-application data access.

## Architecture

### 1. Database Connection and Session Management (`database.py`)

*   **SQLAlchemy Engine:** Defines the central SQLAlchemy `engine` for connecting to the database. This engine is configured to point to the shared `opal_suite.db` (or a Cloud SQL instance in production).
*   **SessionLocal:** A session factory for creating database sessions. This ensures that each request or operation gets its own isolated database session.
*   **Base:** The declarative base (`Base`) for defining SQLAlchemy ORM models. All shared and application-specific models within `OpalSuite` should inherit from this `Base`.
*   **`get_db()` Dependency:** A FastAPI dependency function that provides a database session (`Session`) to API endpoints, ensuring proper session lifecycle management (creation, yielding, and closing).

### 2. Common Database Models (`models/`)

*   **Shared Entities:** The `models/` subdirectory contains SQLAlchemy ORM models for entities that are common across multiple `OpalSuite` applications. A prime example is the `User` model, which is central to the authentication service.
*   **Inheritance:** All models defined here, and in individual sub-applications, inherit from the `Base` defined in `database.py`.

## How it Fits into OpalSuite

*   **Single Source of Truth:** Ensures that all applications operate on the same, consistent dataset, preventing data silos and inconsistencies.
*   **Simplified Data Management:** Centralizes database schema definitions and connection logic, making it easier to manage and evolve the database.
*   **Cross-Application Data Access:** Facilitates seamless data sharing and interaction between different sub-applications.
*   **Scalability:** Designed to connect to a robust database solution (like Cloud SQL), supporting the scalability needs of the entire platform.

## Getting Started (Development)

1.  **Database URL:** Ensure the `SQLALCHEMY_DATABASE_URL` in `database.py` is correctly configured for your development environment (e.g., `sqlite:///./opal_suite.db`).
2.  **Initialize Database:** Run the `init_shared_db.py` script from the `OpalSuite` root to create the necessary tables in the shared database:
    ```bash
    python init_shared_db.py
    ```
3.  **Integrate Models:** When creating or refactoring models in sub-applications, ensure they import `Base` from `OpalSuite.shared.database_base.database` and inherit from it.

## Future Enhancements

*   **Alembic Migrations:** Implement Alembic for robust database schema migrations, especially crucial for managing changes to shared models.
*   **Database Connection Pooling:** Optimize database connections for high-traffic scenarios.
*   **Read Replicas/Sharding:** Explore advanced database scaling strategies for very large datasets or high read loads.
