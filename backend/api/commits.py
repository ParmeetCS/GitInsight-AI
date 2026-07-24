from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Commit, Repository, User
from deps import get_current_user, get_db

router = APIRouter(
    prefix="/commits",
    tags=["Commits"]
)

def verify_repo_owner(repository_id: int, user: User, db: Session):
    repo = db.query(Repository).filter(Repository.id == repository_id, Repository.user_id == user.id).first()
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found.")
    return repo

@router.get("/{repository_id}")
def get_commits(repository_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    verify_repo_owner(repository_id, current_user, db)
    commits = db.query(Commit).filter(Commit.repository_id == repository_id).all()
    if not commits:
        raise HTTPException(status_code=404, detail="No commits found.")
    return commits

@router.get("/{repository_id}/recent")
def recent_commits(repository_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    verify_repo_owner(repository_id, current_user, db)
    return db.query(Commit).filter(Commit.repository_id == repository_id).order_by(Commit.commit_date.desc()).limit(10).all()

@router.get("/{repository_id}/{sha}")
def get_commit(repository_id: int, sha: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    verify_repo_owner(repository_id, current_user, db)
    commit = db.query(Commit).filter(Commit.repository_id == repository_id, Commit.sha == sha).first()
    if not commit:
        raise HTTPException(status_code=404, detail="Commit not found.")
    return commit