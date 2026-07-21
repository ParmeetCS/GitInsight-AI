import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")

engine=create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
)
SessionLocal=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


# For testing purpose 
from sqlalchemy import text
from database import engine

with engine.connect() as conn:
    result = conn.execute(text("SELECT version();"))
    print(result.fetchone())