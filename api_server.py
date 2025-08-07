#!/usr/bin/env python3
"""Simple API server for PhindLlama status and control."""
import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime
from pathlib import Path
import json

app = FastAPI(
    title="PhindLlama API",
    description="Autonomous AI Financial System API",
    version="0.1.0"
)

logger = logging.getLogger(__name__)

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "PhindLlama Autonomous AI System", "status": "active"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "phindllama-api",
        "version": "0.1.0"
    }

@app.get("/status")
async def system_status():
    """Get system status."""
    try:
        config_path = Path.home() / ".phindllama" / "config.json"
        config_exists = config_path.exists()
        
        if config_exists:
            with open(config_path) as f:
                config = json.load(f)
        else:
            config = {}
        
        return {
            "system_configured": config_exists,
            "autonomous_mode": config.get("autonomous_mode", False),
            "automation_level": config.get("profile", {}).get("automation_level", 0),
            "services_enabled": config.get("profile", {}).get("target_services", []),
            "wallet_connected": config.get("wallet", {}).get("signed_in", False),
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        raise HTTPException(status_code=500, detail="Could not retrieve system status")

@app.post("/configure")
async def configure_system(autonomous: bool = True):
    """Configure system for autonomous operation."""
    try:
        config_path = Path.home() / ".phindllama" / "config.json"
        
        config = {
            "wallet": {"address": "", "chain": "ethereum", "signed_in": False},
            "profile": {
                "business_type": "Startup",
                "target_services": ["Job Scraping", "Grant Applications", "Auto-Promotion", "Lead Generation"],
                "automation_level": 5 if autonomous else 3
            },
            "version": "0.1.0",
            "hooks_installed": True,
            "autonomous_mode": autonomous
        }
        
        config_path.parent.mkdir(exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        return {
            "success": True,
            "message": f"System configured for {'autonomous' if autonomous else 'manual'} operation",
            "config": config
        }
    except Exception as e:
        logger.error(f"Error configuring system: {e}")
        raise HTTPException(status_code=500, detail="Configuration failed")

@app.get("/strategies")
async def get_strategies():
    """Get available strategies."""
    return {
        "available_strategies": [
            {
                "name": "market_analysis",
                "type": "analysis",
                "priority": 1,
                "status": "active"
            },
            {
                "name": "opportunity_detection", 
                "type": "detection",
                "priority": 2,
                "status": "active"
            },
            {
                "name": "risk_management",
                "type": "monitoring",
                "priority": 3,
                "status": "active"
            }
        ]
    }

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting PhindLlama API server...")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info"
    )
