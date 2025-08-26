# OpalSuite Shared Backend Module

## Overview

The `shared/backend/` module serves as the central FastAPI application for `OpalSuite`'s shared services. Its primary role is to aggregate and expose common APIs that are utilized by various sub-applications within the monorepo. This module acts as a gateway for functionalities that are shared across the platform, such as authentication, and can be extended to include other common services.

## Architecture

### 1. Core Application (`main.py`)

*   **FastAPI Instance:** The `main.py` file initializes the core FastAPI application for shared services.
*   **Router Inclusion:** It includes routers from other shared modules, such as the authentication router from `shared/common/auth/`.

### 2. Integration with Other Shared Modules

*   **Authentication (`shared/common/auth/`):** The `shared/backend/` module integrates directly with the centralized authentication service. It includes the authentication router, making endpoints like `/auth/register` and `/auth/token` accessible through this central backend.
*   **Database (`shared/database_base/`):** While the authentication service (within `shared/common/auth/`) directly interacts with the common database, any future shared APIs exposed by `shared/backend/` would also utilize the database connection and models defined in `shared/database_base/`.

## How it Fits into OpalSuite

*   **Centralized API Gateway:** It provides a single, consistent entry point for sub-applications to access shared functionalities, reducing the need for each sub-application to implement or directly connect to multiple shared services.
*   **Scalability:** As a FastAPI application, it is designed for high performance and scalability, capable of handling requests from numerous sub-applications.
*   **Modularity:** By including routers from other shared modules, it maintains a modular structure, allowing for easy addition or modification of shared services without impacting the core application logic.

## Getting Started (Development)

To run this shared backend locally:

1.  Ensure you have installed the root-level Python dependencies (`pip install -r requirements.txt` from the `OpalSuite` root).
2.  Initialize the shared database (`python init_shared_db.py` from the `OpalSuite` root).
3.  Run the FastAPI application:
    ```bash
    uvicorn OpalSuite.shared.backend.main:app --host 0.0.0.0 --port 8000
    ```
    (Note: The module is `OpalSuite.shared.backend.main` because it's part of the `OpalSuite` package structure.)

## Future Enhancements

*   **Additional Shared APIs:** Extend with other common APIs required by multiple sub-applications.
*   **API Versioning:** Implement API versioning (e.g., `/api/v1/`) for better management of API changes.
*   **Monitoring & Logging:** Integrate with centralized monitoring and logging solutions.
