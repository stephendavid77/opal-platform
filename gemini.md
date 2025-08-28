# OpalSuite Project Overview and Gemini Guidelines

This document provides a comprehensive overview of the OpalSuite project, its architecture, technology stack, and development practices, along with guidelines for effective interaction with the Gemini model.

## 1. OpalSuite Project Overview

### 1.1 Purpose
OpalSuite is a unified platform designed to consolidate various independent Python productivity applications.

### 1.2 Architecture
OpalSuite employs a multi-repository architecture:
*   **Shared Repositories:** Individual repositories provide common and reusable components, including:
    *   `opal-auth-backend`: Provides centralized authentication (FastAPI, JWT).
    *   `opal-shared-utils`: Offers secure secret management and other shared utilities.
    *   `opal-database`: Contains shared SQLAlchemy database models and connection logic.
    *   `opal-global-ui`: A React and Bootstrap-based design system for consistent user experience.
    *   `opal-auth-frontend`: Contains authentication-related UI components.
    *   `opal-portal`: The main portal application, including the landing page and shared backend.
    *   `opal-dev-tools`: Contains tools for maintaining architectural integrity, including module architecture checks.
*   **Application Repositories:** Each application resides in its own repository, consuming shared components as versioned dependencies, enabling independent development, testing, and deployment.
*   **Main Repository (`OpalSuite`):** Serves as a central hub for documentation, guidelines, and architectural standards.

### 1.3 Key Repositories
*   **Shared Repositories:**
    *   `opal-database`: Shared database models and connection logic.
    *   `opal-auth-backend`: Authentication backend service.
    *   `opal-shared-utils`: Shared utilities (configuration, secrets management).
    *   `opal-global-ui`: Shared UI components and styles.
    *   `opal-auth-frontend`: Authentication-related UI components.
    *   `opal-portal`: Main portal application, which includes the landing page and the shared backend.
    *   `opal-dev-tools`: Contains tools for maintaining architectural integrity, including module architecture checks.
*   **Application Repositories:**
    *   `RegressionInsight` (formerly `release-regression-reporter`): Automates regression report generation.
    *   `StandupBot`: Manages standup reports.
    *   `BuildPilot`: Manages build processes.
    *   `CalMind`: Calendar and mind management tool.
    *   `MonitorIQ`: System monitoring and intelligence application.
    *   `XrayQC`: Quality control tool.
    *   `landing-page`: Main entry point for the platform.

### 1.4 Technology Stack
*   **Frontend:** React, Bootstrap, Custom CSS
*   **Backend:** FastAPI, Python
*   **Database:** SQLAlchemy, SQLite (local development), PostgreSQL (cloud deployment)

### 1.5 Development Practices
*   **Code Quality:**
    *   Python: Adheres to PEP 8, enforced by `black`, `isort`, and `flake8` via pre-commit hooks.
    *   JavaScript/React: Follows Airbnb style guide, formatted with `prettier`.
*   **Git Workflow:** Feature branching model; new work in feature branches merged via pull requests.
*   **Code Review:** All pull requests require at least one reviewer.
*   **CI/CD:** Each application has its own CI/CD pipeline defined in `.github/workflows`.
*   **Architectural Integrity:** Module architecture checks (pre-commit hooks) ensure adherence to architectural standards (e.g., applications do not implement their own auth/DB logic).

## 2. Gemini Guidelines

This section outlines the guidelines for interacting with the Gemini model within the OpalSuite project.

### 2.1 General Principles
*   **Clarity and Conciseness:** When formulating prompts, be clear, concise, and specific. Avoid ambiguity.
*   **Contextual Information:** Provide sufficient context for the model to understand the task. This includes relevant code snippets, error messages, or descriptions of the problem.
*   **Iterative Refinement:** If the initial response is not satisfactory, refine your prompt and try again. Break down complex tasks into smaller, more manageable steps.

### 2.2 Prompt Engineering Best Practices
*   **Specify Output Format:** If you require a specific output format (e.g., JSON, Python code, Markdown), explicitly state it in your prompt.
*   **Define Constraints:** Clearly define any constraints or limitations for the model's response (e.g., "limit the response to 3 sentences," "do not use external libraries").
*   **Provide Examples:** For complex tasks, providing a few examples of desired input-output pairs can significantly improve the model's performance.
*   **Role-Playing:** Sometimes, it's helpful to assign a role to the model (e.g., "Act as a senior Python developer," "You are a cybersecurity expert").

### 2.3 Use Cases for Gemini in OpalSuite
*   **Code Generation:** Generate code snippets, functions, or even entire modules based on a description.
*   **Code Explanation:** Explain complex code, identify potential issues, or suggest improvements.
*   **Debugging Assistance:** Help diagnose errors, suggest fixes, or provide debugging strategies.
*   **Documentation Generation:** Generate documentation for code, APIs, or project features.
*   **Test Case Generation:** Create unit tests or integration tests for existing code.
*   **Refactoring Suggestions:** Propose ways to refactor code for better readability, performance, or maintainability.

### 2.4 Ethical Considerations
*   **Bias Awareness:** Be aware that AI models can sometimes exhibit biases present in their training data. Review generated content critically.
*   **Security:** Do not include sensitive information (e.g., API keys, personal data) in your prompts.
*   **Verification:** Always verify the accuracy and correctness of generated code or information before using it in production.

### 2.5 Feedback
Your feedback on the quality and usefulness of Gemini's responses is highly valued. Please report any issues or suggestions to the development team.