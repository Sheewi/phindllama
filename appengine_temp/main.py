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
