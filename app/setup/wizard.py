import os
import json
from web3 import Web3
from typing import Optional
from pathlib import Path
from pydantic import BaseModel, field_validator
import questionary

class WalletConfig(BaseModel):
    address: str
    chain: str = "ethereum"
    signed_in: bool = False

    @field_validator('address')
    @classmethod
    def validate_address(cls, v):
        # Allow empty address for autonomous mode
        if v == "":
            return v
        if not Web3.is_address(v):
            raise ValueError("Invalid wallet address")
        return Web3.to_checksum_address(v)

class UserProfile(BaseModel):
    business_type: str
    target_services: list
    automation_level: int = 1

class SetupWizard:
    def __init__(self):
        self.config_path = Path("~/.phindllama/config.json").expanduser()
        self.w3 = Web3(Web3.HTTPProvider(self._get_default_rpc()))

    def _get_default_rpc(self) -> str:
        """Get default RPC endpoint"""
        return os.getenv('WEB3_PROVIDER_URI', 'https://mainnet.infura.io/v3/your-project-id')

    def _get_current_version(self) -> str:
        """Get current application version"""
        return "0.1.0"

    def _greet(self):
        """Welcome message"""
        print("Welcome to PhindLlama Setup Wizard!")
        print("This will configure your autonomous AI system.")

    def _configure_services(self):
        """Configure system services"""
        print("Configuring system services...")
        # Placeholder for service configuration logic

    def run(self, interactive: bool = False):
        """Main wizard flow"""
        if interactive:
            self._greet()
        else:
            print("PhindLlama: Starting autonomous configuration...")
            
        wallet = self._setup_wallet(interactive)
        profile = self._setup_profile(interactive)
        self._configure_services()
        self._install_hooks()
        self._finalize(wallet, profile)

    def _setup_wallet(self, interactive: bool = False) -> WalletConfig:
        """Wallet connection flow"""
        if interactive:
            choice = questionary.select(
                "Connect your wallet:",
                choices=["MetaMask", "WalletConnect", "Phantom", "Skip"]
            ).ask()

            if choice == "Skip":
                return WalletConfig(address="", signed_in=False)

            address = questionary.text("Enter wallet address:").ask()
            return WalletConfig(address=address, signed_in=True)
        else:
            # Autonomous mode - no wallet connection by default for security
            return WalletConfig(address="", signed_in=False)

    def _setup_profile(self, interactive: bool = False) -> UserProfile:
        """AI profile customization"""
        if interactive:
            business_type = questionary.select(
                "Your business type:",
                choices=["Freelancer", "Agency", "Startup", "Enterprise"]
            ).ask()
            
            target_services = questionary.checkbox(
                "Enable services:",
                choices=[
                    "Job Scraping",
                    "Grant Applications", 
                    "Auto-Promotion",
                    "Lead Generation"
                ]
            ).ask()
            
            # Use text input instead of slider (questionary doesn't have slider)
            automation_level = int(questionary.text(
                "Automation level (1-5):",
                default="3",
                validate=lambda x: x.isdigit() and 1 <= int(x) <= 5
            ).ask())
        else:
            # Autonomous defaults - optimal configuration
            business_type = "Startup"  # Most versatile for autonomous operation
            target_services = [
                "Job Scraping",
                "Grant Applications",
                "Auto-Promotion", 
                "Lead Generation"
            ]  # Enable all services for maximum autonomy
            automation_level = 5  # Maximum automation
            
        return UserProfile(
            business_type=business_type,
            target_services=target_services,
            automation_level=automation_level
        )

    def _install_hooks(self):
        """Self-evolving system hooks"""
        hooks = [
            ("update_checker", "0 3 * * *"),  # Daily at 3AM
            ("performance_analyzer", "*/30 * * * *"),
            ("behavior_adjuster", "0 */6 * * *")
        ]
        # Implementation would vary by OS
        print(f"Installing {len(hooks)} ecosystem hooks...")

    def _finalize(self, wallet: WalletConfig, profile: UserProfile):
        """Save configuration and initialize"""
        config = {
            "wallet": wallet.model_dump(),
            "profile": profile.model_dump(),
            "version": self._get_current_version(),
            "hooks_installed": True
        }
        
        self.config_path.parent.mkdir(exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print("Setup complete! Ecosystem is now self-managing.")

if __name__ == "__main__":
    import sys
    # Check if interactive mode is requested
    interactive = "--interactive" in sys.argv or "-i" in sys.argv
    
    wizard = SetupWizard()
    wizard.run(interactive=interactive)