#!/bin/bash
# start_services.sh

# Initialize history file if missing
touch /workspaces/phindllama/wallet_history.csv

# Start services
supervisord -c /workspaces/phindllama/supervisord.conf &

# Wait for services to start
sleep 5

# Verify services
ps aux | grep -E 'supervisord|streamlit'

# Keep container running
tail -f /dev/null