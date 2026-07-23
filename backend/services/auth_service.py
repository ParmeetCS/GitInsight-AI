import bcrypt
from datetime import datetime, timedelta

from jose import jwt, JWTError
from sqlalchemy.orm import Session

from database import SessionLocal
from models import User
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


class AuthService:

    def __init__(self):
        self.db: Session = SessionLocal()

    # -----------------------------------------
    # Hash Password
    # -----------------------------------------

    def hash_password(self, password: str):
        pwd_bytes = password.encode("utf-8")[:72]
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(pwd_bytes, salt)
        return hashed.decode("utf-8")

    # -----------------------------------------
    # Verify Password
    # -----------------------------------------

    def verify_password(
        self,
        plain_password: str,
        hashed_password: str
    ):
        pwd_bytes = plain_password.encode("utf-8")[:72]
        hashed_bytes = hashed_password.encode("utf-8")
        try:
            return bcrypt.checkpw(pwd_bytes, hashed_bytes)
        except Exception:
            return False

    # -----------------------------------------
    # Create JWT Token
    # -----------------------------------------

    def create_access_token(
        self,
        data: dict
    ):

        to_encode = data.copy()

        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

        to_encode.update(
            {"exp": expire}
        )

        token = jwt.encode(
            to_encode,
            SECRET_KEY,
            algorithm=ALGORITHM
        )

        return token

    # -----------------------------------------
    # Register User
    # -----------------------------------------

    def register(
        self,
        username: str,
        email: str,
        password: str
    ):

        existing_user = self.db.query(User).filter(
            User.email == email
        ).first()

        if existing_user:
            raise ValueError("Email already registered.")

        user = User(
            username=username,
            email=email,
            hashed_password=self.hash_password(password)
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }

    # -----------------------------------------
    # Login
    # -----------------------------------------

    def login(
        self,
        email: str,
        password: str
    ):

        user = self.db.query(User).filter(
            User.email == email
        ).first()

        if user is None:
            return None

        if not self.verify_password(
            password,
            user.hashed_password
        ):
            return None

        token = self.create_access_token(
            {
                "sub": user.email
            }
        )

        return token

    # -----------------------------------------
    # Current User
    # -----------------------------------------

    def get_current_user(
        self,
        token: str
    ):

        try:

            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )

            email = payload.get("sub")

            if email is None:
                return None

        except JWTError:
            return None

        user = self.db.query(User).filter(
            User.email == email
        ).first()

        if user is None:
            return None

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }

    # -----------------------------------------
    # Close Session
    # -----------------------------------------

    def close(self):

        self.db.close()