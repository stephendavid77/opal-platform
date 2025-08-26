#!/bin/bash

# Run all subproject standalone scripts in the background, or a specific one in the foreground

TARGET_SUBPROJECT="$1"

if [ -z "$TARGET_SUBPROJECT" ]; then
    # No specific subproject provided, run all in background
    echo "Starting all subprojects in standalone mode (background)."
    for dir in */ ; do
        if [ -f "$dir/run_standalone.sh" ]; then
            echo "Starting standalone script for $dir"
            (cd "$dir" && ./run_standalone.sh) &
        fi
    done
    wait
else
    # Specific subproject provided, run it in foreground
    if [ -d "$TARGET_SUBPROJECT" ] && [ -f "$TARGET_SUBPROJECT/run_standalone.sh" ]; then
        echo "Starting $TARGET_SUBPROJECT in standalone mode (foreground)."
        (cd "$TARGET_SUBPROJECT" && ./run_standalone.sh)
    else
        echo "Error: Subproject '$TARGET_SUBPROJECT' not found or does not have a run_standalone.sh script."
        exit 1
    fi
fi
