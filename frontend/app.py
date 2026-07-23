import os
import streamlit as st
import requests
from components import render_hero_banner, render_section_header
from api_client import APIClient
from auth import Auth

st.set_page_config(
    page_title="GitInsight AI | Developer Health Monitor",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

# -----------------------------------------------------------------------------
# Authentication Guard
# -----------------------------------------------------------------------------
if not Auth.is_authenticated():
    st.title("Welcome to GitInsight AI 🚀")
    st.write("AI-Powered Developer Community Health & Contributor Churn Monitor")
    st.divider()

    tab_login, tab_register = st.tabs(["🔑 Login", "📝 Register"])

    with tab_login:
        st.subheader("Login to your account")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login", type="primary", key="btn_login"):
            if not email or not password:
                st.error("Please enter both email and password.")
            else:
                try:
                    res = APIClient.login(email, password)
                    if res is not None and res.status_code == 200:
                        data = res.json()
                        if isinstance(data, dict):
                            token = data.get("access_token")
                            if token:
                                username = data.get("username", email.split("@")[0])
                                Auth.login(token, username)
                                st.success("Logged in successfully!")
                                st.rerun()
                            else:
                                st.error("Login failed: Access token missing in server response.")
                        else:
                            st.error("Login failed: Invalid server response format.")
                    else:
                        err_msg = "Invalid email or password."
                        if res is not None:
                            try:
                                data = res.json()
                                if isinstance(data, dict):
                                    err_msg = data.get("detail", err_msg)
                            except Exception:
                                pass
                        st.error(f"Login failed: {err_msg}")
                except Exception as e:
                    st.error(f"Could not connect to backend server: {e}")

    with tab_register:
        st.subheader("Create a new account")
        reg_username = st.text_input("Username", key="reg_username")
        reg_email = st.text_input("Email", key="reg_email")
        reg_password = st.text_input("Password", type="password", key="reg_password")
        if st.button("Register", type="primary", key="btn_register"):
            if not reg_username or not reg_email or not reg_password:
                st.error("Please fill in all fields.")
            else:
                try:
                    res = APIClient.register(reg_username, reg_email, reg_password)
                    if res is not None and res.status_code in (200, 201):
                        st.success("Account registered successfully! Please log in.")
                    else:
                        err_msg = "Registration failed."
                        if res is not None:
                            try:
                                data = res.json()
                                if isinstance(data, dict):
                                    err_msg = data.get("detail", err_msg)
                            except Exception:
                                pass
                        st.error(f"Registration failed: {err_msg}")
                except Exception as e:
                    st.error(f"Could not connect to backend server: {e}")

    st.stop()


# -----------------------------------------------------------------------------
# Authenticated Application View
# -----------------------------------------------------------------------------
def get_all_repositories():
    try:
        token = Auth.get_token()
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        response = requests.get(f"{BACKEND_URL}/repository/", headers=headers)
        if response.status_code == 200:
            return response.json()
    except Exception:
        st.error(f"Could not connect to backend at {BACKEND_URL}.")
    return []


# Sidebar Controls
st.sidebar.title("GitInsight AI")
st.sidebar.caption("Developer Community Health Monitor")

username = Auth.get_username()
if username:
    st.sidebar.write(f"👤 **Logged in as:** `{username}`")

if st.sidebar.button("🚪 Logout", key="btn_logout"):
    Auth.logout()
    st.rerun()

st.sidebar.divider()

repos = get_all_repositories()

if repos:
    repo_options = {f"{r['owner']}/{r['name']}": r for r in repos}
    
    if "selected_repo_name" not in st.session_state:
        st.session_state.selected_repo_name = list(repo_options.keys())[0]
        
    selected_name = st.sidebar.selectbox(
        "Active Repository",
        options=list(repo_options.keys()),
        index=list(repo_options.keys()).index(st.session_state.selected_repo_name) if st.session_state.selected_repo_name in repo_options else 0
    )
    
    st.session_state.selected_repo_name = selected_name
    st.session_state.active_repo = repo_options[selected_name]
else:
    st.sidebar.warning("No ingested repositories found. Go to 'Repository' page to ingest data.")
    st.session_state.active_repo = None
    st.session_state.selected_repo_name = None

st.sidebar.divider()
st.sidebar.info("Navigation: Select pages from sidebar to view details, charts, and chatbot.")

# Hero Banner
render_hero_banner(
    "AI-Powered Developer Health & Churn Monitor",
    "Analyze git repository patterns, project engagement metrics, and community health. Leverage machine learning to predict contributor churn and monitor community health."
)

# Active Repository Overview & Features
if st.session_state.active_repo:
    repo = st.session_state.active_repo
    col1, col2 = st.columns([2, 1])
    
    with col1:
        render_section_header("Active Repository Overview")
        st.write(f"### {repo['full_name']}")
        st.write(repo['description'] or "No description provided.")
        st.write(f"**Primary Language:** {repo['language'] or 'N/A'}")
        st.write(f"**Default Branch:** {repo['default_branch'] or 'main'}")
        st.write(f"**License:** {repo['license'] or 'None'}")
        st.link_button("View on GitHub ↗", repo['html_url'])
        
        st.write("---")
        st.write("### Explore Features")
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            st.subheader("📊 Repository Dashboard")
            st.write("View high-level repository stats (Stars, Forks, Watchers) and community health metrics like health score, release frequency, and bus factor.")
        with f_col2:
            st.subheader("📈 Deep ML Analytics")
            st.write("Interact with charts of commit frequencies, PR merge rates, issue resolutions, and ML-powered developer churn risk predictions.")
    
    with col2:
        render_section_header("How it Works")
        st.subheader("Community Health Score")
        st.write("A score from 0-100 built by evaluating commit activity, contributor growth, PR merge times, and issue resolution velocity.")
        st.subheader("Developer Churn Risk")
        st.write("Forecasts the probability of a developer leaving the project or becoming inactive.")
        st.subheader("Bus Factor")
        st.write("Reflects knowledge distribution. Low bus factor indicates high dependency on single developers.")
else:
    st.info("Welcome! No repository ingested yet. Go to the Repository page to ingest a repository.")
