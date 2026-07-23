import os
import requests
from dotenv import load_dotenv

load_dotenv()

class GitHubClient:
    BASE_URL = "https://api.github.com"

    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.headers = {
            "Accept": "application/vnd.github+json"
        }
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"

    def _get(self, endpoint, params=None):
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_repository(self, owner, repo):
        return self._get(f"/repos/{owner}/{repo}")

    def get_contributors(self, owner, repo, per_page=100):
        return self._get(f"/repos/{owner}/{repo}/contributors", {"per_page": per_page})

    def get_commits(self, owner, repo, per_page=100):
        return self._get(f"/repos/{owner}/{repo}/commits", {"per_page": per_page})

    def get_issues(self, owner, repo, state="all", per_page=100):
        return self._get(f"/repos/{owner}/{repo}/issues", {"state": state, "per_page": per_page})

    def get_pull_requests(self, owner, repo, state="all", per_page=100):
        return self._get(f"/repos/{owner}/{repo}/pulls", {"state": state, "per_page": per_page})

    def get_releases(self, owner, repo):
        return self._get(f"/repos/{owner}/{repo}/releases")

    def get_branches(self, owner, repo):
        return self._get(f"/repos/{owner}/{repo}/branches")

    def get_tags(self, owner, repo):
        return self._get(f"/repos/{owner}/{repo}/tags")

    def get_languages(self, owner, repo):
        return self._get(f"/repos/{owner}/{repo}/languages")

    def get_events(self, owner, repo, per_page=100):
        return self._get(f"/repos/{owner}/{repo}/events", {"per_page": per_page})
