# 🚀 GitInsight AI

> **AI-Powered Developer Community Health & Contributor Churn Monitor**

GitInsight AI is an advanced, full-stack analytics and predictive intelligence platform engineered for GitHub repositories. It enables engineering leaders, open-source maintainers, and community managers to automatically ingest repository metrics, evaluate health indicators (such as **Bus Factor**, **Health Score**, and **Issue Resolution Velocity**), run **VADER Sentiment Analysis**, predict **contributor churn and repository growth** using machine learning, and interact with an **AI Repository Assistant** powered by LLMs.

---

## 🌟 Key Features

- 🔄 **Automated GitHub Data Ingestion**: Seamlessly fetch repositories, commits, contributors, issues, pull requests, releases, branches, tags, and language breakdowns using the GitHub REST API.
- 📊 **Developer Community Health Metrics**: Calculate holistic health scores (0-100), commit frequencies, PR merge rates, issue resolution times, community engagement, and critical **Bus Factor** risks.
- 🔮 **Machine Learning Churn & Growth Prediction**: 
  - Predict contributor churn risk (High / Medium / Low & Probability %) using trained Scikit-Learn **RandomForest Classifier** models with heuristic fallbacks.
  - Forecast future repository growth and health score trajectories with **RandomForest Regressor**.
- 💬 **VADER Sentiment & NLP Analytics**: Evaluate community sentiment across issues and pull requests to spot contributor burnout or toxic discussions early.
- 🤖 **AI Repository Chatbot**: Ask questions about active contributors, commit history, open issues, and repository health summaries powered by **OpenRouter LLM (GPT Models)**.
- 🎨 **Modern Streamlit Dashboard**: Clean, responsive multi-page dashboard featuring interactive data visualizations, repository controls, and real-time analytical insights.

---

## 🏗 System Architecture

The following diagram illustrates the architecture of GitInsight AI, showing how the **Streamlit Frontend**, **FastAPI Backend**, **PostgreSQL Database**, **Scikit-Learn ML Engines**, and **External APIs** interact:

```mermaid
flowchart TD
    subgraph Client ["Frontend Layer (Streamlit)"]
        UI["Streamlit Web App (app.py)"]
        P1["Repository Ingestion Page"]
        P2["Community Dashboard"]
        P3["ML Analytics & Churn Page"]
        P4["AI Assistant Chatbot"]
        UI --> P1
        UI --> P2
        UI --> P3
        UI --> P4
    end

    subgraph API ["Backend API Layer (FastAPI & Uvicorn)"]
        MAIN["FastAPI Server (main.py)"]
        R_REPO["/repository Router"]
        R_ANALYTICS["/analytics Router"]
        R_CHAT["/chatbot Router"]
        R_DATA["/contributors, /commits, /issues, /pull_requests"]
        
        MAIN --> R_REPO
        MAIN --> R_ANALYTICS
        MAIN --> R_CHAT
        MAIN --> R_DATA
    end

    subgraph Service ["Service & Analytics Layer"]
        INGEST["Ingestion Pipeline (ingestion_pipeline.py)"]
        GH_CLIENT["GitHub API Client (github_client.py)"]
        ANALYTICS_ENG["Analytics Engine (analytics_services.py)"]
        SENTIMENT["VADER Sentiment Service (sentiment_services.py)"]
        LLM_SERV["LLM Assistant Service (llm_services.py)"]
        
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

    %% Flow connections
    Client <-->|REST Requests| API
    R_REPO --> INGEST
    R_ANALYTICS --> ANALYTICS_ENG
    R_ANALYTICS --> CHURN
    R_ANALYTICS --> GROWTH
    R_CHAT --> LLM_SERV
    
    INGEST <--> ORM
    ANALYTICS_ENG <--> ORM
    
    GH_CLIENT <-->|HTTPS / PAT| GITHUB
    LLM_SERV <-->|OpenAI SDK / HTTP| OPENROUTER
```

---

## 🔄 Data Ingestion & Machine Learning Pipeline

The diagram below outlines the end-to-end data lifecycle from GitHub API ingestion to database storage, feature extraction, ML model evaluation, and final visualization:

```mermaid
sequenceDiagram
    autonumber
    actor User as Maintainer / User
    participant UI as Streamlit UI
    participant API as FastAPI Backend
    participant GH as GitHub REST API
    participant DB as PostgreSQL Database
    participant ML as ML & Analytics Engine
    participant LLM as OpenRouter LLM API

    User->>UI: Input Repository (Owner/Repo)
    UI->>API: POST /repository/ingest
    API->>GH: Fetch Repo Details, Commits, PRs, Issues, Contributors
    GH-->>API: Raw JSON Payload
    API->>DB: Upsert Repository Entities & Metadata
    API-->>UI: Ingestion Success Response

    User->>UI: Request Analytics & Churn Prediction
    UI->>API: GET /analytics/{repository_id}/churn
    API->>DB: Query Repository Features & Metrics
    DB-->>API: Metrics & Counts
    API->>ML: Pass Feature Vector to Random Forest Classifier
    ML-->>API: Churn Risk Level & Churn Probability (%)
    API-->>UI: Display Health Score, Bus Factor & Churn Cards

    User->>UI: Ask Question in AI Assistant
    UI->>API: POST /chatbot/repository/{repository_id}
    API->>DB: Retrieve Summary Context & Recent Activity
    DB-->>API: Top Contributors, Issues & Commits
    API->>LLM: Send Prompt + Context Payload
    LLM-->>API: Generated AI Insight Response
    API-->>UI: Display Chatbot Answer
```

---

## 🗄 Entity Relationship (ER) Diagram

GitInsight AI utilizes a relational schema built with **SQLAlchemy** and hosted on **PostgreSQL**. Below is the complete Entity Relationship diagram showing relationships across repositories, contributors, commits, issues, PRs, releases, branches, tags, languages, and calculated analytics:

```mermaid
erDiagram
    repositories ||--o{ contributors : "has many"
    repositories ||--o{ commits : "has many"
    repositories ||--o{ issues : "has many"
    repositories ||--o{ pull_requests : "has many"
    repositories ||--o{ releases : "has many"
    repositories ||--o{ branches : "has many"
    repositories ||--o{ tags : "has many"
    repositories ||--o{ languages : "has many"
    repositories ||--|| repository_analytics : "has one"

    repositories {
        int id PK
        bigint github_id UK
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
│   │   ├── chatbot.py          # REST API endpoints for OpenRouter LLM Chatbot
│   │   ├── commits.py          # Commits API router
│   │   ├── contributors.py     # Contributors API router
│   │   ├── issues.py           # Issues API router
│   │   ├── pull_requests.py    # Pull Requests API router
│   │   └── repository.py       # Repository ingestion and query router
│   ├── ml/
│   │   ├── churn_prediction.py # Contributor churn prediction model & rules
│   │   ├── feature_engineering.py # Data extraction & dataset builder for ML
│   │   ├── growth_prediction.py# Growth prediction model & heuristics
│   │   └── train.py            # Random Forest training script
│   ├── services/
│   │   ├── analytics_services.py # Core repository health metric computations
│   │   ├── github_client.py    # GitHub REST API client wrapper
│   │   ├── ingestion_pipeline.py # Full repository ETL ingestion workflow
│   │   ├── llm_services.py     # OpenRouter LLM integration
│   │   └── sentiment_services.py # VADER Sentiment analysis engine
│   ├── create_table.py         # SQLAlchemy database table creation script
│   ├── database.py             # Database engine & session management
│   ├── main.py                 # FastAPI application entrypoint
│   ├── models.py               # SQLAlchemy ORM models
│   └── schemas.py              # Pydantic validation schemas
├── frontend/
│   ├── pages/
│   │   ├── analytics.py        # Interactive Charts & Churn Risk UI
│   │   ├── chatbot.py          # AI Assistant conversation interface
│   │   ├── dashboard.py        # Community Health Dashboard
│   │   └── repository.py       # GitHub Repository ingestion manager
│   ├── app.py                  # Streamlit frontend entrypoint
│   └── components.py           # Reusable UI banners, cards & styled headers
├── .env                        # Environment variable configuration
├── .gitignore                  # Git ignore rules
└── requirements.txt            # Python dependencies manifest
```

---

## 🛠 Technology Stack

### **Backend & API**
- **[FastAPI](https://fastapi.tiangolo.com/)**: Asynchronous, high-performance Python web API framework.
- **[Uvicorn](https://www.uvicorn.org/)**: Lightning-fast ASGI server implementation.
- **[SQLAlchemy](https://www.sqlalchemy.org/)**: SQL toolkit and Object Relational Mapper (ORM).
- **[PostgreSQL / Neon DB](https://neon.tech/)**: Serverless cloud PostgreSQL database storage.
- **[Pydantic](https://docs.pydantic.dev/)**: Data validation and settings management using Python type annotations.

### **Frontend & UI**
- **[Streamlit](https://streamlit.io/)**: Interactive web application framework for data science and ML.
- **[Plotly / Streamlit Components](https://plotly.com/)**: Rich data visualization charts and metrics cards.

### **Machine Learning & NLP**
- **[Scikit-Learn](https://scikit-learn.org/)**: Machine learning algorithms (**RandomForestRegressor**, **RandomForestClassifier**).
- **[Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/)**: High-performance data manipulation and feature matrix construction.
- **[Joblib](https://joblib.readthedocs.io/)**: Serialization and persistence of trained ML models.
- **[vaderSentiment](https://github.com/cjhutto/vaderSentiment)**: Rule-based sentiment analysis for issue & PR text.

### **External APIs & Integrations**
- **[GitHub REST API](https://docs.github.com/en/rest)**: Direct data extraction for repository activity.
- **[OpenRouter API](https://openrouter.ai/)**: Unified LLM endpoint accessing state-of-the-art AI models.

---

## ⚙️ Environment Configuration

Create a `.env` file in the root directory of the repository with the following configuration keys:

```env
# GitHub Personal Access Token (PAT) with repo scope
GITHUB_TOKEN=your_github_personal_access_token

# Database Connection URL (PostgreSQL)
DATABASE_URL=postgresql://username:password@ep-host.region.aws.neon.tech/neondb?sslmode=require

# OpenRouter API Key for AI Chatbot Insights
OPENAI_API_KEY=your_openrouter_api_key
```

---

## 🚀 Getting Started

Follow these step-by-step instructions to get GitInsight AI up and running on your local machine.

### **Prerequisites**
- **Python 3.9+** installed.
- A **PostgreSQL** database (or a free cloud instance on [Neon.tech](https://neon.tech/)).
- A **GitHub Personal Access Token** ([Generate here](https://github.com/settings/tokens)).
- An **OpenRouter API Key** ([Get key here](https://openrouter.ai/keys)).

---

### **1. Clone the Repository & Set Up Environment**

```bash
# Clone repository
git clone https://github.com/ParmeetCS/GitInsight-AI.git
cd "GitInsight AI"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### **2. Initialize Database Tables**

Run the database setup script to create all SQLAlchemy schema tables in PostgreSQL:

```bash
python backend/create_table.py
```

---

### **3. Train Machine Learning Models (Optional)**

To train the Scikit-Learn Random Forest Growth and Churn models on ingested data:

```bash
python backend/ml/train.py
```

> *Note: If model files (`growth_model.pkl` or `churn_model.pkl`) are not present, the system automatically falls back to robust heuristic scoring algorithms.*

---

### **4. Start the FastAPI Backend Server**

Launch the backend REST API server on `http://127.0.0.1:8000`:

```bash
uvicorn backend.main:app --reload --port 8000
```

You can view the interactive OpenAPI documentation at **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**.

---

### **5. Start the Streamlit Frontend Dashboard**

In a separate terminal window (with your virtual environment active):

```bash
streamlit run frontend/app.py
```

The dashboard will open automatically in your default browser at **`http://localhost:8501`**.

---

## 📌 API Reference Summary

Below is an overview of key REST API endpoints provided by the backend:

| Category | Endpoint | Method | Description |
| :--- | :--- | :---: | :--- |
| **System** | `/health` | `GET` | Health check endpoint |
| **Repository** | `/repository/ingest` | `POST` | Ingest repository from GitHub (`owner`, `repo`) |
| **Repository** | `/repository/` | `GET` | List all ingested repositories |
| **Repository** | `/repository/{owner}/{repo}` | `GET` | Fetch details for a specific repository |
| **Analytics** | `/analytics/{repository_id}` | `POST` | Trigger calculation of health & engagement metrics |
| **Analytics** | `/analytics/{repository_id}` | `GET` | Fetch computed repository metrics |
| **Analytics** | `/analytics/{repository_id}/churn` | `GET` | Predict contributor churn probability & risk level |
| **Analytics** | `/analytics/{repository_id}/growth` | `GET` | Forecast predicted health & growth score |
| **Chatbot** | `/chatbot/repository/{repository_id}` | `POST` | Query AI Repository Assistant with custom question |

---

## 📈 Community Health Score & Churn Methodology

1. **Community Health Score (0-100)**: Evaluated using a weighted blend of:
   - **Commit Frequency**: Frequency and consistency of recent code updates.
   - **PR Merge Rate & Velocity**: Ratio of merged vs. abandoned pull requests and time-to-merge.
   - **Issue Resolution Time**: Average time required to triage and close issues.
   - **Contributor Growth & Retention**: Active contributor trend over time.
2. **Bus Factor Risk**: Measures key contributor concentration. A low Bus Factor signifies that critical knowledge is concentrated in too few maintainers.
3. **Contributor Churn Prediction**: Combines Random Forest classification with commit drop-off metrics, issue resolution velocity, and release activity to output a **Low**, **Medium**, or **High** risk profile with an exact churn percentage.

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for details.

---

## 🤝 Contributing

Contributions are welcome! If you'd like to improve GitInsight AI:
1. Fork the Project.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the Branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

<p align="center">
  Made with ❤️ by <b>GitInsight AI Team</b>
</p>
