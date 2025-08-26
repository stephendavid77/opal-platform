#!/bin/bash

# This script handles prerequisites for database initialization.

# Ensure the current directory has write permissions
# This assumes the script is run from the project root where opal_suite.db will be created.
chmod u+w . || { echo "Error: Cannot set write permissions for current directory."; exit 1; }

# Install Python dependencies
echo "Installing root and auth_service Python dependencies..."
pip install -r requirements.txt || { echo "Error: Failed to install root dependencies."; exit 1; }
pip install -r auth_service/requirements.txt || { echo "Error: Failed to install auth_service dependencies."; exit 1; }

# Check for 'fuser' command (used in run_standalone.sh for aggressive killing)
if ! command -v fuser &> /dev/null
then
    echo "Warning: 'fuser' command not found. Process killing by port might be less effective."
    echo "Please install 'fuser' (e.g., 'sudo apt-get install psmisc' on Debian/Ubuntu, 'brew install psutils' on macOS)."
fi

echo "Database prerequisites handled successfully."
