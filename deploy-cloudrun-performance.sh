#!/bin/bash

# Performance-optimized Cloud Run deployment script for PhindLlama
# This script configures Cloud Run for maximum performance and income generation

set -e

PROJECT_ID=${1:-"phind-468207"}
SERVICE_NAME="phindllama-trading-system"
REGION="us-central1"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "🚀 Deploying PhindLlama to Google Cloud Run (Performance-optimized)"
echo "Project: ${PROJECT_ID}"
echo "Service: ${SERVICE_NAME}"
echo "Region: ${REGION}"

# Build and push container image
echo "📦 Building container image..."
docker build -f Dockerfile.cloudrun -t ${IMAGE_NAME} .

echo "⬆️ Pushing to Google Container Registry..."
docker push ${IMAGE_NAME}

# Deploy to Cloud Run with performance-optimized settings
echo "🌊 Deploying to Cloud Run (performance-optimized)..."
gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME} \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --timeout 3600 \
    --concurrency 800 \
    --min-instances 1 \
    --max-instances 2 \
    --set-env-vars "ENVIRONMENT=production,DAILY_REVENUE_TARGET=500,PERFORMANCE_MODE=high" \
    --project ${PROJECT_ID}

# Get service URL
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} --region=${REGION} --format='value(status.url)')

echo "✅ Performance-optimized deployment complete!"
echo "🌐 Service URL: ${SERVICE_URL}"
echo "📊 Dashboard: ${SERVICE_URL}"
echo "💬 API: ${SERVICE_URL}/api/dashboard"

# Set up performance monitoring
echo "📈 Setting up performance monitoring..."
gcloud services enable monitoring.googleapis.com
gcloud services enable cloudprofiler.googleapis.com

# Create income tracking integration (placeholder - customize based on your actual income tracking logic)
echo "💰 Setting up income tracking..."
gcloud services enable pubsub.googleapis.com

# Create a topic for income events
gcloud pubsub topics create phindllama-income-events --project=${PROJECT_ID}

# Create a subscription for processing income events
gcloud pubsub subscriptions create phindllama-income-processing \
    --topic=phindllama-income-events \
    --project=${PROJECT_ID}

echo ""
echo "🔥 Your PhindLlama system is deployed with high-performance configuration!"
echo "💵 Revenue-focused optimizations applied:"
echo "  - Higher memory and CPU allocation for faster transaction processing"
echo "  - Multiple always-on instances to avoid cold starts and capture every opportunity"
echo "  - Scalable to handle high-volume trading periods"
echo "  - Performance monitoring enabled to identify bottlenecks"
echo ""
echo "🎯 Next steps to maximize revenue:"
echo "  - Set up automatic alerts for trade opportunities"
echo "  - Implement income tracking and reporting"
echo "  - Consider adding additional trading strategies"
echo "  - Monitor performance metrics to further optimize revenue generation"
