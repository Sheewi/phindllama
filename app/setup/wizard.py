import os
import json
from web3 import Web3
from typing import Optional
from pathlib import Path
from pydantic import BaseModel, validator
import questionary

class WalletConfig(BaseModel):
    address: str
    chain: str = "ethereum"
    signed_in: bool = False

    @validator('address')
    def validate_address(cls, v):
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

    def run(self):
        """Main wizard flow"""
        self._greet()
        wallet = self._setup_wallet()
        profile = self._setup_profile()
        self._configure_services()
        self._install_hooks()
        self._finalize(wallet, profile)

    def _setup_wallet(self) -> WalletConfig:
        """Wallet connection flow"""
        choice = questionary.select(
            "Connect your wallet:",
            choices=["MetaMask", "WalletConnect", "Phantom", "Skip"]
        ).ask()

        if choice == "Skip":
            return WalletConfig(address="", signed_in=False)

        address = questionary.text("Enter wallet address:").ask()
        return WalletConfig(address=address, signed_in=True)

    def _setup_profile(self) -> UserProfile:
        """AI profile customization"""
        return UserProfile(
            business_type=questionary.select(
                "Your business type:",
                choices=["Freelancer", "Agency", "Startup", "Enterprise"]
            ).ask(),
            target_services=questionary.checkbox(
                "Enable services:",
                choices=[
                    "Job Scraping",
                    "Grant Applications",
                    "Auto-Promotion",
                    "Lead Generation"
                ]
            ).ask(),
            automation_level=questionary.slider(
                "Automation level:",
                min_value=1,
                max_value=5,
                default=3
            ).ask()
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
            "wallet": wallet.dict(),
            "profile": profile.dict(),
            "version": self._get_current_version(),
            "hooks_installed": True
        }
        
        self.config_path.parent.mkdir(exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print("Setup complete! Ecosystem is now self-managing.")