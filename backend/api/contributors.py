from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Contributor, Repository, User
from deps import get_current_user, get_db

router = APIRouter(
    prefix="/contributors",
    tags=["contributors"]
)

def verify_repo_owner(repository_id: int, user: User, db: Session):
    repo = db.query(Repository).filter(Repository.id == repository_id, Repository.user_id == user.id).first()
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found.")
    return repo

@router.get("/{repository_id}")
def get_contributors(repository_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    verify_repo_owner(repository_id, current_user, db)
    contributors = db.query(Contributor).filter(Contributor.repository_id == repository_id).all()
    if not contributors:
        raise HTTPException(status_code=404, detail="No contributor found.")
    return contributors

@router.get("/{repository_id}/{username}")
def get_contributor(repository_id: int, username: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    verify_repo_owner(repository_id, current_user, db)
    contributor = db.query(Contributor).filter(Contributor.repository_id == repository_id, Contributor.username == username).first()
    if not contributor:
        raise HTTPException(status_code=404, detail="Contributor not found.")
    return contributor