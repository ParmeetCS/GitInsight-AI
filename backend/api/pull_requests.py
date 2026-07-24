from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import PullRequest, Repository, User
from deps import get_current_user, get_db

router = APIRouter(
    prefix="/pull-requests",
    tags=["Pull Requests"]
)

def verify_repo_owner(repository_id: int, user: User, db: Session):
    repo = db.query(Repository).filter(Repository.id == repository_id, Repository.user_id == user.id).first()
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found.")
    return repo

@router.get("/{repository_id}")
def get_pull_requests(repository_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    verify_repo_owner(repository_id, current_user, db)
    prs = db.query(PullRequest).filter(PullRequest.repository_id == repository_id).all()
    if not prs:
        raise HTTPException(status_code=404, detail="No pull requests found.")
    return prs

@router.get("/{repository_id}/merged")
def merged_pull_requests(repository_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    verify_repo_owner(repository_id, current_user, db)
    return db.query(PullRequest).filter(PullRequest.repository_id == repository_id, PullRequest.is_merged == True).all()

@router.get("/{repository_id}/open")
def open_pull_requests(repository_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    verify_repo_owner(repository_id, current_user, db)
    return db.query(PullRequest).filter(PullRequest.repository_id == repository_id, PullRequest.state == "open").all()