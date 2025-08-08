#!/bin/bash
# Deploy the minimal App Engine proxy for the Cloud Run service

set -e

# Constants
PROJECT_ID=${1:-"phind-468207"}
CLOUD_RUN_URL=${2:-"https://phindllama-trading-system-u5d2kummnq-uc.a.run.app"}

echo "🚀 Deploying Minimal Proxy to Google App Engine"
echo "Project: ${PROJECT_ID}"
echo "Cloud Run URL: ${CLOUD_RUN_URL}"

# Make sure we're in the correct directory
cd minimal-proxy

# Update Cloud Run URL in app.yaml if provided
if [ "$CLOUD_RUN_URL" != "https://phindllama-trading-system-u5d2kummnq-uc.a.run.app" ]; then
    echo "✏️ Updating Cloud Run URL in app.yaml..."
    sed -i "s|CLOUD_RUN_URL: \"https://phindllama-trading-system-u5d2kummnq-uc.a.run.app\"|CLOUD_RUN_URL: \"$CLOUD_RUN_URL\"|g" app.yaml
fi

# Deploy to App Engine
echo "🌐 Deploying minimal proxy to App Engine..."
gcloud app deploy --project ${PROJECT_ID} --quiet

# Get App URL
APP_URL=$(gcloud app describe --project=${PROJECT_ID} --format='value(defaultHostname)')

echo "✅ Deployment complete!"
echo "🌐 Your App Engine Proxy URL: https://${APP_URL}"
echo "🔄 Proxy is now forwarding requests to Cloud Run service at: ${CLOUD_RUN_URL}"
