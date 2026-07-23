import os
import sys
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from components import render_hero_banner, render_section_header
from auth import Auth

st.set_page_config(
    page_title="GitInsight AI | Analytics & Predictions",
    page_icon="🚀",
    layout="wide"
)

if not Auth.is_authenticated():
    st.error("🔒 Authentication Required")
    st.info("Please log in or register on the **Home** page to access Analytics & ML Predictions.")
    st.stop()

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

def get_headers():
    token = Auth.get_token()
    return {"Authorization": f"Bearer {token}"} if token else {}

render_hero_banner(
    "Visual Analytics & Machine Learning Predictions",
    "Review commit frequencies, PR statuses, issue logs, language breakdowns, and ML predictions."
)

if not st.session_state.get("active_repo"):
    st.info("No active repository selected. Please go to Home or Repository page.")
else:
    repo = st.session_state.active_repo
    repo_id = repo["id"]
    
    render_section_header("Machine Learning Predictions")
    
    pred_col1, pred_col2 = st.columns(2)
    
    with pred_col1:
        st.subheader("Contributor Churn Prediction")
        try:
            res = requests.get(f"{BACKEND_URL}/analytics/{repo_id}/churn", headers=get_headers())
            if res.status_code == 200:
                churn_data = res.json()
                risk = churn_data.get("risk", "Medium")
                prob = churn_data.get("churn_probability", 50.0)
                
                st.metric(f"Churn Risk: {risk}", f"{prob:.1f}%")
                st.info(f"Contributor Churn is modeled at {prob:.1f}% probability with {risk} risk.")
            else:
                st.error("Could not fetch churn prediction.")
        except Exception as e:
            st.error(f"Error: {e}")
            
    with pred_col2:
        st.subheader("Future Health Score Trend")
        try:
            growth_res = requests.get(f"{BACKEND_URL}/analytics/{repo_id}/growth", headers=get_headers())
            analytics_res = requests.get(f"{BACKEND_URL}/analytics/{repo_id}", headers=get_headers())
            
            if growth_res.status_code == 200 and analytics_res.status_code == 200:
                predicted_score = growth_res.json().get("predicted_health_score", 50.0)
                current_score = analytics_res.json().get("health_score", 50.0)
                delta = round(predicted_score - current_score, 2)
                
                st.metric("Predicted Health Score", f"{predicted_score:.1f}", delta=f"{delta}")
                st.info(f"Health score is forecast to reach {predicted_score:.1f} (change of {delta}).")
            else:
                st.error("Could not fetch growth prediction.")
        except Exception as e:
            st.error(f"Error: {e}")
            
    st.divider()
    render_section_header("Repository Analytics & Activity Charts")
    
    row1_col1, row1_col2 = st.columns(2)
    
    with row1_col1:
        st.subheader("Commit Activity Over Time")
        try:
            res = requests.get(f"{BACKEND_URL}/commits/{repo_id}", headers=get_headers())
            if res.status_code == 200 and res.json():
                df_commits = pd.DataFrame(res.json())
                df_commits['commit_date'] = pd.to_datetime(df_commits['commit_date'])
                df_grouped = df_commits.groupby(df_commits['commit_date'].dt.date).size().reset_index(name='commits')
                df_grouped = df_grouped.sort_values('commit_date')
                
                fig_line = px.line(df_grouped, x='commit_date', y='commits', labels={'commit_date': 'Date', 'commits': 'Commits'})
                st.plotly_chart(fig_line, use_container_width=True)
            else:
                st.info("No commit logs found.")
        except Exception as e:
            st.error(f"Error loading commits: {e}")
            
    with row1_col2:
        st.subheader("Code Language Distribution")
        try:
            res = requests.get(f"{BACKEND_URL}/repository/{repo_id}/languages", headers=get_headers())
            if res.status_code == 200 and res.json():
                df_langs = pd.DataFrame(res.json())
                fig_pie = px.pie(df_langs, names='language_name', values='bytes_of_code', hole=0.4)
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("No language data found.")
        except Exception as e:
            st.error(f"Error loading languages: {e}")
            
    row2_col1, row2_col2 = st.columns(2)
    
    with row2_col1:
        st.subheader("Issue Backlog Status")
        try:
            res = requests.get(f"{BACKEND_URL}/issues/{repo_id}", headers=get_headers())
            if res.status_code == 200 and res.json():
                df_issues = pd.DataFrame(res.json())
                state_counts = df_issues['state'].value_counts().reset_index()
                state_counts.columns = ['state', 'count']
                fig_issues = px.pie(state_counts, names='state', values='count', hole=0.3)
                st.plotly_chart(fig_issues, use_container_width=True)
            else:
                st.info("No issues found.")
        except Exception as e:
            st.error(f"Error loading issues: {e}")
            
    with row2_col2:
        st.subheader("Pull Request Review States")
        try:
            res = requests.get(f"{BACKEND_URL}/pull-requests/{repo_id}", headers=get_headers())
            if res.status_code == 200 and res.json():
                df_prs = pd.DataFrame(res.json())
                df_prs['status'] = df_prs.apply(
                    lambda r: 'merged' if r['is_merged'] else ('open' if r['state'] == 'open' else 'closed'), axis=1
                )
                pr_counts = df_prs['status'].value_counts().reset_index()
                pr_counts.columns = ['status', 'count']
                fig_prs = px.bar(pr_counts, x='status', y='count', color='status')
                st.plotly_chart(fig_prs, use_container_width=True)
            else:
                st.info("No pull requests found.")
        except Exception as e:
            st.error(f"Error loading pull requests: {e}")
            
    st.subheader("Contributor Contribution Shares")
    try:
        res = requests.get(f"{BACKEND_URL}/contributors/{repo_id}", headers=get_headers())
        if res.status_code == 200 and res.json():
            df_contrib = pd.DataFrame(res.json()).sort_values('contributions', ascending=False).head(15)
            fig_contrib = px.bar(df_contrib, y='username', x='contributions', orientation='h')
            st.plotly_chart(fig_contrib, use_container_width=True)
        else:
            st.info("No contributors found.")
    except Exception as e:
        st.error(f"Error loading contributors: {e}")
