#!/bin/bash

# Run all subproject standalone scripts in the background

for dir in */ ; do
    if [ -f "$dir/run_webapp_nodocker.sh" ]; then
        echo "Starting non-docker script for $dir"
        (cd "$dir" && ./run_webapp_nodocker.sh) &
    fi
done

# Wait for all background processes to finish
wait
