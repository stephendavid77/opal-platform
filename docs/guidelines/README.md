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

OpalSuite utilizes the `pre-commit` framework to enforce code quality, style, and architectural standards across all modules. Global checks are defined in the `opal-dev-tools` repository, and each project's `.pre-commit-config.yaml` references these global hooks.

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

To update the pre-commit hooks to their latest versions (as defined in `opal-dev-tools`):

```bash
pre-commit autoupdate
```

### Overriding or Customizing Hooks

Each project's `.pre-commit-config.yaml` includes all global hooks from `opal-dev-tools`. If you need to override or customize a specific hook for a particular project, you can do so by redefining the hook in the project's `.pre-commit-config.yaml` *after* the `opal-dev-tools` repository definition.

**Example: Disabling a specific hook (e.g., `mypy`) for a project:**

```yaml
repos:
  - repo: https://github.com/stephendavid77/opal-dev-tools
    rev: main # Or a specific commit hash/tag
    hooks:
      - id: trailing-whitespace
      # ... other global hooks ...
      - id: mypy # This hook is included from opal-dev-tools

  # Project-specific overrides
  - repo: local
    hooks:
      - id: mypy # Redefine mypy to disable it for this project
        enabled: false
```

**Example: Adding a project-specific hook:**

```yaml
repos:
  - repo: https://github.com/stephendavid77/opal-dev-tools
    rev: main # Or a specific commit hash/tag
    hooks:
      - id: trailing-whitespace
      # ... other global hooks ...

  # Project-specific additions
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: check-json # Example: Add a JSON check only for this project
```
