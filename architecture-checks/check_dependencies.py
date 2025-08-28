#!/usr/bin/env python

"""
This script checks the dependencies of each module to ensure that they follow the architectural rules.
"""

import os
import sys

import toml

# A dictionary that defines the allowed dependencies for each module type.
# This is a simplified example. In a real scenario, this would be more comprehensive.
ALLOWED_DEPENDENCIES = {
    "application": [
        "opal-auth-backend",
        "opal-shared-utils",
        "opal-global-ui",
        "opal-auth-frontend",
    ],
    "shared-library": {
        "opal-database": [],
        "opal-auth-backend": ["opal-database"],
        "opal-shared-utils": [],
        "opal-global-ui": [],
        "opal-auth-frontend": ["opal-global-ui"],
    },
}

# A dictionary that defines forbidden dependencies for each module type.
FORBIDDEN_DEPENDENCIES = {
    "application": [
        "flask-jwt-extended",  # Custom auth library
        "django-rest-framework-jwt",  # Custom auth library
        "python-jose",  # Should be handled by opal-auth-backend
        "passlib",  # Should be handled by opal-auth-backend
        "sqlalchemy",  # Should be handled by opal-database
        "bootstrap",  # Should be handled by opal-global-ui
        "react-bootstrap",  # Should be handled by opal-global-ui
    ],
    "shared-library": {
        # Shared libraries should not have their own auth/config/UI dependencies
        "opal-database": ["flask-jwt-extended", "bootstrap"],
        "opal-auth-backend": ["bootstrap"],
        "opal-shared-utils": ["flask-jwt-extended", "bootstrap"],
        "opal-global-ui": ["flask-jwt-extended"],
        "opal-auth-frontend": [],
    },
}


def get_project_type(project_path):
    # This is a placeholder. In a real scenario, you might infer this from project structure or a config file.
    if (
        "opal-auth-backend" in project_path
        or "opal-database" in project_path
        or "opal-shared-utils" in project_path
        or "opal-global-ui" in project_path
        or "opal-auth-frontend" in project_path
    ):
        return "shared-library"
    return "application"


def check_dependencies():
    print("Checking dependencies...")
    project_path = os.getcwd()  # Assuming the script is run from the project root
    project_type = get_project_type(project_path)

    violations = []

    # Check pyproject.toml for dependencies
    pyproject_path = os.path.join(project_path, "pyproject.toml")
    if os.path.exists(pyproject_path):
        with open(pyproject_path, "r") as f:
            pyproject_data = toml.load(f)
            project_dependencies = pyproject_data.get("project", {}).get(
                "dependencies", []
            )

            for forbidden_dep in FORBIDDEN_DEPENDENCIES.get(project_type, []):
                if forbidden_dep in " ".join(project_dependencies):
                    violations.append(
                        f"Forbidden dependency found in pyproject.toml: {forbidden_dep}"
                    )

    # Check requirements.txt for dependencies
    requirements_path = os.path.join(project_path, "requirements.txt")
    if os.path.exists(requirements_path):
        with open(requirements_path, "r") as f:
            requirements_content = f.read()
            for forbidden_dep in FORBIDDEN_DEPENDENCIES.get(project_type, []):
                if forbidden_dep in requirements_content:
                    violations.append(
                        f"Forbidden dependency found in requirements.txt: {forbidden_dep}"
                    )

    if violations:
        print("Dependency check failed:")
        for violation in violations:
            print(f"- {violation}")
        sys.exit(1)
    else:
        print("Dependency check passed.")
        sys.exit(0)


if __name__ == "__main__":
    check_dependencies()
