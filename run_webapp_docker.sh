#!/bin/bash

# Run all subproject docker scripts in the background

for dir in */ ; do
    if [ -f "$dir/run_webapp_docker.sh" ]; then
        echo "Starting docker script for $dir"
        (cd "$dir" && ./run_webapp_docker.sh) &
    fi
done

# Wait for all background processes to finish
wait