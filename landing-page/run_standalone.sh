#!/bin/bash

# Source the common script
source ../shared/scripts/standalone.sh

# Kill any process running on port 3000
kill_process_on_port 3000

# Install dependencies
npm install

# Run the application
npm start