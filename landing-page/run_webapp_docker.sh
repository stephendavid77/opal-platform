#!/bin/bash

# Source the common script
source ../shared/scripts/docker.sh

# Build and run the docker container
build_and_run_docker "landing-page" "landing-page" "3000:80"