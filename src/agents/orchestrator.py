from concurrent.futures import ThreadPoolExecutor
from agents import JobScraper, GrantWriter, PromotionEngine, WorkGenerator

class Orchestrator:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=5)
        
    def run_daily_workflow(self):
        # Job scraping every 6 hours
        self.executor.submit(JobScraper().scrape, "AI development", "Remote")
        
        # Grant applications weekly
        self.executor.submit(GrantWriter().process_pending_grants)
        
        # Social media posting
        self.executor.submit(PromotionEngine().post_scheduled_content)