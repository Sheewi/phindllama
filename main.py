#!/usr/bin/env python3
"""
Main entry point for App Engine
"""

import logging
from api_server import app

# App Engine uses gunicorn as the web server and expects
# the Flask app to be named 'app' in the 'main.py' file
# No need to run the app here, App Engine will do that

if __name__ == "__main__":
    # This is used when running locally
    logging.basicConfig(level=logging.INFO)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
