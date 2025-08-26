# OpalSuite Landing Page

## Overview

The `landing-page/` module serves as the primary entry point for the entire `OpalSuite` platform. It is a React-based web application designed to provide a centralized hub where users can discover and access all available applications within the monorepo. The landing page is built with extensibility in mind, allowing for easy integration with a centralized authentication module.

## Architecture

### 1. React Application

*   **Foundation:** The landing page is a standard Create React App (CRA) project, providing a familiar and efficient development environment.
*   **Component-Based:** The UI is built using React components, promoting reusability and maintainability.

### 2. Application Listing

*   **Dynamic Listing (Future):** While currently hardcoded for demonstration, the application list can be dynamically fetched from a backend service (e.g., the `OpalSuite` shared backend) in the future.
*   **Navigation:** Each listed application provides a link that, when clicked, redirects the user to the respective application's URL. This requires proper routing configuration at the central web server level.

### 3. Authentication Integration

*   **Placeholder:** The landing page includes a dedicated section and UI elements (e.g., a login button) as a placeholder for integration with the `OpalSuite`'s centralized authentication service (`shared/common/auth/`).
*   **Future Flow:** Upon integration, users will be able to log in or register directly from the landing page, and their authentication status will be managed by the central authentication service.

### 4. Styling

*   **Shared Design System:** The landing page is designed to integrate with the `OpalSuite`'s shared frontend base (`shared/frontend_base/`), ensuring a consistent look and feel with other applications in the suite.
*   **Technology:** Utilizes React and Bootstrap for responsive and modern UI design.

## How it Fits into OpalSuite

*   **Central Entry Point:** Provides a single, intuitive starting point for users to navigate the entire `OpalSuite` platform.
*   **Unified Experience:** Contributes to a cohesive user experience by presenting all applications under a common visual and navigational umbrella.
*   **Authentication Gateway:** Acts as the primary interface for user authentication, directing users to the central authentication service.

## Getting Started (Development)

1.  **Install Dependencies:** Navigate to `OpalSuite/landing-page/` and install Node.js dependencies:
    ```bash
    npm install
    ```
2.  **Start Development Server:** Run the React development server:
    ```bash
    npm start
    ```
3.  **Integrate with Shared Frontend Base:** To achieve consistent styling, you will need to configure this project to import and use components/styles from `OpalSuite/shared/frontend_base/`.
4.  **Integrate Authentication:** Connect the login/registration UI to the `OpalSuite`'s centralized authentication service endpoints.

## Future Enhancements

*   **Dynamic Application Listing:** Fetch the list of available applications from a backend service.
*   **User-Specific Dashboards:** Display personalized content or application access based on user roles and permissions.
*   **Notifications:** Integrate with a centralized notification system.
*   **Search Functionality:** Allow users to search for applications or content within the suite.
