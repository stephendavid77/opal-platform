#!/bin/bash

# Source the common script
source ../shared/scripts/standalone.sh

# Kill any process running on port 8000
kill_process_on_port 8000

# Install dependencies
pip install -r requirements.txt

# Run the application from the project root
# This ensures 'auth_service' is treated as a package
(cd .. && uvicorn auth_service.main:app --host 0.0.0.0 --port 8000)
