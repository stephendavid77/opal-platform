# Development Guidelines

This section contains the development guidelines, style guides, and best practices for the OpalSuite project.

## Coding Standards

All Python code should follow the [PEP 8 style guide](https://www.python.org/dev/peps/pep-0008/). We use `black` for code formatting and `flake8` for linting. These are enforced by pre-commit hooks.

All JavaScript and React code should follow the [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript). We use `prettier` for code formatting.

## Git Workflow

We use a a feature branching workflow. All new work should be done in a feature branch and then merged into the `main` branch via a pull request.

Branch names should be descriptive and follow the format `<type>/<short-description>`, where `<type>` is one of `feat`, `fix`, `docs`, `style`, `refactor`, `test`, or `chore`.

## Code Review Process

All pull requests must be reviewed and approved by at least one other developer before being merged. The reviewer should check for code quality, correctness, and adherence to the guidelines.
