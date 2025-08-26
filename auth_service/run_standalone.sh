#!/bin/bash

# Navigate to the project root directory
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")
cd "$PROJECT_ROOT" || exit

# Source the common script
source shared/scripts/standalone.sh

# Add the project root to PYTHONPATH
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

# Check if the shared database exists, and create tables if not
DB_PATH="./shared/database_base/data/opal_suite.db"
if [ ! -f "$DB_PATH" ]; then
    echo "Shared database not found. Creating tables..."
    ./scripts/create_db_tables.sh
else
    echo "Shared database already exists. Skipping table creation."
fi

# Kill any existing process using port 8000
PID=$(lsof -t -i:8000)
if [ -n "$PID" ]; then
    echo "Killing process $PID on port 8000..."
    kill -9 "$PID"
    sleep 1
fi

# Install dependencies
pip install -r requirements.txt

# Run the application from the project root
# This ensures 'auth_service' is treated as a package
uvicorn auth_service.main:app --host 0.0.0.0 --port 8000 --log-level debug