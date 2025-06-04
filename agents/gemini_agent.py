# agents/gemini_agent.py

from vertexai.preview.generative_models import GenerativeModel
import vertexai
from google.oauth2 import service_account

class GeminiAgent:
    def __init__(self, project_id: str, location: str = "asia-south1"):
        credentials = service_account.Credentials.from_service_account_file("secrets/service-account.json")
        vertexai.init(project=project_id, location=location, credentials=credentials)
        self.model = GenerativeModel("gemini-pro")

    def run(self, prompt: str):
        response = self.model.generate_content(prompt)
        return response.text
