# CI/CD Rules

This section contains the CI/CD rules and configurations for the OpalSuite project.

## CI/CD Pipeline Overview

Each application in the OpalSuite ecosystem has its own CI/CD pipeline. The pipelines are responsible for building, testing, and deploying the applications.

The CI/CD pipelines are defined in the `.github/workflows` directory of each application's repository.

## Adding a New Application to the CI/CD System

To add a new application to the CI/CD system, you will need to:

1.  Create a new repository for the application.
2.  Add a `.github/workflows` directory to the repository.
3.  Create a new workflow file in the `.github/workflows` directory that defines the build, test, and deployment steps for the application.
4.  The workflow should be configured to be triggered on pushes to the `main` branch and on pull requests.
