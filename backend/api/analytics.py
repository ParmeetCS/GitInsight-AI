from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from services.analytics_services import AnalyticsService
from models import Repository, Contributor, Commit, Issue, PullRequest, RepositoryAnalytics, User
from ml.churn_prediction import ChurnPredictor
from ml.growth_prediction import GrowthPredictor
from deps import get_current_user, get_db

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.post("/{repository_id}")
def generate_analytics(repository_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    repo = db.query(Repository).filter(Repository.id == repository_id, Repository.user_id == current_user.id).first()
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found.")
    
    service = AnalyticsService()
    try:
        analytics = service.calculate_analytics(repository_id)
        if analytics is None:
            raise HTTPException(status_code=404, detail="Repository not found.")
        return {"message": "Analytics generated successfully."}
    finally:
        service.close()

@router.get("/{repository_id}")
def get_analytics(repository_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    repo = db.query(Repository).filter(Repository.id == repository_id, Repository.user_id == current_user.id).first()
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found.")
    
    service = AnalyticsService()
    try:
        analytics = service.get_analytics(repository_id)
        if analytics is None:
            raise HTTPException(status_code=404, detail="Analytics not found.")
        return analytics
    finally:
        service.close()

@router.get("/{repository_id}/churn")
def predict_churn(repository_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    repo = db.query(Repository).filter(Repository.id == repository_id, Repository.user_id == current_user.id).first()
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found.")

    contributors = db.query(Contributor).filter(Contributor.repository_id == repository_id).count()
    commits = db.query(Commit).filter(Commit.repository_id == repository_id).count()
    issues = db.query(Issue).filter(Issue.repository_id == repository_id).count()
    closed_issues = db.query(Issue).filter(Issue.repository_id == repository_id, Issue.state == "closed").count()
    pull_requests = db.query(PullRequest).filter(PullRequest.repository_id == repository_id).count()
    merged_prs = db.query(PullRequest).filter(PullRequest.repository_id == repository_id, PullRequest.is_merged == True).count()
    releases_count = len(repo.releases)

    analytics = db.query(RepositoryAnalytics).filter(RepositoryAnalytics.repository_id == repository_id).first()
    merge_rate = analytics.merge_rate if analytics else 0.0
    community_engagement = analytics.community_engagement if analytics else 0.0

    predictor = ChurnPredictor()
    prediction = predictor.predict(
        stars=repo.stars,
        forks=repo.forks,
        watchers=repo.watchers,
        contributors=contributors,
        commits=commits,
        issues=issues,
        closed_issues=closed_issues,
        pull_requests=pull_requests,
        merged_prs=merged_prs,
        releases=releases_count,
        merge_rate=merge_rate,
        community_engagement=community_engagement
    )

    prob = prediction.get("churn_probability", 50.0)
    if "prediction" in prediction:
        risk = "High" if prediction["prediction"] == 1 else "Low"
        status = "Repository At Risk" if prediction["prediction"] == 1 else "Healthy Repository"
    else:
        risk = prediction.get("risk", "Medium")
        status = prediction.get("status", "Repository Needs Attention")

    return {
        "risk": risk,
        "status": status,
        "churn_probability": prob
    }

@router.get("/{repository_id}/growth")
def predict_growth(repository_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    repo = db.query(Repository).filter(Repository.id == repository_id, Repository.user_id == current_user.id).first()
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found.")

    contributors = db.query(Contributor).filter(Contributor.repository_id == repository_id).count()
    commits = db.query(Commit).filter(Commit.repository_id == repository_id).count()
    issues = db.query(Issue).filter(Issue.repository_id == repository_id).count()
    closed_issues = db.query(Issue).filter(Issue.repository_id == repository_id, Issue.state == "closed").count()
    pull_requests = db.query(PullRequest).filter(PullRequest.repository_id == repository_id).count()
    merged_prs = db.query(PullRequest).filter(PullRequest.repository_id == repository_id, PullRequest.is_merged == True).count()
    releases_count = len(repo.releases)

    analytics = db.query(RepositoryAnalytics).filter(RepositoryAnalytics.repository_id == repository_id).first()
    merge_rate = analytics.merge_rate if analytics else 0.0
    community_engagement = analytics.community_engagement if analytics else 0.0

    predictor = GrowthPredictor()
    predicted_health = predictor.predict(
        stars=repo.stars,
        forks=repo.forks,
        watchers=repo.watchers,
        contributors=contributors,
        commits=commits,
        issues=issues,
        closed_issues=closed_issues,
        pull_requests=pull_requests,
        merged_prs=merged_prs,
        releases=releases_count,
        merge_rate=merge_rate,
        community_engagement=community_engagement
    )

    return {"predicted_health_score": predicted_health}