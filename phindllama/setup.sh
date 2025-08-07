#!/bin/bash

# Install core dependencies
pip install web3 pandas scikit-learn boto3 streamlit questionary python-dotenv

# Set up environment variables
echo "INFURA_KEY=your_infura_key_here" > .env
echo "WALLET_ADDRESS=0xYourWalletAddress" >> .env
echo "AWS_ACCESS_KEY=your_aws_key" >> .env
echo "AWS_SECRET=your_aws_secret" >> .env

# Initialize wallet tracking
python3 -c "
from wallet.profit_tracker import WalletProfitTracker
from web3 import Web3
import os
w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{os.getenv(\"INFURA_KEY\")}'))
wt = WalletProfitTracker(w3, os.getenv('WALLET_ADDRESS'))
wt.update_snapshot()
print('Initial wallet snapshot recorded')
"

# Create systemd service (Linux)
echo "[Unit]
Description=PhindLlama Adaptation System
After=network.target

[Service]
User=$USER
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/python3 -c '
from orchestrator import AdaptiveOrchestrator;
from web3 import Web3;
import os;
w3 = Web3(Web3.HTTPProvider(f\"https://mainnet.infura.io/v3/{os.getenv(\"INFURA_KEY\")}\"));
orchestrator = AdaptiveOrchestrator(w3);
orchestrator.run_cycle()
'
Restart=always

[Install]
WantedBy=multi-user.target" | sudo tee /etc/systemd/system/phindllama.service

sudo systemctl daemon-reload
sudo systemctl enable phindllama.service
