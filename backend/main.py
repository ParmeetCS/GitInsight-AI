import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)
    sys.path.append(os.path.join(current_dir, "services"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.contributors import router as contributors_router
from api.commits import router as commits_router
from api.issues import router as issues_router
from api.pull_requests import router as pull_requests_router
from database import engine
from models import Base
from api.repository import router as repository_router
from api.analytics import router as analytics_router
from api.chatbot import router as chatbot_router
from api.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GitInsight AI",
    description="AI-Powered Developer Community Health Monitor",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Welcome to GitInsight AI 🚀", "status": "Running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

app.include_router(repository_router)
app.include_router(contributors_router)
app.include_router(commits_router)
app.include_router(issues_router)
app.include_router(pull_requests_router)
app.include_router(analytics_router)
app.include_router(chatbot_router)
app.include_router(auth_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)