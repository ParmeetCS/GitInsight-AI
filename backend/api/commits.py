from fastapi import APIRouter, HTTPException
from database import SessionLocal
from models import Commit

router = APIRouter(
    prefix="/commits",
    tags=["Commits"]
)

@router.get("/{repository_id}")
def get_commits(repository_id: int):
    db = SessionLocal()
    try:
        commits = db.query(Commit).filter(Commit.repository_id == repository_id).all()
        if not commits:
            raise HTTPException(status_code=404, detail="No commits found.")
        return commits
    finally:
        db.close()

@router.get("/{repository_id}/recent")
def recent_commits(repository_id: int):
    db = SessionLocal()
    try:
        return db.query(Commit).filter(Commit.repository_id == repository_id).order_by(Commit.commit_date.desc()).limit(10).all()
    finally:
        db.close()

@router.get("/{repository_id}/{sha}")
def get_commit(repository_id: int, sha: str):
    db = SessionLocal()
    try:
        commit = db.query(Commit).filter(Commit.repository_id == repository_id, Commit.sha == sha).first()
        if not commit:
            raise HTTPException(status_code=404, detail="Commit not found.")
        return commit
    finally:
        db.close()