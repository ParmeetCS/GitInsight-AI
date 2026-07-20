import requests
from requests import request
import os 
import requests
from dotenv import load_dotenv

load_dotenv()

class GitHubClient:
    BASE_URL="https://api.github.com"

    def __init__(self):
        self.token=os.getenv("GITHUB_TOKEN")

        self.headers={
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json"
        }
    
    def _get(self,endpoint,params=None):
        url=f"{self.BASE_URL}{endpoint}"

        repsone=requests.get(
            url,
            headers=self.headers,
            params=params
        )

        repsone.raise_for_status()
        return repsone.json()
    
    def get_repository(self,owner,repo):
        return self._get(f"/repos/{owner}/{repo}")
    
    def get_contributors(self,owner,repo,per_page=100):
        return self._get(
            f"/repos/{owner}/{repo}/contributors",
            {"per_page": per_page}
        )
    def get_commits(self, owner, repo, per_page=100):
        return self._get(
            f"/repos/{owner}/{repo}/commits",
            {"per_page": per_page}
        )

    def get_issues(self, owner, repo, state="all", per_page=100):
        return self._get(
            f"/repos/{owner}/{repo}/issues",
            {
                "state": state,
                "per_page": per_page
            }
        )

    def get_pull_requests(self, owner, repo, state="all", per_page=100):
        return self._get(
            f"/repos/{owner}/{repo}/pulls",
            {
                "state": state,
                "per_page": per_page
            }
        )
    def get_releases(self, owner, repo):
        return self._get(
            f"/repos/{owner}/{repo}/releases"
        )
    def get_branches(self, owner, repo):
        return self._get(
            f"/repos/{owner}/{repo}/branches"
        )
    def get_tags(self, owner, repo):
        return self._get(
            f"/repos/{owner}/{repo}/tags"
        )
    def get_languages(self, owner, repo):
        return self._get(
            f"/repos/{owner}/{repo}/languages"
        )

    def get_events(self, owner, repo, per_page=100):
        return self._get(
            f"/repos/{owner}/{repo}/events",
            {"per_page": per_page}
        )

   
    def get_discussions(self, owner, repo):
        raise NotImplementedError(
            "GitHub Discussions require the GraphQL API."
        )
    
# for individual file testing 
if __name__=="__main__":
    github=GitHubClient()
    OWNER = "langchain-ai"
    REPO = "langchain"

    print("Repository")
    print(github.get_repository(OWNER, REPO)["full_name"])

    print("Contributors")
    print(len(github.get_contributors(OWNER, REPO)))

    print("Commits")
    print(len(github.get_commits(OWNER, REPO)))

    print("Issues")
    print(len(github.get_issues(OWNER, REPO)))

    print("Pull Requests")
    print(len(github.get_pull_requests(OWNER, REPO)))

    print("Releases")
    print(len(github.get_releases(OWNER, REPO)))

    print("Branches")
    print(len(github.get_branches(OWNER, REPO)))

    print("Tags")
    print(len(github.get_tags(OWNER, REPO)))

    print("Languages")
    print(github.get_languages(OWNER, REPO))

    print("Repository Events")
    print(len(github.get_events(OWNER, REPO)))
