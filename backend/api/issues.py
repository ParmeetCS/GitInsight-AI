from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Issue, Repository, User
from deps import get_current_user, get_db

router = APIRouter(
    prefix="/issues",
    tags=["Issues"]
)

def verify_repo_owner(repository_id: int, user: User, db: Session):
    repo = db.query(Repository).filter(Repository.id == repository_id, Repository.user_id == user.id).first()
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found.")
    return repo

@router.get("/{repository_id}")
def get_issues(repository_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    verify_repo_owner(repository_id, current_user, db)
    issues = db.query(Issue).filter(Issue.repository_id == repository_id).all()
    if not issues:
        raise HTTPException(status_code=404, detail="No issues found.")
    return issues

@router.get("/{repository_id}/open")
def open_issues(repository_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    verify_repo_owner(repository_id, current_user, db)
    return db.query(Issue).filter(Issue.repository_id == repository_id, Issue.state == "open").all()

@router.get("/{repository_id}/closed")
def closed_issues(repository_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    verify_repo_owner(repository_id, current_user, db)
    return db.query(Issue).filter(Issue.repository_id == repository_id, Issue.state == "closed").all()
