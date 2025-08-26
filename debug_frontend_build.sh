#!/bin/bash

# Navigate to the shared/frontend_base directory
cd shared/frontend_base || { echo "Error: shared/frontend_base directory not found."; exit 1; }

echo "Starting Rollup build with Node.js debugger attached."
echo "Open Chrome and go to chrome://inspect to connect to the debugger."

# Run the build command with Node.js debugging flags
npm run build:lib