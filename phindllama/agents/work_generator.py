# phindllama/agents/work_generator.py
"""Work generation agent for creating project ideas and opportunities."""
from typing import List, Dict, Any
import logging
from datetime import datetime
import random

class ProjectIdea:
    """Simple project idea representation."""
    
    def __init__(self, title: str, description: str, potential_clients: List[str], required_skills: List[str]):
        self.title = title
        self.description = description
        self.potential_clients = potential_clients
        self.required_skills = required_skills

class WorkGenerator:
    """Agent specialized in generating work opportunities and project ideas."""
    
    def __init__(self, config: Dict[str, Any]):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.generated_ideas = []
        
        # Business type templates
        self.business_templates = {
            'fintech': {
                'skills': ['blockchain', 'trading algorithms', 'risk management', 'compliance'],
                'clients': ['banks', 'investment firms', 'crypto exchanges', 'fintech startups']
            },
            'ai_development': {
                'skills': ['machine learning', 'data analysis', 'automation', 'nlp'],
                'clients': ['tech companies', 'research institutions', 'enterprises', 'consultancies']
            },
            'automation': {
                'skills': ['process automation', 'rpa', 'workflow optimization', 'integration'],
                'clients': ['manufacturing', 'healthcare', 'finance', 'logistics']
            }
        }
        
        self.prompt = """Generate innovative project ideas for a {business_type} business with these core competencies:
        - {skills}
        
        Include:
        1. Project title
        2. 2-sentence description
        3. Potential client types
        4. Required skills"""
        
        self.logger.info("WorkGenerator initialized")

    def generate_ideas(self, business_type: str, skills: List[str]) -> List[ProjectIdea]:
        """Generate project ideas based on business type and skills."""
        ideas = []
        
        # Use predefined templates or custom skills
        if business_type in self.business_templates:
            template = self.business_templates[business_type]
            base_skills = template['skills']
            base_clients = template['clients']
        else:
            base_skills = skills
            base_clients = ['enterprises', 'startups', 'government', 'nonprofits']
        
        # Generate specific project ideas
        project_templates = [
            {
                'title': f"Automated {business_type.title()} Platform",
                'description': f"Comprehensive automation platform for {business_type} operations. Reduces manual work by 80% and increases efficiency.",
                'skills': base_skills[:3],
                'clients': base_clients[:2]
            },
            {
                'title': f"AI-Powered {business_type.title()} Analytics",
                'description': f"Advanced analytics solution using machine learning for {business_type} insights. Provides real-time decision support and predictive capabilities.",
                'skills': ['ai', 'data analysis'] + base_skills[:2],
                'clients': base_clients[1:3]
            },
            {
                'title': f"Custom {business_type.title()} Integration Suite",
                'description': f"Seamless integration platform connecting various {business_type} systems. Improves data flow and operational efficiency.",
                'skills': ['api development', 'integration'] + base_skills[:2],
                'clients': base_clients
            },
            {
                'title': f"Mobile {business_type.title()} Application",
                'description': f"User-friendly mobile app for {business_type} management. Provides on-the-go access and real-time notifications.",
                'skills': ['mobile development', 'ui/ux'] + base_skills[:2],
                'clients': base_clients[:3]
            },
            {
                'title': f"Enterprise {business_type.title()} Dashboard",
                'description': f"Comprehensive dashboard for {business_type} monitoring and control. Features customizable widgets and real-time data visualization.",
                'skills': ['dashboard development', 'data visualization'] + base_skills[:2],
                'clients': ['large enterprises', 'corporations']
            }
        ]
        
        for template in project_templates:
            idea = ProjectIdea(
                title=template['title'],
                description=template['description'],
                potential_clients=template['clients'],
                required_skills=template['skills']
            )
            ideas.append(idea)
        
        self.generated_ideas.extend(ideas)
        self.logger.info(f"Generated {len(ideas)} project ideas for {business_type}")
        
        return ideas

    def estimate_project_value(self, idea: ProjectIdea) -> Dict[str, Any]:
        """Estimate the potential value of a project idea."""
        # Base estimation logic
        skill_multiplier = len(idea.required_skills) * 10000
        client_multiplier = len(idea.potential_clients) * 5000
        complexity_bonus = random.randint(5000, 25000)
        
        estimated_value = skill_multiplier + client_multiplier + complexity_bonus
        
        return {
            'project_title': idea.title,
            'estimated_value': estimated_value,
            'time_estimate': f"{random.randint(2, 12)} months",
            'difficulty': random.choice(['easy', 'medium', 'hard']),
            'market_demand': random.choice(['low', 'medium', 'high']),
            'competition_level': random.choice(['low', 'medium', 'high']),
            'roi_potential': random.uniform(1.5, 4.0),
            'estimated_at': datetime.now().isoformat()
        }

    def identify_market_gaps(self, industry: str) -> List[Dict[str, Any]]:
        """Identify potential market gaps and opportunities."""
        gaps = [
            {
                'gap': f"Lack of user-friendly {industry} tools",
                'opportunity': f"Develop intuitive {industry} platform",
                'market_size': random.randint(100000, 1000000),
                'urgency': random.choice(['low', 'medium', 'high']),
                'investment_required': random.randint(50000, 500000)
            },
            {
                'gap': f"Limited automation in {industry}",
                'opportunity': f"Create automation solutions for {industry}",
                'market_size': random.randint(200000, 2000000),
                'urgency': random.choice(['medium', 'high']),
                'investment_required': random.randint(100000, 750000)
            },
            {
                'gap': f"Poor integration between {industry} systems",
                'opportunity': f"Build integration platform for {industry}",
                'market_size': random.randint(150000, 1500000),
                'urgency': random.choice(['medium', 'high']),
                'investment_required': random.randint(75000, 600000)
            }
        ]
        
        self.logger.info(f"Identified {len(gaps)} market gaps for {industry}")
        return gaps

    def generate_business_plan_outline(self, idea: ProjectIdea) -> Dict[str, Any]:
        """Generate a basic business plan outline for a project idea."""
        plan = {
            'project_title': idea.title,
            'executive_summary': idea.description,
            'market_analysis': {
                'target_clients': idea.potential_clients,
                'market_size': f"${random.randint(100, 1000)}M",
                'competition': 'Moderate'
            },
            'technical_requirements': {
                'required_skills': idea.required_skills,
                'team_size': f"{len(idea.required_skills) + 2}-{len(idea.required_skills) + 5} people",
                'technology_stack': 'Modern web/mobile technologies'
            },
            'financial_projections': {
                'initial_investment': f"${random.randint(50, 500)}K",
                'revenue_year_1': f"${random.randint(100, 800)}K",
                'revenue_year_3': f"${random.randint(500, 3000)}K",
                'break_even': f"{random.randint(12, 24)} months"
            },
            'milestones': [
                'Proof of concept - 3 months',
                'MVP development - 6 months',
                'First client - 9 months',
                'Market expansion - 12 months'
            ],
            'generated_at': datetime.now().isoformat()
        }
        
        self.logger.info(f"Generated business plan outline for: {idea.title}")
        return plan

    def get_generation_summary(self) -> Dict[str, Any]:
        """Get summary of work generation activities."""
        return {
            'total_ideas_generated': len(self.generated_ideas),
            'unique_business_types': len(self.business_templates),
            'last_generation': datetime.now().isoformat() if self.generated_ideas else None,
            'available_templates': list(self.business_templates.keys())
        }