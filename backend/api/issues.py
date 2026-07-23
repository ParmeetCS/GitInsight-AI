from fastapi import APIRouter, HTTPException
from database import SessionLocal
from models import Issue

router = APIRouter(
    prefix="/issues",
    tags=["Issues"]
)

@router.get("/{repository_id}")
def get_issues(repository_id: int):
    db = SessionLocal()
    try:
        issues = db.query(Issue).filter(Issue.repository_id == repository_id).all()
        if not issues:
            raise HTTPException(status_code=404, detail="No issues found.")
        return issues
    finally:
        db.close()

@router.get("/{repository_id}/open")
def open_issues(repository_id: int):
    db = SessionLocal()
    try:
        return db.query(Issue).filter(Issue.repository_id == repository_id, Issue.state == "open").all()
    finally:
        db.close()

@router.get("/{repository_id}/closed")
def closed_issues(repository_id: int):
    db = SessionLocal()
    try:
        return db.query(Issue).filter(Issue.repository_id == repository_id, Issue.state == "closed").all()
    finally:
        db.close()
