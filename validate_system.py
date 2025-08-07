#!/usr/bin/env python3
"""
System validation script to demonstrate all components are working correctly.
"""

def test_imports():
    """Test that all major components can be imported."""
    print("🔍 Testing imports...")
    
    try:
        from phindllama.orchestrator import Orchestrator
        print("✅ Orchestrator")
        
        from phindllama.agent_cluster import AgentCluster
        print("✅ AgentCluster")
        
        from phindllama.risk_engine import RiskEngine
        print("✅ RiskEngine")
        
        from phindllama.agents.trading_agent import TradingAgent
        print("✅ TradingAgent")
        
        from phindllama.agents.financial_agent import FinancialAgent
        print("✅ FinancialAgent")
        
        from phindllama.agents.grant_writer import GrantWriter
        print("✅ GrantWriter")
        
        from phindllama.agents.job_scraper import JobScraper
        print("✅ JobScraper")
        
        from phindllama.agents.promotion_engine import PromotionEngine
        print("✅ PromotionEngine")
        
        from phindllama.agents.work_generator import WorkGenerator
        print("✅ WorkGenerator")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_initialization():
    """Test that components can be initialized."""
    print("\n🔍 Testing initialization...")
    
    try:
        from phindllama.orchestrator import Orchestrator
        from phindllama.agent_cluster import AgentCluster
        from phindllama.risk_engine import RiskEngine
        from phindllama.agents.trading_agent import TradingAgent
        from phindllama.agents.financial_agent import FinancialAgent
        
        config = {'mode': 'simulation', 'debug': True}
        
        # Test core components
        orchestrator = Orchestrator(config)
        print("✅ Orchestrator initialized")
        
        cluster = AgentCluster(config)
        print("✅ AgentCluster initialized")
        
        risk_engine = RiskEngine(config)
        print("✅ RiskEngine initialized")
        
        # Test agents
        trading_agent = TradingAgent(config)
        print("✅ TradingAgent initialized")
        
        financial_agent = FinancialAgent(config)
        print("✅ FinancialAgent initialized")
        
        return True
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return False

def test_functionality():
    """Test basic functionality of components."""
    print("\n🔍 Testing functionality...")
    
    try:
        from phindllama.agents.trading_agent import TradingAgent
        from phindllama.agents.financial_agent import FinancialAgent
        from phindllama.agents.job_scraper import JobScraper
        
        config = {'mode': 'simulation', 'debug': True}
        
        # Test trading agent
        trading_agent = TradingAgent(config)
        market_data = trading_agent.analyze_market("BTC/USD")
        print(f"✅ Trading analysis: {market_data['recommendation']}")
        
        # Test financial agent
        financial_agent = FinancialAgent(config)
        metrics = financial_agent.analyze_financial_metrics("ETH")
        print(f"✅ Financial analysis: {metrics['recommendation']}")
        
        # Test job scraper
        job_scraper = JobScraper(config)
        jobs = job_scraper.scrape_jobs("python developer")
        print(f"✅ Job scraping: Found {len(jobs)} jobs")
        
        return True
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def main():
    """Run validation tests."""
    print("🚀 PhindLlama System Validation")
    print("=" * 40)
    
    success = True
    
    # Run tests
    success &= test_imports()
    success &= test_initialization()
    success &= test_functionality()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 ALL TESTS PASSED!")
        print("✅ System is ready for autonomous operation")
        print("\nTo run the system autonomously:")
        print("   python3 -m phindllama")
    else:
        print("❌ Some tests failed")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
