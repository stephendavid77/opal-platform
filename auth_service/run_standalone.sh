#!/bin/bash

# Source the common script
source ../shared/scripts/standalone.sh

# Kill any process running on port 8000
kill_process_on_port 8000

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn main:app --host 0.0.0.0 --port 8000