# OpalSuite Shared Frontend Base (Design System)

## Overview

The `shared/frontend_base/` module serves as `OpalSuite`'s centralized design system and shared UI component library. Its primary goal is to ensure a consistent look and feel across all React-based sub-applications within the monorepo. By providing reusable components and a unified styling approach, it accelerates frontend development, reduces design inconsistencies, and simplifies maintenance.

## Architecture

### 1. React Project Setup

*   **Foundation:** This module is initialized as a standard React project, providing a familiar development environment and build tooling.
*   **Core Imports:** The `src/index.js` file is configured to centrally import the chosen CSS framework (Bootstrap) and any custom `OpalSuite` global styles.

### 2. Styling and Theming

*   **Bootstrap Integration:** Bootstrap is integrated as the primary CSS framework, providing a robust and responsive grid system, pre-built components, and utility classes.
*   **Custom Styles (`src/styles/main.css`):** This file is dedicated to `OpalSuite`'s custom branding, including color palettes, typography, spacing, and overrides to Bootstrap defaults. This ensures a unique and consistent visual identity.

### 3. Reusable UI Components

*   **Component Library:** This module will house a library of reusable React UI components (e.g., `OpalButton`, `OpalCard`, `OpalNavbar`). These components will wrap standard HTML elements or React-Bootstrap components, applying `OpalSuite`'s custom styling and design principles.
*   **Export Mechanism:** Components will be exported from this module, allowing sub-applications to easily import and use them.

## How it Fits into OpalSuite

*   **Visual Consistency:** Guarantees a unified user experience across all applications, making the entire suite feel cohesive.
*   **Accelerated Development:** Frontend developers can leverage pre-built, styled components, significantly speeding up UI development.
*   **Simplified Maintenance:** Changes to the design system or core styling can be made in one place and propagated across all applications.
*   **Brand Identity:** Reinforces the `OpalSuite` brand through consistent visual elements.

## Getting Started (Development)

1.  **Install Dependencies:** Navigate to `OpalSuite/shared/frontend_base/` and install Node.js dependencies:
    ```bash
    npm install
    ```
2.  **Develop Components:** Create and modify React components within `src/components/` (or similar) and define custom styles in `src/styles/main.css`.
3.  **Integrate into Sub-Applications:**
    *   In each React-based sub-application's `frontend/` directory, ensure `bootstrap` and `react-bootstrap` are installed.
    *   Configure the sub-application's build system (e.g., `craco` for Create React App) to resolve imports from `OpalSuite/shared/frontend_base/`.
    *   Import the shared styles and components into the sub-application's `index.js` or `App.js`.

## Future Enhancements

*   **Storybook Integration:** Use Storybook to develop, document, and test UI components in isolation.
*   **Theming System:** Implement a more advanced theming system for dynamic theme switching.
*   **Accessibility (A11y):** Ensure all reusable components adhere to accessibility best practices.
*   **Automated Visual Regression Testing:** Integrate tools to automatically detect unintended visual changes.
