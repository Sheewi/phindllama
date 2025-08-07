import openai
from typing import List
from pydantic import BaseModel

class GrantApplication(BaseModel):
    foundation: str
    deadline: str
    amount: float
    requirements: List[str]

class GrantWriter:
    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.template = """Write a compelling grant application to {foundation} for {amount} focusing on:
        - {requirements}
        - Our unique qualifications: {qualifications}"""

    def generate_proposal(self, grant: GrantApplication, qualifications: List[str]) -> str:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{
                "role": "system",
                "content": "You're an expert grant writer"
            }, {
                "role": "user",
                "content": self.template.format(
                    foundation=grant.foundation,
                    amount=grant.amount,
                    requirements='\n- '.join(grant.requirements),
                    qualifications='\n- '.join(qualifications)
                )
            }]
        )
        return response.choices[0].message.content

    def submit_application(self, proposal: str, endpoint: str) -> bool:
        # Implementation for submission logic
        pass