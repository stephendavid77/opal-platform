#!/bin/bash

deploy_gcloud() {
    if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
        echo "Usage: deploy_gcloud <gcp_project_id> <gcp_region> <service_name>"
        return 1
    fi

    local gcp_project_id=$1
    local gcp_region=$2
    local service_name=$3

    docker build -t gcr.io/$gcp_project_id/$service_name .

    docker push gcr.io/$gcp_project_id/$service_name

    gcloud run deploy $service_name \
      --image gcr.io/$gcp_project_id/$service_name \
      --platform managed \
      --region $gcp_region \
      --allow-unauthenticated
}
