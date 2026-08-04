# 🚀 GitInsight AI

> **AI-Powered Developer Community Health & Contributor Churn Monitor**

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=flat-square&logo=streamlit)](https://streamlit.io/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL%20%2F%20Neon-4169E1?style=flat-square&logo=postgresql)](https://neon.tech/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-F7931E?style=flat-square&logo=scikit-learn)](https://scikit-learn.org/)
[![OpenRouter](https://img.shields.io/badge/AI-OpenRouter%20LLM-6366F1?style=flat-square)](https://openrouter.ai/)

**GitInsight AI** is an end-to-end, full-stack analytics and predictive intelligence platform engineered for GitHub repositories. It empowers engineering leaders, open-source maintainers, and developer advocates to automatically ingest repository activity, evaluate key community health indicators (such as **Bus Factor**, **Health Score**, **Commit Frequency**, and **Issue Resolution Velocity**), execute **VADER Sentiment Analysis**, predict **contributor churn and repository growth** using machine learning, and interact with a context-aware **AI Repository Assistant** powered by state-of-the-art LLMs.

---

## 🌐 Live Deployments

- 🖥️ **Frontend Dashboard**: [https://gitinsight-ai-fwij96hyhhcqms3nohvvhf.streamlit.app/](https://gitinsight-ai-fwij96hyhhcqms3nohvvhf.streamlit.app/)
- ⚙️ **Backend REST API**: [https://gitinsight-ai-utz2.onrender.com](https://gitinsight-ai-utz2.onrender.com)
- 📑 **Interactive API Docs (Swagger)**: [https://gitinsight-ai-utz2.onrender.com/docs](https://gitinsight-ai-utz2.onrender.com/docs)

---

## 🌟 Key Features

- 🔐 **User Authentication & Session Management**: Secure user registration, password hashing (`bcrypt`), and JWT-based authentication token handling (`python-jose`) for personalized workspace management.
- 🔄 **Automated GitHub Data Ingestion**: Fetch comprehensive entity data using the GitHub REST API, including repositories, commits, contributors, issues, pull requests, releases, branches, tags, and language breakdowns.
- 📊 **Developer Community Health Metrics**: Automatically compute holistic repository health scores (0-100), commit frequencies, PR merge velocity, issue resolution times, community engagement, and critical **Bus Factor** risk metrics.
- 🔮 **Machine Learning Churn & Growth Prediction**: 
  - Predict contributor churn risk (**High / Medium / Low** & **Churn Probability %**) using trained **RandomForest Classifier** models with intelligent heuristic fallbacks.
  - Forecast future repository growth trends and health trajectory scores with a **RandomForest Regressor**.
- 💬 **VADER Sentiment & NLP Analytics**: Perform real-time Natural Language Processing (NLP) sentiment scoring across issue bodies and pull request discussions to detect contributor burnout and community friction early.
- 🤖 **AI Repository Assistant**: Interact with an AI chatbot powered by **OpenRouter LLMs** for deep context-aware Q&A, repository activity summaries, and metric explanations.
- 🎨 **Modern Streamlit Dashboard**: Clean, responsive, multi-page user interface with custom CSS design tokens, Plotly interactive visualizations, search filtering, and user session management.

---

## 🏗 System Architecture

The diagram below illustrates the end-to-end architecture of GitInsight AI, demonstrating interactions across the **Streamlit UI**, **FastAPI Backend**, **PostgreSQL Database**, **Scikit-Learn ML Models**, and **External APIs**:

```mermaid
flowchart TD
    subgraph Client ["Frontend Layer (Streamlit)"]
        UI["Streamlit Web App (app.py)"]
        AUTH_UI["User Auth Manager (auth.py)"]
        P1["Repository Ingestion Page"]
        P2["Community Dashboard"]
        P3["ML Analytics & Churn Page"]
        P4["AI Assistant Chatbot"]
        
        UI --> AUTH_UI
        UI --> P1
        UI --> P2
        UI --> P3
        UI --> P4
    end

    subgraph API ["Backend API Layer (FastAPI & Uvicorn)"]
        MAIN["FastAPI Server (main.py)"]
        R_AUTH["/auth Router"]
        R_REPO["/repository Router"]
        R_ANALYTICS["/analytics Router"]
        R_CHAT["/chatbot Router"]
        R_DATA["/contributors, /commits, /issues, /pull_requests"]
        
        MAIN --> R_AUTH
        MAIN --> R_REPO
        MAIN --> R_ANALYTICS
        MAIN --> R_CHAT
        MAIN --> R_DATA
    end

    subgraph Service ["Service & Security Layer"]
        AUTH_SERV["Auth Service (auth_service.py)"]
        INGEST["Ingestion Pipeline (ingestion_pipeline.py)"]
        GH_CLIENT["GitHub API Client (github_client.py)"]
        ANALYTICS_ENG["Analytics Engine (analytics_services.py)"]
        SENTIMENT["VADER Sentiment Service (sentiment_services.py)"]
        LLM_SERV["LLM Assistant Service (llm_services.py)"]
        
        R_AUTH --> AUTH_SERV
        INGEST --> GH_CLIENT
        ANALYTICS_ENG --> SENTIMENT
    end

    subgraph ML ["Machine Learning Layer"]
        FEATURE["Feature Engineering (feature_engineering.py)"]
        TRAIN["Model Trainer (train.py)"]
        CHURN["Churn Predictor (churn_prediction.py)"]
        GROWTH["Growth Predictor (growth_prediction.py)"]
        
        TRAIN --> FEATURE
        CHURN -. Uses trained model .-> TRAIN
        GROWTH -. Uses trained model .-> TRAIN
    end

    subgraph Storage ["Database Layer (PostgreSQL)"]
        DB[(PostgreSQL Database / Neon)]
        ORM["SQLAlchemy ORM (models.py)"]
        DB <--> ORM
    end

    subgraph External ["External Services"]
        GITHUB["GitHub REST API"]
        OPENROUTER["OpenRouter API (LLM)"]
    end

    %% Client-Backend Connections
    Client <-->|REST API + Bearer Token| API
    
    R_REPO --> INGEST
    R_ANALYTICS --> ANALYTICS_ENG
    R_ANALYTICS --> CHURN
    R_ANALYTICS --> GROWTH
    R_CHAT --> LLM_SERV
    
    INGEST <--> ORM
    ANALYTICS_ENG <--> ORM
    AUTH_SERV <--> ORM
    
    GH_CLIENT <-->|HTTPS / PAT| GITHUB
    LLM_SERV <-->|HTTPS / API Key| OPENROUTER
```

---

## 🔄 Data Ingestion & Machine Learning Pipeline

```mermaid
sequenceDiagram
    autonumber
    actor User as User / Maintainer
    participant UI as Streamlit UI
    participant API as FastAPI Backend
    participant GH as GitHub REST API
    participant DB as PostgreSQL Database
    participant ML as Scikit-Learn ML Engine
    participant LLM as OpenRouter LLM API

    User->>UI: Register / Login
    UI->>API: POST /auth/login
    API-->>UI: Return JWT Access Token
    
    User->>UI: Submit Repository (Owner/Repo)
    UI->>API: POST /repository/ingest (with JWT Token)
    API->>GH: Fetch Repo Details, Commits, PRs, Issues, Contributors, Languages
    GH-->>API: Raw JSON Payload
    API->>DB: Store Repository Entities mapped to User ID
    API-->>UI: Ingestion Success Response

    User->>UI: Request Health & Churn Analysis
    UI->>API: GET /analytics/{repository_id}/churn
    API->>DB: Query Repository Activity Metrics
    DB-->>API: Metric Data & Features
    API->>ML: Evaluate Feature Vector with Random Forest Classifier
    ML-->>API: Return Churn Risk Level & Churn Probability (%)
    API-->>UI: Render Health Cards, Bus Factor & Churn Charts

    User->>UI: Ask Question to AI Assistant
    UI->>API: POST /chatbot/repository/{repository_id}
    API->>DB: Query Repository Context & Activity Summary
    DB-->>API: Contributor, Commit & Issue Data
    API->>LLM: Send Prompt + Repository Context Payload
    LLM-->>API: Generated AI Response
    API-->>UI: Render AI Answer in Chat Window
```

---

## 🗄 Entity Relationship (ER) Diagram

GitInsight AI utilizes a relational database schema built with **SQLAlchemy** and hosted on **PostgreSQL / Neon**. Below is the complete Entity Relationship diagram:

```mermaid
erDiagram
    user ||--o{ repositories : "owns / monitors"
    repositories ||--o{ contributors : "has many"
    repositories ||--o{ commits : "has many"
    repositories ||--o{ issues : "has many"
    repositories ||--o{ pull_requests : "has many"
    repositories ||--o{ releases : "has many"
    repositories ||--o{ branches : "has many"
    repositories ||--o{ tags : "has many"
    repositories ||--o{ languages : "has many"
    repositories ||--|| repository_analytics : "has one"

    user {
        int id PK
        string username UK
        string email UK
        string hashed_password
        datetime created_at
    }

    repositories {
        int id PK
        int user_id FK
        bigint github_id
        string owner
        string name
        string full_name UK
        text description
        string language
        string license
        int stars
        int forks
        int watchers
        int open_issues
        string default_branch
        string html_url
        datetime created_at
        datetime updated_at
    }

    contributors {
        int id PK
        int repository_id FK
        bigint github_id
        string username
        string profile_url
        string avatar_url
        string account_type
        boolean site_admin
        int contributions
        int followers
        int following
        string company
        string location
        string email
        text bio
    }

    commits {
        int id PK
        int repository_id FK
        string sha UK
        string author_name
        string author_username
        string committer_name
        string committer_username
        text message
        string url
        datetime commit_date
    }

    issues {
        int id PK
        int repository_id FK
        bigint github_issue_id UK
        int issue_number
        string title
        text body
        string state
        string author
        string assignee
        int comments
        datetime created_at
        datetime closed_at
    }

    pull_requests {
        int id PK
        int repository_id FK
        bigint github_pr_id UK
        int pr_number
        string title
        text body
        string state
        string author
        boolean is_draft
        boolean is_merged
        int additions
        int deletions
        int changed_files
        datetime created_at
        datetime merged_at
    }

    releases {
        int id PK
        int repository_id FK
        bigint github_release_id UK
        string tag_name
        string name
        text body
        string author
        boolean draft
        boolean prerelease
        datetime published_at
    }

    branches {
        int id PK
        int repository_id FK
        string name
        boolean protected
        string last_commit_sha
    }

    tags {
        int id PK
        int repository_id FK
        string name
        string commit_sha
    }

    languages {
        int id PK
        int repository_id FK
        string language_name
        bigint bytes_of_code
        int percentage
    }

    repository_analytics {
        int id PK
        int repository_id FK, UK
        float health_score
        float commit_frequency
        float contributor_growth
        float contributor_retention
        float merge_rate
        float issue_resolution_time
        float average_pr_merge_time
        float release_frequency
        float community_engagement
        float bus_factor
        datetime last_calculated
    }
```

---

## 📁 Repository Directory Structure

```directory
GitInsight AI/
├── backend/
│   ├── api/
│   │   ├── analytics.py        # REST API endpoints for Health, Churn & Growth ML
│   │   ├── auth.py             # REST API endpoints for User Registration, Login & Profile
│   │   ├── chatbot.py          # REST API endpoints for OpenRouter AI Assistant
│   │   ├── commits.py          # REST API router for commit metrics
│   │   ├── contributors.py     # REST API router for contributor metrics
│   │   ├── issues.py           # REST API router for issue metrics
│   │   ├── pull_requests.py    # REST API router for PR metrics
│   │   └── repository.py       # REST API endpoints for repository ingestion & management
│   ├── ml/
│   │   ├── churn_prediction.py # Contributor churn prediction model & rule fallbacks
│   │   ├── feature_engineering.py # Feature extraction matrix builder for Scikit-Learn
│   │   ├── growth_prediction.py# Repository growth forecasting model
│   │   └── train.py            # Random Forest model training execution script
│   ├── services/
│   │   ├── analytics_services.py # Core health score & metric computation routines
│   │   ├── auth_service.py     # Password hashing (bcrypt) & JWT token manager
│   │   ├── github_client.py    # GitHub REST API client wrapper
│   │   ├── ingestion_pipeline.py # Full repository ETL ingestion workflow
│   │   ├── llm_services.py     # OpenRouter LLM assistant integration
│   │   └── sentiment_services.py # VADER Sentiment analysis engine
│   ├── config.py               # Central environment variable configuration loader
│   ├── create_table.py         # Database schema creation script
│   ├── database.py             # SQLAlchemy engine & session factory
│   ├── deps.py                 # FastAPI dependency injection (JWT auth & DB session)
│   ├── main.py                 # FastAPI application entrypoint & middleware setup
│   ├── migrate_db.py           # Automated schema migration helper
│   ├── models.py               # SQLAlchemy ORM models definitions
│   └── schemas.py              # Pydantic data validation schemas
├── frontend/
│   ├── pages/
│   │   ├── analytics.py        # Interactive Churn & Growth ML UI
│   │   ├── chatbot.py          # AI Repository Assistant conversational interface
│   │   ├── dashboard.py        # Community Health Metrics & Overview Dashboard
│   │   └── repository.py       # GitHub Repository ingestion & selection manager
│   ├── api_client.py           # Streamlit-to-FastAPI HTTP request wrapper
│   ├── app.py                  # Streamlit application main entrypoint & sidebar
│   ├── auth.py                 # Streamlit authentication UI & state manager
│   ├── components.py           # Custom UI cards, badges & banner components
│   └── utils.py                # Streamlit session state and visual helpers
├── .env                        # Local environment variable configuration (ignored by git)
├── .env.example                # Template for required environment variables
├── .gitignore                  # Git repository exclusion rules
└── requirements.txt            # Python dependencies manifest
```

---

## 🛠 Technology Stack

### **Backend & Security**
- **[FastAPI](https://fastapi.tiangolo.com/)**: Modern, high-performance Python web API framework.
- **[Uvicorn](https://www.uvicorn.org/)**: Lightning-fast ASGI web server.
- **[SQLAlchemy](https://www.sqlalchemy.org/)**: Powerful SQL toolkit and Object Relational Mapper (ORM).
- **[PostgreSQL / Neon DB](https://neon.tech/)**: Serverless cloud PostgreSQL relational database.
- **[python-jose](https://python-jose.readthedocs.io/) & [bcrypt](https://pypi.org/project/bcrypt/)**: Secure JWT token generation and salted password hashing.
- **[Pydantic](https://docs.pydantic.dev/)**: Data validation using Python type annotations.

### **Frontend & UI**
- **[Streamlit](https://streamlit.io/)**: Interactive web application framework for Python data apps.
- **[Plotly](https://plotly.com/)**: Rich, interactive data visualizations and analytics charts.

### **Machine Learning & NLP**
- **[Scikit-Learn](https://scikit-learn.org/)**: Machine learning models (**RandomForestClassifier**, **RandomForestRegressor**).
- **[Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/)**: High-performance data manipulation and matrix transformations.
- **[Joblib](https://joblib.readthedocs.io/)**: Model serialization and persistence.
- **[vaderSentiment](https://github.com/cjhutto/vaderSentiment)**: Valence Aware Dictionary for Sentiment Reasoning NLP engine.

### **External APIs**
- **[GitHub REST API](https://docs.github.com/en/rest)**: Live data fetching for commits, PRs, issues, and contributors.
- **[OpenRouter API](https://openrouter.ai/)**: Unified access point for advanced LLM reasoning models.

---

## ⚙️ Environment Configuration

Copy `.env.example` to `.env` in the project root directory and fill in your credential values:

```bash
cp .env.example .env
```

### `.env` File Keys Reference:

```env
# 🔑 GitHub Personal Access Token (PAT) with repo read scope
GITHUB_TOKEN=your_github_personal_access_token

# 🗄 PostgreSQL Database Connection String (Neon PostgreSQL or Local Postgres)
NEON_DATABASE_URL=postgresql://username:password@ep-host.region.aws.neon.tech/neondb?sslmode=require

# 🤖 OpenRouter / OpenAI API Key for AI Repository Assistant
OPENAI_API_KEY=your_openrouter_api_key

# 🔐 Secret Key for JWT Authentication (HS256)
SECRET_KEY=your_random_secret_key_here

# 🌐 Deployment Service URLs
BACKEND_URL=http://127.0.0.1:8000
FRONTEND_URL=http://localhost:8501
```

---

## 🚀 Getting Started

### **Prerequisites**
- **Python 3.9+** installed.
- A **PostgreSQL** database (or a free cloud database on [Neon.tech](https://neon.tech/)).
- A **GitHub Personal Access Token** ([Generate here](https://github.com/settings/tokens)).
- An **OpenRouter API Key** ([Get key here](https://openrouter.ai/keys)).

---

### **1. Clone the Repository & Prepare Environment**

```bash
# Clone the repository
git clone https://github.com/ParmeetCS/GitInsight-AI.git
cd "GitInsight AI"

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS / Linux:
source venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

---

### **2. Set Up Environment Variables**

Create `.env` based on `.env.example`:

```bash
# Copy example configuration template
cp .env.example .env
```

Edit `.env` with your actual `GITHUB_TOKEN`, `NEON_DATABASE_URL`, `OPENAI_API_KEY`, and `SECRET_KEY`.

---

### **3. Initialize Database Tables**

Run the database setup script to apply database schema and migrations:

```bash
python backend/create_table.py
```

---

### **4. Train Machine Learning Models (Optional)**

Train the Scikit-Learn Random Forest Growth and Churn models:

```bash
python backend/ml/train.py
```

> *Note: If pre-trained model files are missing, GitInsight AI automatically uses intelligent heuristic calculation engines.*

---

### **5. Run the FastAPI Backend Server**

Start the FastAPI application server locally on `http://127.0.0.1:8000`:

```bash
uvicorn backend.main:app --reload --port 8000
```

Access the interactive Swagger API documentation at: **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**.

---

### **6. Run the Streamlit Frontend Dashboard**

In a new terminal window (with the virtual environment activated):

```bash
streamlit run frontend/app.py
```

The Streamlit dashboard will automatically launch at **`http://localhost:8501`**.

---

## 📌 API Reference Summary

| Category | Endpoint | Method | Security | Description |
| :--- | :--- | :---: | :---: | :--- |
| **System** | `/health` | `GET` | Public | System health check endpoint |
| **Auth** | `/auth/register` | `POST` | Public | Register a new user account |
| **Auth** | `/auth/login` | `POST` | Public | Authenticate user & return JWT Bearer token |
| **Auth** | `/auth/me` | `GET` | Bearer Auth | Retrieve currently authenticated user profile |
| **Repository** | `/repository/ingest` | `POST` | Bearer Auth | Ingest repository data from GitHub (`owner`, `repo`) |
| **Repository** | `/repository/` | `GET` | Bearer Auth | List user's ingested repositories |
| **Repository** | `/repository/{owner}/{repo}` | `GET` | Bearer Auth | Fetch specific repository details |
| **Repository** | `/repository/refresh` | `POST` | Bearer Auth | Re-ingest and update repository data |
| **Repository** | `/repository/{id}/languages` | `GET` | Bearer Auth | Get language breakdown statistics |
| **Analytics** | `/analytics/{id}` | `POST` | Public | Compute and store repository health metrics |
| **Analytics** | `/analytics/{id}` | `GET` | Public | Fetch computed repository health metrics |
| **Analytics** | `/analytics/{id}/churn` | `GET` | Public | Predict contributor churn probability & risk level |
| **Analytics** | `/analytics/{id}/growth` | `GET` | Public | Forecast predicted growth & trajectory score |
| **Chatbot** | `/chatbot/repository/{id}` | `POST` | Public | Query AI Assistant with custom question |
| **Chatbot** | `/chatbot/explain` | `POST` | Public | Request AI explanation of repository metrics |
| **Data** | `/commits/{id}` | `GET` | Public | Retrieve repository commit history |
| **Data** | `/contributors/{id}` | `GET` | Public | Retrieve contributor activity metrics |
| **Data** | `/issues/{id}` | `GET` | Public | Retrieve issue metrics & sentiment |
| **Data** | `/pull_requests/{id}` | `GET` | Public | Retrieve pull request metrics & sentiment |

---

## 📈 Community Health Score & Churn Methodology

1. **Community Health Score (0-100)**: Evaluated using a weighted blend of:
   - **Commit Frequency**: Consistency and volume of recent code commits.
   - **PR Merge Rate & Velocity**: Ratio of merged vs. unmerged pull requests and average time-to-merge.
   - **Issue Resolution Time**: Average duration required to triage and close open issues.
   - **Contributor Growth & Retention**: Active contributor velocity over time.
2. **Bus Factor Risk**: Quantifies contributor dependency. A low Bus Factor flags critical knowledge concentration risk among very few active maintainers.
3. **Contributor Churn Prediction**: Combines Random Forest classification with commit drop-off trends, issue resolution velocity, and release cadences to produce **Low**, **Medium**, or **High** risk levels with explicit churn probabilities.

---

## 🤝 Contributing

Contributions are warmly welcome! To contribute:
1. **Fork** the repository.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the Branch (`git push origin feature/AmazingFeature`).
5. Open a **Pull Request**.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.
