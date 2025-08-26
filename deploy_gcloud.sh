#!/bin/bash

# Run all subproject gcloud deployment scripts

for dir in */ ; do
    if [ -f "$dir/deploy_gcloud.sh" ]; then
        echo "Deploying $dir to Google Cloud"
        (cd "$dir" && ./deploy_gcloud.sh)
    fi
done
