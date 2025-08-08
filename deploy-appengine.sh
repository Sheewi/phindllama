#!/bin/bash
# App Engine Deployment Script

set -e

# Constants
PROJECT_ID=${1:-"phind-468207"}
REGION="us-central"
SERVICE_NAME="phindllama-app"

echo "🚀 Deploying PhindLlama to Google App Engine"
echo "Project: ${PROJECT_ID}"
echo "Region: ${REGION}"

# Make sure App Engine API is enabled
echo "✅ Ensuring App Engine API is enabled..."
gcloud services enable appengine.googleapis.com --project ${PROJECT_ID}

# Creating working directory
echo "📁 Creating deployment directory..."
mkdir -p appengine_temp
cd appengine_temp

# Creating simple application files
echo "📝 Creating application files..."

# Create app.yaml
cat > app.yaml << EOL
runtime: python39
instance_class: F2
entrypoint: gunicorn -b :$PORT main:app

basic_scaling:
  max_instances: 5
  idle_timeout: 10m

handlers:
- url: /.*
  script: auto
  secure: always

env_variables:
  ENVIRONMENT: "production"
  LOG_LEVEL: "INFO"
EOL

# Create main.py
cat > main.py << EOL
import os
from flask import Flask, jsonify
import logging

# Initialize Flask app
app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    """Home endpoint for PhindLlama App Engine deployment."""
    logger.info("Home endpoint accessed")
    return jsonify({
        "status": "success",
        "message": "PhindLlama API is running on Google App Engine",
        "service": "PhindLlama Trading System",
        "version": "1.0.0"
    })

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})

@app.route('/strategies')
def strategies():
    """Get available strategies."""
    return jsonify({
        "available_strategies": [
            {
                "name": "market_analysis",
                "type": "analysis",
                "priority": 1,
                "status": "active"
            },
            {
                "name": "opportunity_detection", 
                "type": "detection",
                "priority": 2,
                "status": "active"
            },
            {
                "name": "risk_management",
                "type": "monitoring",
                "priority": 3,
                "status": "active"
            }
        ]
    })

if __name__ == "__main__":
    # This is used when running locally
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
EOL

# Create requirements.txt
cat > requirements.txt << EOL
Flask==2.0.1
gunicorn==20.1.0
Werkzeug==2.0.1
EOL

# Deploy to App Engine
echo "🌐 Deploying to App Engine..."
gcloud app deploy --project ${PROJECT_ID} --quiet

# Get App URL
APP_URL=$(gcloud app describe --project=${PROJECT_ID} --format='value(defaultHostname)')

echo "✅ Deployment complete!"
echo "🌐 Your App Engine URL: https://${APP_URL}"
echo "📊 Dashboard: https://console.cloud.google.com/appengine?project=${PROJECT_ID}"

# Clean up
echo "🧹 Cleaning up..."
cd ..
# Uncomment to remove temp directory after deployment
# rm -rf appengine_temp

echo "🎉 PhindLlama is now running on App Engine with auto-scaling!"
