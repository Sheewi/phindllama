#!/bin/bash

# Run Streamlit dashboard
streamlit run --server.port 8501 --server.headless true --browser.serverAddress 0.0.0.0 <<EOF > dashboard.log 2>&1 &
import streamlit as st
from wallet.profit_tracker import WalletProfitTracker
st.title("Profitability Dashboard")
wt = WalletProfitTracker.load()
st.line_chart(wt.history.set_index('timestamp')['usd_value'])
EOF

# Set up Nginx reverse proxy (optional)
sudo apt install nginx
sudo tee /etc/nginx/sites-available/phindllama <<EOF
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/phindllama /etc/nginx/sites-enabled
sudo systemctl restart nginx
