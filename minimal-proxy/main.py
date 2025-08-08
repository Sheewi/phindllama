from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# Cloud Run service URL
CLOUD_RUN_URL = os.environ.get('CLOUD_RUN_URL', 'https://phindllama-trading-system-u5d2kummnq-uc.a.run.app')

@app.route('/')
def home():
    return '''
    <h1>PhindLlama App Engine Proxy</h1>
    <p>This App Engine service proxies requests to the Cloud Run backend.</p>
    <p>Cloud Run URL: {}</p>
    <p><a href="/api/health">Check System Health</a></p>
    '''.format(CLOUD_RUN_URL)

@app.route('/api/<path:path>')
def proxy_api(path):
    try:
        resp = requests.get(f"{CLOUD_RUN_URL}/{path}")
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({
            "error": "Failed to connect to backend service",
            "details": str(e)
        }), 500

@app.route('/api/health')
def health():
    try:
        # Check Cloud Run service health
        response = requests.get(f"{CLOUD_RUN_URL}/health", timeout=5)
        return jsonify({
            "status": "healthy",
            "cloud_run_status": "healthy" if response.status_code == 200 else "error"
        })
    except Exception as e:
        return jsonify({
            "status": "healthy",
            "cloud_run_status": "unreachable",
            "error": str(e)
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
