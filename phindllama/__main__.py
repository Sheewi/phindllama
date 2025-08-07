#!/usr/bin/env python3
"""Main entry point for the phindllama system."""
import sys
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def check_and_run_setup():
    """Check if initial setup is needed and run it autonomously."""
    import logging
    logger = logging.getLogger(__name__)
    
    config_path = Path.home() / ".phindllama" / "config.json"
    
    if not config_path.exists():
        logger.info("No configuration found. Running autonomous setup...")
        try:
            # Create basic config autonomously
            config = {
                "wallet": {"address": "", "chain": "ethereum", "signed_in": False},
                "profile": {
                    "business_type": "Startup",
                    "target_services": ["Job Scraping", "Grant Applications", "Auto-Promotion", "Lead Generation"],
                    "automation_level": 5
                },
                "version": "0.1.0",
                "hooks_installed": True,
                "autonomous_mode": True
            }
            
            config_path.parent.mkdir(exist_ok=True)
            with open(config_path, 'w') as f:
                import json
                json.dump(config, f, indent=2)
            
            logger.info("Autonomous configuration created successfully")
            return True
        except Exception as e:
            logger.warning(f"Autonomous setup failed: {e}")
            return False
    return True

def main():
    """Main entry point."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Starting PhindLlama system...")
    
    # Run initial setup if needed
    if not check_and_run_setup():
        logger.error("Setup failed, continuing anyway...")
    
    try:
        # Try the correct import path first
        from .orchestrator import AdaptiveOrchestrator
        orchestrator = AdaptiveOrchestrator()
        orchestrator.run()
    except ImportError as e:
        logger.error(f"Import error: {e}")
        logger.info("Running basic setup instead...")
        
        # Basic setup without dependencies
        print("PhindLlama - Autonomous AI System")
        print("=" * 40)
        print("System starting in minimal mode...")
        print("For interactive setup: python app/setup/wizard.py --interactive")
        
    except Exception as e:
        logger.error(f"Startup error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()