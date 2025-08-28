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

## Pre-commit Hooks Setup

OpalSuite utilizes the `pre-commit` framework to enforce code quality, style, and architectural standards across all modules. Global checks are defined in the `opal-dev-tools` repository within its `.pre-commit-hooks.yaml` file. Each project's `.pre-commit-config.yaml` references these global hooks.

### Installation

To set up the pre-commit hooks for any module in the OpalSuite ecosystem:

1.  **Navigate to the module's root directory:**
    ```bash
    cd /path/to/your/module
    ```
2.  **Install the pre-commit hooks:**
    ```bash
    pre-commit install
    ```
    This command sets up the Git hooks in your local repository. The first time you commit after installation, `pre-commit` will download and install the necessary tools.

### Validating Existing Code

To run all configured hooks against all files in your repository (useful for validating existing code or after updating hook configurations):

```bash
pre-commit run --all-files
```

### Updating Hooks

To update the pre-commit hooks to their latest versions (as defined by the commit hash in `opal-dev-tools`):

```bash
pre-commit autoupdate
```

### Overriding or Customizing Hooks

Each project's `.pre-commit-config.yaml` includes all global hooks from `opal-dev-tools`. If you need to override or customize a specific hook for a particular project, you can do so by defining additional hooks in the project's `.pre-commit-config.yaml` using `repo: local`.

**Example: Project's `.pre-commit-config.yaml` referencing `opal-dev-tools`:**

```yaml
repos:
  - repo: https://github.com/stephendavid77/opal-dev-tools
    rev: 4aef5433195fa4c3fc91d91c996a63b54560103d # Use a specific commit hash for production stability
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: black
      - id: isort
      - id: flake8
      - id: mypy
      - id: bandit
      - id: eslint
      - id: prettier
      - id: check-dependencies
      - id: check-imports
      - id: check-structure
      - id: pytest

  # Project-specific overrides or additions (using repo: local)
  - repo: local
    hooks:
      - id: mypy # Example: Override mypy to skip it for this project
        name: Mypy Type Checker (Project Override)
        entry: mypy
        language: python
        enabled: false # Disable this hook for this project
```

### How to Add a New Module to the Ecosystem

When adding a new module to the OpalSuite ecosystem, follow these steps to integrate it with the pre-commit framework:

1.  **Create the new module's repository.**
2.  **Add a `.pre-commit-config.yaml` file** to the root of the new module's repository with the content shown in the "Example: Project's `.pre-commit-config.yaml`" above. Ensure you use the latest stable commit hash for `opal-dev-tools`.
3.  **Run `pre-commit install`** in the new module's root directory.
4.  **Run `pre-commit run --all-files`** to validate existing code in the new module.
