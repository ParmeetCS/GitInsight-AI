import pandas as pd
from sqlalchemy.orm import Session

from database import SessionLocal

from models import(
    Repository,
    Contributor,
    Commit,
    Issue,
    PullRequest,
    Release,
    RepositoryAnalytics
)

class FeatureEngineering:

    def __init__(self):
        self.db: Session = SessionLocal()

    def create_dataset(self):
        """
        Create ML dataset from database.
        One row = One repository.
        """

        repositories = self.db.query(Repository).all()

        dataset = []

        for repo in repositories:

            contributors = self.db.query(Contributor).filter(
                Contributor.repository_id == repo.id
            ).count()

            commits = self.db.query(Commit).filter(
                Commit.repository_id == repo.id
            ).count()

            issues = self.db.query(Issue).filter(
                Issue.repository_id == repo.id
            ).count()

            closed_issues = self.db.query(Issue).filter(
                Issue.repository_id == repo.id,
                Issue.state == "closed"
            ).count()

            pull_requests = self.db.query(PullRequest).filter(
                PullRequest.repository_id == repo.id
            ).count()

            merged_prs = self.db.query(PullRequest).filter(
                PullRequest.repository_id == repo.id,
                PullRequest.is_merged == True
            ).count()

            releases = self.db.query(Release).filter(
                Release.repository_id == repo.id
            ).count()

            analytics = self.db.query(RepositoryAnalytics).filter(
                RepositoryAnalytics.repository_id == repo.id
            ).first()

            row = {

                "repository_id": repo.id,
                "repository": repo.full_name,

                "stars": repo.stars,
                "forks": repo.forks,
                "watchers": repo.watchers,

                "contributors": contributors,

                "commits": commits,

                "issues": issues,

                "closed_issues": closed_issues,

                "pull_requests": pull_requests,

                "merged_prs": merged_prs,

                "releases": releases,

                "health_score": (
                    analytics.health_score
                    if analytics else 0
                ),

                "merge_rate": (
                    analytics.merge_rate
                    if analytics else 0
                ),

                "community_engagement": (
                    analytics.community_engagement
                    if analytics else 0
                )
            }

            dataset.append(row)

        return pd.DataFrame(dataset)

    def save_dataset(self, filename="repository_features.csv"):

        df = self.create_dataset()

        df.to_csv(filename, index=False)

        return df

    def close(self):
        self.db.close()


if __name__ == "__main__":

    fe = FeatureEngineering()

    df = fe.save_dataset()

    print(df.head())

    fe.close()