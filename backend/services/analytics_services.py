from sqlalchemy.orm import Session
from database import SessionLocal
from models import Repository, Contributor, Commit, Issue, PullRequest, Release, RepositoryAnalytics

class AnalyticsService:

    def __init__(self):
        self.db: Session = SessionLocal()

    def get_repository(self, repository_id: int):
        return self.db.query(Repository).filter(Repository.id == repository_id).first()

    def calculate_analytics(self, repository_id: int):
        repository = self.get_repository(repository_id)
        if not repository:
            return None

        existing_analytics = self.db.query(RepositoryAnalytics).filter(
            RepositoryAnalytics.repository_id == repository_id
        ).first()
        if existing_analytics:
            self.db.delete(existing_analytics)
            self.db.commit()

        contributors = self.db.query(Contributor).filter(Contributor.repository_id == repository_id).count()
        commits = self.db.query(Commit).filter(Commit.repository_id == repository_id).count()
        issues = self.db.query(Issue).filter(Issue.repository_id == repository_id).count()
        closed_issues = self.db.query(Issue).filter(Issue.repository_id == repository_id, Issue.state == "closed").count()
        pull_requests = self.db.query(PullRequest).filter(PullRequest.repository_id == repository_id).count()
        merged_prs = self.db.query(PullRequest).filter(PullRequest.repository_id == repository_id, PullRequest.is_merged == True).count()
        releases = self.db.query(Release).filter(Release.repository_id == repository_id).count()

        merge_rate = (merged_prs / pull_requests * 100) if pull_requests else 0
        issue_resolution_rate = (closed_issues / issues * 100) if issues else 0
        commit_frequency = commits
        community_engagement = contributors * 10
        release_frequency = releases
        bus_factor = contributors

        health_score = round(
            (merge_rate + issue_resolution_rate + commit_frequency + community_engagement + release_frequency + bus_factor) / 6,
            2
        )

        analytics = RepositoryAnalytics(
            repository_id=repository_id,
            health_score=health_score,
            commit_frequency=commit_frequency,
            contributor_growth=contributors,
            contributor_retention=100,
            merge_rate=merge_rate,
            issue_resolution_time=issue_resolution_rate,
            average_pr_merge_time=0,
            release_frequency=release_frequency,
            community_engagement=community_engagement,
            bus_factor=bus_factor
        )

        self.db.add(analytics)
        self.db.commit()
        return analytics

    def get_analytics(self, repository_id: int):
        return self.db.query(RepositoryAnalytics).filter(RepositoryAnalytics.repository_id == repository_id).first()

    def close(self):
        self.db.close()