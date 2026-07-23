import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ===========================
# Database
# ===========================
DATABASE_URL = os.getenv("DATABASE_URL")

# ===========================
# GitHub
# ===========================
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# ===========================
# Gemini
# ===========================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ===========================
# JWT Authentication
# ===========================
SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60