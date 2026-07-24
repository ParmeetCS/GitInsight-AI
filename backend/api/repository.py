from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from services.ingestion_pipeline import IngestionServices
from database import SessionLocal
from models import Repository, Language, User
from deps import get_current_user, get_db

router = APIRouter(
    prefix="/repository",
    tags=["Repository"]
)

class RespositoryRequest(BaseModel):
    owner: str
    repo: str

@router.post("/ingest")
def ingest_repository(request: RespositoryRequest, current_user: User = Depends(get_current_user)):
    service = IngestionServices()
    try:
        service.run_pipeline(owner=request.owner, repo=request.repo, user_id=current_user.id)
        return {
            "status": "success",
            "message": "Repository data ingested successfully.",
            "repository": f"{request.owner}/{request.repo}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        service.close()

@router.get("/{owner}/{repo}")
def get_repository(owner: str, repo: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    repository = db.query(Repository).filter(
        Repository.owner.ilike(owner),
        Repository.name.ilike(repo),
        Repository.user_id == current_user.id
    ).first()
    if not repository:
        raise HTTPException(status_code=404, detail="Repository not found.")
    return repository

@router.post("/refresh")
def refresh_repository(request: RespositoryRequest, current_user: User = Depends(get_current_user)):
    service = IngestionServices()
    try:
        service.run_pipeline(owner=request.owner, repo=request.repo, user_id=current_user.id)
        return {
            "status": "success",
            "message": "Repository refreshed successfully."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        service.close()

@router.get("/")
def list_repositories(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Repository).filter(Repository.user_id == current_user.id).all()

@router.get("/{repository_id}/languages")
def get_repository_languages(repository_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    repository = db.query(Repository).filter(
        Repository.id == repository_id,
        Repository.user_id == current_user.id
    ).first()
    if not repository:
        raise HTTPException(status_code=404, detail="Repository not found.")
    return db.query(Language).filter(Language.repository_id == repository_id).all()
