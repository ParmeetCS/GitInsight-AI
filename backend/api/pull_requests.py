from fastapi import APIRouter, HTTPException
from database import SessionLocal
from models import PullRequest

router = APIRouter(
    prefix="/pull-requests",
    tags=["Pull Requests"]
)

@router.get("/{repository_id}")
def get_pull_requests(repository_id: int):
    db = SessionLocal()
    try:
        prs = db.query(PullRequest).filter(PullRequest.repository_id == repository_id).all()
        if not prs:
            raise HTTPException(status_code=404, detail="No pull requests found.")
        return prs
    finally:
        db.close()

@router.get("/{repository_id}/merged")
def merged_pull_requests(repository_id: int):
    db = SessionLocal()
    try:
        return db.query(PullRequest).filter(PullRequest.repository_id == repository_id, PullRequest.is_merged == True).all()
    finally:
        db.close()

@router.get("/{repository_id}/open")
def open_pull_requests(repository_id: int):
    db = SessionLocal()
    try:
        return db.query(PullRequest).filter(PullRequest.repository_id == repository_id, PullRequest.state == "open").all()
    finally:
        db.close()