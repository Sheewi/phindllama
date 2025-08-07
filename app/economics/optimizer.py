from scipy.optimize import linprog
import numpy as np

class ProfitOptimizer:
    def __init__(self):
        self.agent_costs = {
            'job_scraper': 0.01,
            'grant_writer': 0.05, 
            'sales_agent': 0.03
        }
        
    def calculate_allocations(self, profit_data: Dict[str, float]) -> Dict[str, float]:
        """Linear programming for optimal resource allocation"""
        # Objective: Maximize profit
        c = [-x for x in profit_data.values()]  # Negative for maximization
        
        # Constraints: 
        # 1. Total budget <= 1 (100%)
        # 2. Each agent >= min allocation
        A = [[1, 1, 1]]  # Sum of allocations
        b = [1]          # Total budget
        
        bounds = [
            (0.1, 1),    # Job scraper min 10%
            (0.05, 1),   # Grant writer min 5%
            (0.2, 1)     # Sales min 20%
        ]
        
        res = linprog(c, A_ub=A, b_ub=b, bounds=bounds)
        return {
            'job_scraper': res.x[0],
            'grant_writer': res.x[1],
            'sales_agent': res.x[2]
        }