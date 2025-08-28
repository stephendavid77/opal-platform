# Architecture Checks

This directory contains scripts that perform architectural checks on the modules in the OpalSuite ecosystem.

## Checks

*   `check_dependencies.py`: Checks the dependencies of each module to ensure that they follow the architectural rules.
*   `check_imports.py`: Checks the import statements in each module to ensure that they follow the architectural rules.
*   `check_structure.py`: Checks the directory structure of each module to ensure that it follows the prescribed structure.

## Usage

These checks are intended to be run as pre-commit hooks. They can also be run manually from the command line.
