from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.ingestion_pipeline import IngestionServices
from database import SessionLocal
from models import Repository, Language

router = APIRouter(
    prefix="/repository",
    tags=["Repository"]
)

class RespositoryRequest(BaseModel):
    owner: str
    repo: str

@router.post("/ingest")
def ingest_repository(request: RespositoryRequest):
    service = IngestionServices()
    try:
        service.run_pipeline(owner=request.owner, repo=request.repo)
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
def get_repository(owner: str, repo: str):
    db = SessionLocal()
    try:
        repository = db.query(Repository).filter(
            Repository.owner.ilike(owner),
            Repository.name.ilike(repo)
        ).first()
        if not repository:
            raise HTTPException(status_code=404, detail="Repository not found.")
        return repository
    finally:
        db.close()

@router.post("/refresh")
def refresh_repository(request: RespositoryRequest):
    service = IngestionServices()
    try:
        service.run_pipeline(owner=request.owner, repo=request.repo)
        return {
            "status": "success",
            "message": "Repository refreshed successfully."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        service.close()

@router.get("/")
def list_repositories():
    db = SessionLocal()
    try:
        return db.query(Repository).all()
    finally:
        db.close()

@router.get("/{repository_id}/languages")
def get_repository_languages(repository_id: int):
    db = SessionLocal()
    try:
        return db.query(Language).filter(Language.repository_id == repository_id).all()
    finally:
        db.close()
