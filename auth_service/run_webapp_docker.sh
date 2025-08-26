#!/bin/bash

# Source the common script
source ../shared/scripts/docker.sh

# Build and run the docker container
build_and_run_docker "auth_service" "auth_service" "8000:8000"