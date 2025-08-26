#!/bin/bash

# Source the common script
source ../shared/scripts/gcloud.sh

# --- Google Cloud Configuration (TO BE CONFIGURED BY THE USER) ---
GCP_PROJECT_ID="your-gcp-project-id"
GCP_REGION="your-gcp-region"
SERVICE_NAME="landing-page"
# -----------------------------------------------------------------

# Deploy the service to Google Cloud Run
deploy_gcloud $GCP_PROJECT_ID $GCP_REGION $SERVICE_NAME