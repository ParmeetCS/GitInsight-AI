import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ===========================
# Database
# ===========================
DATABASE_URL = os.getenv("NEON_DATABASE_URL") or os.getenv("DATABASE_URL")

# ===========================
# GitHub
# ===========================
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# ===========================
# LLM / OpenRouter API Key
# ===========================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ===========================
# JWT Authentication
# ===========================
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ===========================
# Service URLs
# ===========================
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8501").rstrip("/")