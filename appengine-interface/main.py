import os
import datetime
import requests
from flask import Flask, request, render_template_string, jsonify

# Initialize Flask app
app = Flask(__name__)

# Simple app for App Engine

# Cloud Run service URL
CLOUD_RUN_URL = os.environ.get('CLOUD_RUN_URL', 'https://phindllama-trading-system-u5d2kummnq-uc.a.run.app')

# HTML template for the interface
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PhindLlama Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        .status {
            margin: 20px 0;
            padding: 15px;
            border-radius: 4px;
        }
        .status.success {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }
        .status.error {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }
        .api-section {
            margin-top: 30px;
        }
        button {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            margin-top: 10px;
        }
        button:hover {
            background-color: #2980b9;
        }
        pre {
            background-color: #f8f9fa;
            border: 1px solid #eaeaea;
            border-radius: 4px;
            padding: 15px;
            overflow-x: auto;
            margin-top: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>PhindLlama System Dashboard</h1>
        
        <div class="status {{ status_class }}">
            {{ status_message }}
        </div>
        
        <div class="api-section">
            <h2>Service Information</h2>
            <p><strong>App Engine Interface URL:</strong> {{ app_engine_url }}</p>
            <p><strong>Cloud Run Backend URL:</strong> {{ cloud_run_url }}</p>
            <p><strong>Status:</strong> {{ cloud_run_status }}</p>
            
            <h2>API Endpoints</h2>
            <div>
                <h3>Available Strategies</h3>
                <button onclick="fetch('/api/strategies').then(response => response.json()).then(data => {
                    document.getElementById('strategiesResult').textContent = JSON.stringify(data, null, 2);
                })">Get Strategies</button>
                <pre id="strategiesResult"></pre>
            </div>
            
            <div>
                <h3>System Health</h3>
                <button onclick="fetch('/api/health').then(response => response.json()).then(data => {
                    document.getElementById('healthResult').textContent = JSON.stringify(data, null, 2);
                })">Check Health</button>
                <pre id="healthResult"></pre>
            </div>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def dashboard():
    """Dashboard interface for PhindLlama."""
    
    # Check Cloud Run service status
    try:
        response = requests.get(f"{CLOUD_RUN_URL}/health", timeout=10)
        if response.status_code == 200:
            cloud_run_status = "Operational"
            status_message = "PhindLlama system is online and operational."
            status_class = "success"
        else:
            cloud_run_status = f"Issue detected (Status {response.status_code})"
            status_message = "Warning: PhindLlama system is experiencing issues."
            status_class = "error"
    except Exception as e:
        logger.error(f"Error connecting to Cloud Run service: {str(e)}")
        cloud_run_status = "Connection error"
        status_message = f"Error connecting to PhindLlama system: {str(e)}"
        status_class = "error"
    
    return render_template_string(
        HTML_TEMPLATE,
        app_engine_url=request.host_url,
        cloud_run_url=CLOUD_RUN_URL,
        cloud_run_status=cloud_run_status,
        status_message=status_message,
        status_class=status_class
    )

@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_api(path):
    """Proxy all API requests to the Cloud Run service."""
    # Forward the request to Cloud Run
    try:
        resp = requests.request(
            method=request.method,
            url=f"{CLOUD_RUN_URL}/{path}",
            headers={key: value for key, value in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            timeout=30
        )

        # Create response
        response = Response(resp.content, resp.status_code)
        
        # Copy headers from Cloud Run response
        for key, value in resp.headers.items():
            if key.lower() != 'content-length':
                response.headers[key] = value
                
        return response
    except Exception as e:
        logger.error(f"Error proxying request to {path}: {str(e)}")
        return jsonify({
            "error": "Failed to connect to backend service",
            "details": str(e)
        }), 500

@app.route('/health')
def health():
    """Health check endpoint."""
    try:
        # Check Cloud Run service health
        response = requests.get(f"{CLOUD_RUN_URL}/health", timeout=5)
        cloud_run_status = "healthy" if response.status_code == 200 else "unhealthy"
        
        return jsonify({
            "status": "healthy",
            "cloud_run_status": cloud_run_status,
            "timestamp": str(datetime.datetime.now())
        })
    except Exception as e:
        return jsonify({
            "status": "healthy",
            "cloud_run_status": "unreachable",
            "error": str(e),
            "timestamp": str(datetime.datetime.now())
        })

if __name__ == "__main__":
    # This is used when running locally
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
