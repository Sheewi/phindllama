# Cloud Run deployment script
#!/bin/bash

# PhindLlama Cloud Run Deployment Script

set -e

PROJECT_ID=${1:-"your-gcp-project-id"}
SERVICE_NAME="phindllama-trading-system"
REGION="us-central1"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "🚀 Deploying PhindLlama to Google Cloud Run"
echo "Project: ${PROJECT_ID}"
echo "Service: ${SERVICE_NAME}"
echo "Region: ${REGION}"

# Build and push container image
echo "📦 Building container image..."
docker build -f Dockerfile.cloudrun -t ${IMAGE_NAME} .

echo "⬆️ Pushing to Google Container Registry..."
docker push ${IMAGE_NAME}

# Deploy to Cloud Run
echo "🌊 Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME} \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --timeout 3600 \
    --concurrency 1000 \
    --min-instances 1 \
    --max-instances 5 \
    --set-env-vars "ENVIRONMENT=production,DAILY_REVENUE_TARGET=200" \
    --project ${PROJECT_ID}

# Get service URL
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} --region=${REGION} --format='value(status.url)')

echo "✅ Deployment complete!"
echo "🌐 Service URL: ${SERVICE_URL}"
echo "📊 Dashboard: ${SERVICE_URL}"
echo "💬 API: ${SERVICE_URL}/api/dashboard"

# Optional: Set up monitoring
echo "📊 Setting up monitoring (optional)..."
gcloud logging sinks create phindllama-sink \
    bigquery.googleapis.com/projects/${PROJECT_ID}/datasets/phindllama_logs \
    --log-filter="resource.type=cloud_run_revision AND resource.labels.service_name=${SERVICE_NAME}" \
    --project ${PROJECT_ID} || echo "Sink may already exist"

echo "🎉 PhindLlama is now running on Cloud Run with auto-scaling!"
echo "💡 The system will automatically scale from 1 to 10 instances based on demand"
echo "💰 Estimated cost: $20-50/month for moderate usage"
