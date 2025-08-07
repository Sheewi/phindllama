import openai
from typing import List
from pydantic import BaseModel

class ProjectIdea(BaseModel):
    title: str
    description: str
    potential_clients: List[str]
    required_skills: List[str]

class WorkGenerator:
    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.prompt = """Generate 5 innovative project ideas for a {business_type} business with these core competencies:
        - {skills}
        
        Include:
        1. Project title
        2. 2-sentence description
        3. Potential client types
        4. Required skills"""

    def generate_ideas(self, business_type: str, skills: List[str]) -> List[ProjectIdea]:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{
                "role": "system",
                "content": "You're a creative business strategist"
            }, {
                "role": "user",
                "content": self.prompt.format(
                    business_type=business_type,
                    skills='\n- '.join(skills)
                )
            }]
        )
        return self._parse_response(response.choices[0].message.content)

    def _parse_response(self, text: str) -> List[ProjectIdea]:
        # Implementation to parse AI response
        pass