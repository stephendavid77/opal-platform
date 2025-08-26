#!/bin/bash

# Source the common script
source ../shared/scripts/docker.sh

# Check if the shared database exists, and create tables if not
DB_PATH="./shared/database_base/data/opal_suite.db"
if [ ! -f "$DB_PATH" ]; then
    echo "Shared database not found. Creating tables..."
    ./scripts/create_db_tables.sh
else
    echo "Shared database already exists. Skipping table creation."
fi

# Build and run the docker container
build_and_run_docker "auth_service" "auth_service" "8000:8000"