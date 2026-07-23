from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from schemas import UserRegister, UserLogin
from services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/register")
def register(user: UserRegister):
    service = AuthService()
    try:
        res = service.register(user.username, user.email, user.password)
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        service.close()

@router.post("/login")
def login(user: UserLogin):
    service = AuthService()
    try:
        token = service.login(user.email, user.password)
        if not token:
            raise HTTPException(status_code=401, detail="Invalid email or password.")
        
        user_info = service.get_current_user(token)
        username = user_info["username"] if user_info else user.email.split("@")[0]
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "username": username
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        service.close()

@router.get("/me")
def current_user(token: str = Depends(oauth2_scheme)):
    service = AuthService()
    try:
        user = service.get_current_user(token)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid or expired token.")
        return user
    finally:
        service.close()
