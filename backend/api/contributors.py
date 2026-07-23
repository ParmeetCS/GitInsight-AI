from fastapi import APIRouter, HTTPException
from database import SessionLocal
from models import Contributor

router = APIRouter(
    prefix="/contributors",
    tags=["contributors"]
)

@router.get("/{repository_id}")
def get_contributors(repository_id: int):
    db = SessionLocal()
    try:
        contributors = db.query(Contributor).filter(Contributor.repository_id == repository_id).all()
        if not contributors:
            raise HTTPException(status_code=404, detail="No contributor found.")
        return contributors
    finally:
        db.close()

@router.get("/{repository_id}/{username}")
def get_contributor(repository_id: int, username: str):
    db = SessionLocal()
    try:
        contributor = db.query(Contributor).filter(Contributor.repository_id == repository_id, Contributor.username == username).first()
        if not contributor:
            raise HTTPException(status_code=404, detail="Contributor not found.")
        return contributor
    finally:
        db.close()