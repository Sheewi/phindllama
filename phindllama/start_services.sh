#!/bin/bash

# Initialize files
touch /workspaces/phindllama/wallet_history.csv

# Start the adaptation service in background
python /workspaces/phindllama/adaptation_service.py > adaptation.log 2>&1 &

# Start the dashboard
streamlit run /workspaces/phindllama/dashboard.py \
    --server.port=8501 \
    --server.headless=true \
    --browser.serverAddress=0.0.0.0

# Keep container running (if using interactive mode)
tail -f /dev/null