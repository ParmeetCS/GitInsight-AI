from datetime import datetime
from database import SessionLocal
from models import (
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
        self.github = GitHubClient()
        self.db = SessionLocal()
        
    def ingest_repository(self, owner: str, repo: str, user_id: int = None):
        query = self.db.query(Repository).filter(
            Repository.owner.ilike(owner),
            Repository.name.ilike(repo)
        )
        if user_id is not None:
            query = query.filter(Repository.user_id == user_id)
        
        existing_repo = query.first()
        if existing_repo:
            self.db.delete(existing_repo)
            self.db.commit()

        repo_data = self.github.get_repository(owner, repo)

        repository = Repository(
            user_id=user_id,
            github_id=repo_data["id"],
            owner=repo_data["owner"]["login"],
            name=repo_data["name"],
            full_name=repo_data["full_name"],
            description=repo_data.get("description"),
            language=repo_data.get("language"),
            license=repo_data["license"]["name"] if repo_data.get("license") else None,
            stars=repo_data.get("stargazers_count", 0),
            forks=repo_data.get("forks_count", 0),
            watchers=repo_data.get("watchers_count", 0),
            open_issues=repo_data.get("open_issues_count", 0),
            default_branch=repo_data.get("default_branch"),
            html_url=repo_data.get("html_url"),
            created_at=datetime.fromisoformat(
                repo_data["created_at"].replace("Z", "+00:00")
            ) if repo_data.get("created_at") else None,
            updated_at=datetime.fromisoformat(
                repo_data["updated_at"].replace("Z", "+00:00")
            ) if repo_data.get("updated_at") else None
        )

        self.db.add(repository)
        self.db.commit()
        self.db.refresh(repository)

        return repository
    
    def ingest_contributor(self, owner, repo, repository_id):
        contributors = self.github.get_contributors(owner, repo)
        for c_data in contributors:
            contributor = Contributor(
                repository_id=repository_id,
                github_id=c_data["id"],
                username=c_data["login"],
                profile_url=c_data.get("html_url"),
                avatar_url=c_data.get("avatar_url"),
                account_type=c_data.get("type"),
                site_admin=c_data.get("site_admin", False),
                contributions=c_data.get("contributions", 0)
            )
            self.db.add(contributor)
    
    def ingest_commits(self, owner, repo, repository_id):
        commits = self.github.get_commits(owner, repo)
        for c_data in commits:
            commit_date_str = None
            if "commit" in c_data:
                if c_data["commit"].get("committer"):
                    commit_date_str = c_data["commit"]["committer"].get("date")
                elif c_data["commit"].get("author"):
                    commit_date_str = c_data["commit"]["author"].get("date")
            
            commit_date = datetime.fromisoformat(commit_date_str.replace("Z", "+00:00")) if commit_date_str else None
            
            commit = Commit(
                repository_id=repository_id,
                sha=c_data["sha"],
                author_name=c_data["commit"]["author"]["name"] if ("commit" in c_data and c_data["commit"].get("author")) else None,
                author_username=c_data["author"]["login"] if c_data.get("author") else None,
                committer_name=c_data["commit"]["committer"]["name"] if ("commit" in c_data and c_data["commit"].get("committer")) else None,
                committer_username=c_data["committer"]["login"] if c_data.get("committer") else None,
                message=c_data["commit"]["message"] if "commit" in c_data else None,
                url=c_data.get("url"),
                html_url=c_data.get("html_url"),
                comments_url=c_data.get("comments_url"),
                commit_date=commit_date
            )
            self.db.add(commit)

    def ingest_issues(self, owner, repo, repository_id):
        issues = self.github.get_issues(owner, repo)
        for i_data in issues:
            if "pull_request" in i_data:
                continue
            
            created_at = datetime.fromisoformat(i_data["created_at"].replace("Z", "+00:00")) if i_data.get("created_at") else None
            updated_at = datetime.fromisoformat(i_data["updated_at"].replace("Z", "+00:00")) if i_data.get("updated_at") else None
            closed_at = datetime.fromisoformat(i_data["closed_at"].replace("Z", "+00:00")) if i_data.get("closed_at") else None
            
            issue = Issue(
                repository_id=repository_id,
                github_issue_id=i_data["id"],
                issue_number=i_data["number"],
                title=i_data["title"],
                body=i_data.get("body"),
                state=i_data.get("state"),
                state_reason=i_data.get("state_reason"),
                author=i_data["user"]["login"] if i_data.get("user") else None,
                assignee=i_data["assignee"]["login"] if i_data.get("assignee") else None,
                labels=",".join([l["name"] for l in i_data.get("labels", [])]),
                comments=i_data.get("comments", 0),
                locked=i_data.get("locked", False),
                url=i_data.get("url"),
                html_url=i_data.get("html_url"),
                created_at=created_at,
                updated_at=updated_at,
                closed_at=closed_at
            )
            self.db.add(issue)
    
    def ingest_pull_requests(self, owner, repo, repository_id):
        prs = self.github.get_pull_requests(owner, repo)
        for pr_data in prs:
            created_at = datetime.fromisoformat(pr_data["created_at"].replace("Z", "+00:00")) if pr_data.get("created_at") else None
            updated_at = datetime.fromisoformat(pr_data["updated_at"].replace("Z", "+00:00")) if pr_data.get("updated_at") else None
            closed_at = datetime.fromisoformat(pr_data["closed_at"].replace("Z", "+00:00")) if pr_data.get("closed_at") else None
            merged_at = datetime.fromisoformat(pr_data["merged_at"].replace("Z", "+00:00")) if pr_data.get("merged_at") else None
            
            pr = PullRequest(
                repository_id=repository_id,
                github_pr_id=pr_data["id"],
                pr_number=pr_data["number"],
                title=pr_data["title"],
                body=pr_data.get("body"),
                state=pr_data.get("state"),
                author=pr_data["user"]["login"] if pr_data.get("user") else None,
                is_draft=pr_data.get("draft", False),
                is_merged=pr_data.get("merged_at") is not None,
                merge_commit_sha=pr_data.get("merge_commit_sha"),
                commits=pr_data.get("commits", 0),
                additions=pr_data.get("additions", 0),
                deletions=pr_data.get("deletions", 0),
                changed_files=pr_data.get("changed_files", 0),
                comments=pr_data.get("comments", 0),
                review_comments=pr_data.get("review_comments", 0),
                url=pr_data.get("url"),
                html_url=pr_data.get("html_url"),
                created_at=created_at,
                updated_at=updated_at,
                closed_at=closed_at,
                merged_at=merged_at
            )
            self.db.add(pr)

    def ingest_releases(self, owner, repo, repository_id):
        releases = self.github.get_releases(owner, repo)
        for r_data in releases:
            published_at = datetime.fromisoformat(r_data["published_at"].replace("Z", "+00:00")) if r_data.get("published_at") else None
            created_at = datetime.fromisoformat(r_data["created_at"].replace("Z", "+00:00")) if r_data.get("created_at") else None
            
            release = Release(
                repository_id=repository_id,
                github_release_id=r_data["id"],
                tag_name=r_data["tag_name"],
                name=r_data.get("name"),
                body=r_data.get("body"),
                author=r_data["author"]["login"] if r_data.get("author") else None,
                draft=r_data.get("draft", False),
                prerelease=r_data.get("prerelease", False),
                tarball_url=r_data.get("tarball_url"),
                zipball_url=r_data.get("zipball_url"),
                html_url=r_data.get("html_url"),
                published_at=published_at,
                created_at=created_at
            )
            self.db.add(release)

    def ingest_branches(self, owner, repo, repository_id):
        branches = self.github.get_branches(owner, repo)
        for b_data in branches:
            branch = Branch(
                repository_id=repository_id,
                name=b_data["name"],
                protected=b_data.get("protected", False),
                last_commit_sha=b_data["commit"]["sha"] if "commit" in b_data else None,
                last_commit_url=b_data["commit"]["url"] if "commit" in b_data else None
            )
            self.db.add(branch)

    def ingest_tags(self, owner, repo, repository_id):
        tags = self.github.get_tags(owner, repo)
        for t_data in tags:
            tag = Tag(
                repository_id=repository_id,
                name=t_data["name"],
                commit_sha=t_data["commit"]["sha"] if "commit" in t_data else None,
                commit_url=t_data["commit"]["url"] if "commit" in t_data else None,
                zipball_url=t_data.get("zipball_url"),
                tarball_url=t_data.get("tarball_url"),
                node_id=t_data.get("node_id")
            )
            self.db.add(tag)

    def ingest_languages(self, owner, repo, repository_id):
        languages = self.github.get_languages(owner, repo)
        total_bytes = sum(languages.values())
        for lang_name, bytes_code in languages.items():
            percentage = int((bytes_code / total_bytes) * 100) if total_bytes > 0 else 0
            lang = Language(
                repository_id=repository_id,
                language_name=lang_name,
                bytes_of_code=bytes_code,
                percentage=percentage
            )
            self.db.add(lang)

    def run_pipeline(self, owner: str, repo: str, user_id: int = None):
        repository = self.ingest_repository(owner, repo, user_id=user_id)
        self.ingest_contributor(owner, repo, repository.id)
        self.ingest_commits(owner, repo, repository.id)
        self.ingest_issues(owner, repo, repository.id)
        self.ingest_pull_requests(owner, repo, repository.id)
        self.ingest_releases(owner, repo, repository.id)
        self.ingest_branches(owner, repo, repository.id)
        self.ingest_tags(owner, repo, repository.id)
        self.ingest_languages(owner, repo, repository.id)
        self.db.commit()
    
    def close(self):
        self.db.close()