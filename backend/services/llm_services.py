import os
import requests
from dotenv import load_dotenv

load_dotenv()

class LLMService:

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "openai/gpt-oss-20b:free"

    def ask(self, prompt: str):
        if not self.api_key:
            return "API key not configured in .env file."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }
        try:
            res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=30)
            if res.status_code == 200:
                data = res.json()
                return data["choices"][0]["message"]["content"]
            return f"Error from LLM API ({res.status_code}): {res.text}"
        except Exception as e:
            return f"LLM API request error: {e}"

    def analyze_repository(self, repository_data: dict):
        prompt = f"""
You are an expert GitHub Repository Analyst.
Analyze the following repository:
{repository_data}

Generate:
1. Repository Summary
2. Health Assessment
3. Community Activity
4. Contributor Insights
5. Strengths
6. Weaknesses
7. Recommendations
"""
        return self.ask(prompt)

    def explain_metrics(self, analytics: dict):
        prompt = f"""
Explain these repository metrics in simple language:
{analytics}

Explain:
- Health Score
- Commit Frequency
- Merge Rate
- Issue Resolution
- Contributor Growth
- Community Engagement
"""
        return self.ask(prompt)

    def repository_chat(self, repository_data: dict, question: str):
        prompt = f"""
Repository Information:
{repository_data}

Question:
{question}

Answer concisely using only the repository information.
"""
        return self.ask(prompt)