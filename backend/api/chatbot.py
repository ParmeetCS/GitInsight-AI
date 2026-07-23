from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import SessionLocal
from models import Repository, Contributor, Commit, Issue, PullRequest, RepositoryAnalytics
from services.llm_services import LLMService

router = APIRouter(
    prefix="/chatbot",
    tags=["Chatbot"]
)

class ChatRequest(BaseModel):
    question: str

@router.post("/repository/{repository_id}")
def chat_about_repository(repository_id: int, request: ChatRequest):
    db = SessionLocal()
    llm = LLMService()

    try:
        repo = db.query(Repository).filter(Repository.id == repository_id).first()
        if not repo:
            raise HTTPException(status_code=404, detail="Repository not found.")

        contributors = db.query(Contributor).filter(Contributor.repository_id == repository_id).order_by(Contributor.contributions.desc()).limit(10).all()
        contrib_list = [f"- {c.username} ({c.contributions} contributions)" for c in contributors]
        contrib_str = "\n".join(contrib_list) if contrib_list else "No contributor data"

        commits = db.query(Commit).filter(Commit.repository_id == repository_id).order_by(Commit.commit_date.desc()).limit(5).all()
        commit_list = [f"- {c.author_username or c.author_name}: {c.message[:100]} ({c.commit_date.strftime('%Y-%m-%d') if c.commit_date else 'N/A'})" for c in commits]
        commit_str = "\n".join(commit_list) if commit_list else "No commit data"

        total_issues = db.query(Issue).filter(Issue.repository_id == repository_id).count()
        open_issues = db.query(Issue).filter(Issue.repository_id == repository_id, Issue.state == "open").count()
        closed_issues = total_issues - open_issues

        total_prs = db.query(PullRequest).filter(PullRequest.repository_id == repository_id).count()
        open_prs = db.query(PullRequest).filter(PullRequest.repository_id == repository_id, PullRequest.state == "open").count()
        merged_prs = db.query(PullRequest).filter(PullRequest.repository_id == repository_id, PullRequest.is_merged == True).count()

        analytics = db.query(RepositoryAnalytics).filter(RepositoryAnalytics.repository_id == repository_id).first()

        repo_data = {
            "name": repo.name,
            "owner": repo.owner,
            "full_name": repo.full_name,
            "description": repo.description,
            "language": repo.language,
            "stars": repo.stars,
            "forks": repo.forks,
            "watchers": repo.watchers,
            "open_issues_count": repo.open_issues,
            "default_branch": repo.default_branch,
            "html_url": repo.html_url,
            "health_summary": {
                "health_score": f"Health Score: {analytics.health_score if analytics else 'N/A'}/100",
                "bus_factor": f"Bus Factor: {analytics.bus_factor if analytics else 'N/A'}",
                "commit_frequency": f"Commit Frequency Score: {analytics.commit_frequency if analytics else 'N/A'}",
                "community_engagement": f"Community Engagement: {analytics.community_engagement if analytics else 'N/A'}"
            },
            "contributors": contrib_str,
            "recent_commits": commit_str,
            "issues": f"Total: {total_issues}, Open: {open_issues}, Closed: {closed_issues}",
            "pull_requests": f"Total: {total_prs}, Open: {open_prs}, Merged: {merged_prs}"
        }

        response = llm.repository_chat(repo_data, request.question)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
