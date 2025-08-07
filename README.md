# PhindLlama - Autonomous AI Financial System

An intelligent, self-managing AI system for automated financial operations, trading, and business development.

## Features

- **Autonomous Trading**: AI-powered trading strategies with risk management
- **Smart Contract Integration**: Automated DeFi operations and flash loans
- **Grant Management**: Automatic grant discovery and application
- **Job Generation**: AI-powered work opportunity detection
- **Self-Evolution**: System automatically adapts and improves over time
- **Multi-Agent Architecture**: Specialized agents for different tasks

## Quick Start

### Prerequisites

- Python 3.8+
- Docker (optional)
- Web3 provider (Infura, Alchemy, etc.)
- PostgreSQL (optional, falls back to SQLite)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/phindllama.git
   cd phindllama
   ```

2. **Install dependencies**
   ```bash
   pip install -e .
   ```
   
   Or install from requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.template .env
   # Edit .env with your configuration
   ```

4. **Run the setup wizard**
   ```bash
   python -m phindllama.app.setup.wizard
   ```

5. **Start the system**
   ```bash
   python -m phindllama
   ```

### Docker Deployment

```bash
# Build the image
docker build -t phindllama .

# Run the container
docker run -d \
  --name phindllama \
  -p 8080:8080 \
  --env-file .env \
  phindllama
```

## Configuration

### Environment Variables

Key environment variables (see `.env.template` for full list):

- `WEB3_PROVIDER_URI`: Your Web3 provider endpoint
- `WALLET_ADDRESS`: Your Ethereum wallet address
- `DATABASE_URL`: Database connection string
- `ENVIRONMENT`: deployment environment (development/staging/production)

### Setup Wizard

The setup wizard helps configure:

- Wallet connections (MetaMask, WalletConnect, etc.)
- Business profile and automation preferences
- Service enablement (job scraping, grants, etc.)
- Risk management parameters

## Architecture

```
phindllama/
├── agents/          # Specialized AI agents
├── api/            # REST API endpoints
├── config/         # Configuration management
├── contracts/      # Smart contract managers
├── core/           # Core system components
├── monitoring/     # System monitoring
├── storage/        # Data persistence
├── utils/          # Utility functions
└── wallet/         # Wallet and profit tracking
```

### Key Components

- **Orchestrator**: Main system coordinator
- **Agent Cluster**: Manages specialized AI agents
- **Risk Engine**: Monitors and manages risk
- **MCP Controller**: Model Context Protocol management
- **Smart Contract Manager**: DeFi operations
- **Persistent Memory**: Data storage and retrieval

## Usage

### Basic Operations

```python
from phindllama import AdaptiveOrchestrator

# Initialize the system
orchestrator = AdaptiveOrchestrator()

# Run a single cycle
orchestrator.run_cycle()

# Check system health
health = orchestrator.check_system_health()
print(health)
```

### API Usage

```bash
# Start the API server
uvicorn phindllama.api.endpoints:router --host 0.0.0.0 --port 8080

# Generate text
curl -X POST "http://localhost:8080/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Analyze market conditions"}'
```

### Trading Operations

```python
from phindllama.agents.trading_agent import TradingAgent

agent = TradingAgent(config={
    "risk_level": "moderate",
    "max_position_size": 1000
})

# Execute trading strategy
result = agent.execute_strategy("mean_reversion")
```

## Monitoring

- **Health Checks**: `/health` endpoint
- **Metrics**: Prometheus-compatible metrics
- **Logging**: Structured logging with multiple levels
- **Alerts**: Configurable alert system

## Security

- **Wallet Security**: Private keys never stored in code
- **API Authentication**: OAuth2 with JWT tokens
- **Risk Management**: Built-in risk monitoring and limits
- **Input Validation**: Pydantic models for data validation

## Development

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
# Format code
black phindllama/

# Lint code
flake8 phindllama/

# Type checking
mypy phindllama/
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Web3 Connection**: Check your provider URL and API key
   ```bash
   python -c "from web3 import Web3; print(Web3().isConnected())"
   ```

3. **Database Issues**: Check database URL and permissions
   ```bash
   python -c "from sqlalchemy import create_engine; create_engine('your_db_url').connect()"
   ```

### Logs

Check logs for detailed error information:
```bash
tail -f app.log
```

## License

MIT License - see LICENSE file for details.

## Support

- GitHub Issues: Report bugs and feature requests
- Documentation: See `docs/` directory
- Community: Join our Discord/Telegram (links in profile)

## Roadmap

- [ ] Enhanced ML models for market prediction
- [ ] Multi-chain support (Polygon, Arbitrum, etc.)
- [ ] Advanced portfolio management
- [ ] Social media integration
- [ ] Mobile app development
- [ ] Enterprise features
