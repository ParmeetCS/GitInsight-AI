from sqlalchemy.dialects.mssql.base import _owner_plus_db
from datetime import datetime

from database import SessionLocal
from models import(
    Repository,
    Contributor,
    Commit,
    Issue,
    PullRequest,
    Release,
    Branch,
    Tag,
    Language
)

from services.github_client import GitHubClient

class IngestionServices:
    def __init__(self):
        self.github=GitHubClient()
        self.db=SessionLocal()
        
    def ingest_repository(self, owner: str, repo: str):

        repo_data = self.github.get_repository(owner, repo)

        repository = Repository(
            github_id=repo_data["id"],
            owner=repo_data["owner"]["login"],
            name=repo_data["name"],
            full_name=repo_data["full_name"],
            description=repo_data["description"],
            language=repo_data["language"],
            license=repo_data["license"]["name"] if repo_data["license"] else None,
            stars=repo_data["stargazers_count"],
            forks=repo_data["forks_count"],
            watchers=repo_data["watchers_count"],
            open_issues=repo_data["open_issues_count"],
            default_branch=repo_data["default_branch"],
            html_url=repo_data["html_url"],
            created_at=datetime.fromisoformat(
                repo_data["created_at"].replace("Z", "+00:00")
            ),
            updated_at=datetime.fromisoformat(
                repo_data["updated_at"].replace("Z", "+00:00")
            )
        )

        self.db.add(repository)
        self.db.commit()
        self.db.refresh(repository)

        return repository
    
    def ingest_contributor(self,owner,repo,respository_id):
        contributor=self.github.get_contributors(owner,repo)
        print(f"Fetched {len(contributor)} contributors")
    
    def ingest_commits(self,owner,repo,repository_id):
        commit=self.github.get_commits(owner,repo)
        print(f"Fetched {len(commit)} commits")

    def ingest_issues(self,owner,repo,repository_id):
        issues=self.github.get_issues(owner,repo)
        print(f"Fetched {len(issues)} commits")
    
    def ingest_pull_requests(self, owner, repo, repository_id):

        prs = self.github.get_pull_requests(owner, repo)

        print(f"Fetched {len(prs)} pull requests")

    def ingest_releases(self, owner, repo, repository_id):

        releases = self.github.get_releases(owner, repo)

        print(f"Fetched {len(releases)} releases")

    def ingest_branches(self, owner, repo, repository_id):

        branches = self.github.get_branches(owner, repo)

        print(f"Fetched {len(branches)} branches")

    def ingest_tags(self, owner, repo, repository_id):

        tags = self.github.get_tags(owner, repo)

        print(f"Fetched {len(tags)} tags")

    def ingest_languages(self, owner, repo, repository_id):

        languages = self.github.get_languages(owner, repo)

        print(f"Fetched {len(languages)} languages")

    def run_pipeline(self,owner,repo):
        repository=self.ingest_repository(owner,repo)

        self.ingest_contributor(owner,repo,repository.id)
        self.ingest_commits(owner,repo,repository.id)
        self.ingest_issues(owner,repo,repository.id)
        self.ingest_pull_requests(owner,repo,repository.id)
        self.ingest_releases(owner, repo, repository.id)
        self.ingest_branches(owner, repo, repository.id)
        self.ingest_tags(owner, repo, repository.id)
        self.ingest_languages(owner, repo, repository.id)

        print("Repository ingestion completed successfully.")
    
    def close(self):
        self.db.close()

    
        