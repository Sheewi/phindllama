#!/bin/bash

# Cloud Run Quota Request and Scaling Script for PhindLlama
# This script updates your Cloud Run deployment and requests higher quotas for scaling

set -e

PROJECT_ID=${1:-"phind-468207"}
SERVICE_NAME="phindllama-trading-system"
REGION="us-central1"

echo "🚀 Updating and scaling PhindLlama on Cloud Run"
echo "Project: ${PROJECT_ID}"
echo "Service: ${SERVICE_NAME}"
echo "Region: ${REGION}"

# Request quota increase using gcloud beta command
echo "📝 Generating quota increase request for Cloud Run..."

# Get current limits
CURRENT_INSTANCE_LIMIT=$(gcloud run services describe ${SERVICE_NAME} --region=${REGION} --project=${PROJECT_ID} --format='value(spec.template.metadata.annotations."autoscaling.knative.dev/maxScale")')
CURRENT_CPU_LIMIT=$(gcloud run services describe ${SERVICE_NAME} --region=${REGION} --project=${PROJECT_ID} --format='value(spec.template.containerConcurrency)')

echo "Current max instances: ${CURRENT_INSTANCE_LIMIT}"

# Generate quota increase request with justification
echo ""
echo "--------------- QUOTA INCREASE REQUEST ---------------"
echo ""
echo "Please submit this request in the Google Cloud Console:"
echo "https://console.cloud.google.com/iam-admin/quotas?project=${PROJECT_ID}"
echo ""
echo "Request details:"
echo "  - Service: Cloud Run"
echo "  - Region: ${REGION}"
echo "  - Quota: MaxInstancesPerProjectRegion"
echo "  - Current limit: ${CURRENT_INSTANCE_LIMIT}"
echo "  - Requested limit: 20"
echo ""
echo "Justification:"
echo "The PhindLlama trading system requires increased capacity to handle"
echo "higher trading volumes during market peaks. Our system generates revenue"
echo "based on trading opportunities, and the increased quota will allow us to"
echo "capture more of these opportunities, directly increasing our ROI."
echo "Our current performance metrics show that we've been consistently"
echo "hitting our max instance limit during peak times, indicating growth"
echo "potential that's currently being constrained."
echo ""
echo "----------------------------------------------------"

# Set a reminder in 7 days to check quota status
REMIND_DATE=$(date -d "+7 days" "+%Y-%m-%d")

echo ""
echo "While waiting for quota approval, optimize your current resources:"
echo ""
echo "1. Implement better request batching"
echo "   - Group similar operations together"
echo "   - Process multiple trades in single requests"
echo ""
echo "2. Add request prioritization"
echo "   - Ensure high-profit opportunities get processed first"
echo "   - Defer lower-priority operations during peak loads"
echo ""
echo "3. Schedule non-critical tasks during low-usage periods"
echo "   - Move reporting and analysis to off-peak hours"
echo "   - Use Cloud Scheduler for time-distribution"
echo ""
echo "4. Monitor performance with Cloud Monitoring"
echo "   - Track CPU and memory usage patterns"
echo "   - Identify optimization opportunities"
echo ""

echo "📅 Reminder: Check quota increase status on ${REMIND_DATE}"
echo "    Calendar link: https://calendar.google.com/calendar/event?action=TEMPLATE&text=Check%20Cloud%20Run%20Quota%20Status&dates=${REMIND_DATE}/${REMIND_DATE}&details=Check%20the%20status%20of%20your%20Cloud%20Run%20quota%20increase%20request%20for%20project%20${PROJECT_ID}"

# Update Cloud Run service with current maximum performance settings
echo ""
echo "🔄 Updating Cloud Run service with optimized settings..."
gcloud run services update ${SERVICE_NAME} \
  --region=${REGION} \
  --project=${PROJECT_ID} \
  --memory=2Gi \
  --cpu=2 \
  --concurrency=800 \
  --min-instances=1 \
  --max-instances=${CURRENT_INSTANCE_LIMIT} \
  --set-env-vars="ENVIRONMENT=production,DAILY_REVENUE_TARGET=500,PROFIT_TRACKING_ENABLED=true,SCALING_STRATEGY=aggressive"

echo ""
echo "✅ Service updated with optimized settings!"
echo "🌐 Service URL: https://phindllama-trading-system-u5d2kummnq-uc.a.run.app"
echo ""
echo "📈 Next steps to maximize income while waiting for quota increase:"
echo "  1. Visit your dashboard to monitor income tracking"
echo "  2. Optimize your trading strategies based on performance data"
echo "  3. Submit the quota increase request using the details above"
