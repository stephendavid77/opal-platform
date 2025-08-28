#!/usr/bin/env python

"""
This script checks the import statements in each module to ensure that they follow the architectural rules.
"""

import ast
import os
import sys

# A dictionary that defines forbidden import patterns for each module type.
FORBIDDEN_IMPORTS = {
    "application": [
        "flask_jwt_extended",  # Custom auth library
        "django_rest_framework_jwt",  # Custom auth library
        "sqlalchemy",  # Should be handled by opal-database
        "bootstrap",  # Should be handled by opal-global-ui
        "react-bootstrap",  # Should be handled by opal-global-ui
        "some_custom_css_framework",  # Example of a forbidden CSS framework
    ],
    "shared-library": {
        # Shared libraries should not have their own auth/config/UI imports
        "opal-database": ["flask_jwt_extended", "bootstrap"],
        "opal-auth-backend": ["bootstrap"],
        "opal-shared-utils": ["flask_jwt_extended", "bootstrap"],
        "opal-global-ui": ["flask_jwt_extended"],
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


class ImportChecker(ast.NodeVisitor):
    def __init__(self, forbidden_imports):
        self.forbidden_imports = forbidden_imports
        self.violations = []

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name in self.forbidden_imports:
                self.violations.append(
                    f"Forbidden import: {alias.name} at line {node.lineno}"
                )
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module and node.module in self.forbidden_imports:
            self.violations.append(
                f"Forbidden import from: {node.module} at line {node.lineno}"
            )
        self.generic_visit(node)


def check_imports():
    print("Checking imports...")
    project_path = os.getcwd()  # Assuming the script is run from the project root
    project_type = get_project_type(project_path)

    violations = []

    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    try:
                        tree = ast.parse(f.read(), filename=file_path)
                        checker = ImportChecker(FORBIDDEN_IMPORTS.get(project_type, []))
                        checker.visit(tree)
                        violations.extend(checker.violations)
                    except SyntaxError as e:
                        print(f"Error parsing {file_path}: {e}")

    if violations:
        print("Import check failed:")
        for violation in violations:
            print(f"- {violation}")
        sys.exit(1)
    else:
        print("Imports check passed.")
        sys.exit(0)


if __name__ == "__main__":
    check_imports()
