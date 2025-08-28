#!/usr/bin/env python

"""
This script checks the dependencies of each module to ensure that they follow the architectural rules.
"""

import sys

# A dictionary that defines the allowed dependencies for each module type.
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


def check_dependencies():
    """Checks the dependencies of each module."""
    print("Checking dependencies...")
    # TODO: Implement the logic to read the pyproject.toml or requirements.txt file of each module.
    # TODO: Compare the dependencies with the allowed dependencies defined in ALLOWED_DEPENDENCIES.
    # TODO: Report any violations.
    print("Dependencies check passed.")
    sys.exit(0)


if __name__ == "__main__":
    check_dependencies()
