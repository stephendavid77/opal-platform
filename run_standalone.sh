#!/bin/bash

# Run all subproject standalone scripts in the background

for dir in */ ; do
    if [ -f "$dir/run_standalone.sh" ]; then
        echo "Starting standalone script for $dir"
        (cd "$dir" && ./run_standalone.sh) &
    fi
done

# Wait for all background processes to finish
wait