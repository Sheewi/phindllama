#!/bin/bash

# Cost-optimized Cloud Run deployment script for PhindLlama
# This script configures Cloud Run to make efficient use of your credits

set -e

PROJECT_ID=${1:-"phind-468207"}
SERVICE_NAME="phindllama-trading-system"
REGION="us-central1"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "🚀 Deploying PhindLlama to Google Cloud Run (Cost-optimized)"
echo "Project: ${PROJECT_ID}"
echo "Service: ${SERVICE_NAME}"
echo "Region: ${REGION}"

# Build and push container image
echo "📦 Building container image..."
docker build -f Dockerfile.cloudrun -t ${IMAGE_NAME} .

echo "⬆️ Pushing to Google Container Registry..."
docker push ${IMAGE_NAME}

# Deploy to Cloud Run with cost-optimized settings
echo "🌊 Deploying to Cloud Run (cost-optimized)..."
gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME} \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --memory 512Mi \     # Reduced memory allocation
    --cpu 1 \            # Reduced CPU allocation
    --timeout 3600 \
    --concurrency 80 \   # Reduced concurrency for better resource utilization
    --min-instances 0 \  # Scale to zero when not in use to save credits
    --max-instances 3 \  # Reduced max instances
    --set-env-vars "ENVIRONMENT=production,DAILY_REVENUE_TARGET=200,OPTIMIZE_FOR_CREDITS=true" \
    --project ${PROJECT_ID}

# Get service URL
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} --region=${REGION} --format='value(status.url)')

echo "✅ Cost-optimized deployment complete!"
echo "🌐 Service URL: ${SERVICE_URL}"
echo "📊 Dashboard: ${SERVICE_URL}"
echo "💬 API: ${SERVICE_URL}/api/dashboard"

# Set up cost monitoring
echo "💰 Setting up cost monitoring..."
gcloud services enable monitoring.googleapis.com

# Create a budget alert for your Cloud Run service to monitor credit usage
gcloud billing budgets create \
    --billing-account=$(gcloud billing projects describe ${PROJECT_ID} --format="value(billingAccountName)") \
    --display-name="PhindLlama Cloud Run Budget" \
    --budget-amount=100USD \
    --threshold-rules=threshold-percent=0.5 \
    --threshold-rules=threshold-percent=0.9 \
    --services=services/run.googleapis.com

echo "💡 Cost-saving tips:"
echo "  - Your service will now scale to zero when not in use"
echo "  - Memory and CPU have been optimized for credit efficiency"
echo "  - You've set up budget alerts to monitor credit usage"
echo ""
echo "🎯 Next steps for credit optimization:"
echo "  - Monitor usage patterns with Google Cloud Monitoring"
echo "  - Set up scheduled scaling with Cloud Scheduler if needed"
echo "  - Consider implementing request batching for better efficiency"
