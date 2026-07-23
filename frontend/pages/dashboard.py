import streamlit as st
import requests
from components import render_hero_banner, render_section_header, render_health_score_gauge

st.set_page_config(
    page_title="GitInsight AI | Dashboard",
    page_icon="🚀",
    layout="wide"
)

BACKEND_URL = "http://127.0.0.1:8000"

render_hero_banner(
    "Project Health Dashboard",
    "View community metrics, activity status, and overall project health score."
)

if not st.session_state.get("active_repo"):
    st.info("No active repository selected. Please go to Home or Repository page to select one.")
else:
    repo = st.session_state.active_repo
    repo_id = repo["id"]
    
    analytics = None
    try:
        res = requests.get(f"{BACKEND_URL}/analytics/{repo_id}")
        if res.status_code == 200:
            analytics = res.json()
        elif res.status_code == 404:
            gen_res = requests.post(f"{BACKEND_URL}/analytics/{repo_id}")
            if gen_res.status_code == 200:
                res = requests.get(f"{BACKEND_URL}/analytics/{repo_id}")
                if res.status_code == 200:
                    analytics = res.json()
    except Exception:
        st.error("Error communicating with backend API.")
        
    col_left, col_right = st.columns([1, 2])
    
    with col_left:
        render_section_header("Community Health Summary")
        if analytics:
            health_score = int(analytics.get("health_score", 0))
            render_health_score_gauge(health_score)
        else:
            st.warning("Could not load health analytics.")
            if st.button("Generate Analytics"):
                requests.post(f"{BACKEND_URL}/analytics/{repo_id}")
                st.rerun()
                
        st.subheader("Metadata Info")
        st.write(f"**Full Name:** {repo['full_name']}")
        st.write(f"**Language:** {repo.get('language') or 'N/A'}")
        st.write(f"**Default Branch:** {repo.get('default_branch') or 'main'}")
        st.write(f"**License:** {repo.get('license') or 'None'}")
        st.write(f"**ID:** {repo['id']}")

    with col_right:
        render_section_header("Repository Metrics")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Stars", f"{repo.get('stars', 0):,}")
        c2.metric("Forks", f"{repo.get('forks', 0):,}")
        c3.metric("Watchers", f"{repo.get('watchers', 0):,}")
        c4.metric("Open Issues", f"{repo.get('open_issues', 0):,}")
            
        render_section_header("Analytics Metrics")
        
        if analytics:
            ac1, ac2, ac3, ac4 = st.columns(4)
            ac1.metric("Bus Factor", int(analytics.get('bus_factor', 0)))
            ac2.metric("Commit Frequency", int(analytics.get('commit_frequency', 0)))
            ac3.metric("PR Merge Rate", f"{analytics.get('merge_rate', 0.0):.1f}%")
            ac4.metric("Releases", int(analytics.get('release_frequency', 0)))
                
            st.subheader("Insight Summary")
            h = analytics.get("health_score", 0)
            if h >= 75:
                explanation = f"**{repo['full_name']}** has a very strong ecosystem with a health score of **{h}/100**. Bus Factor: {analytics.get('bus_factor')}, PR merge rate: {analytics.get('merge_rate'):.1f}%."
            elif h >= 50:
                explanation = f"**{repo['full_name']}** shows moderate project activity with a health score of **{h}/100**. Bus Factor: {analytics.get('bus_factor')}."
            else:
                explanation = f"**{repo['full_name']}** has a critical health score of **{h}/100**. High risk of developer abandonment."
                
            st.info(explanation)
        else:
            st.info("No analytics data loaded. Refresh repository data on Repository page.")
