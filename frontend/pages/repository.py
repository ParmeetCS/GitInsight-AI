import streamlit as st
import requests
from components import render_hero_banner, render_section_header

st.set_page_config(
    page_title="GitInsight AI | Manage Repositories",
    page_icon="🚀",
    layout="wide"
)

BACKEND_URL = "http://127.0.0.1:8000"

render_hero_banner(
    "Ingest & Manage Repositories",
    "Enter a public GitHub repository path (e.g. 'langchain-ai/langchain') to fetch, parse, and analyze it."
)

col1, col2 = st.columns([1, 2])

with col1:
    render_section_header("Ingest New Repository")
    
    with st.form("ingestion_form"):
        owner_input = st.text_input("Repository Owner", placeholder="e.g., langchain-ai")
        repo_input = st.text_input("Repository Name", placeholder="e.g., langchain")
        submit_button = st.form_submit_button("Start Ingestion")
        
    if submit_button:
        if not owner_input.strip() or not repo_input.strip():
            st.error("Please enter both Owner and Repository Name.")
        else:
            with st.spinner("Ingesting repository... Please wait."):
                try:
                    res = requests.post(
                        f"{BACKEND_URL}/repository/ingest",
                        json={"owner": owner_input.strip(), "repo": repo_input.strip()}
                    )
                    if res.status_code == 200:
                        repo_details = requests.get(f"{BACKEND_URL}/repository/{owner_input.strip()}/{repo_input.strip()}")
                        if repo_details.status_code == 200:
                            repo_data = repo_details.json()
                            requests.post(f"{BACKEND_URL}/analytics/{repo_data['id']}")
                            st.success(f"Ingested and analyzed **{owner_input}/{repo_input}**!")
                            st.session_state.selected_repo_name = f"{repo_data['owner']}/{repo_data['name']}"
                            st.session_state.active_repo = repo_data
                            st.rerun()
                        else:
                            st.warning("Repository ingested, but failed to fetch details for analytics.")
                    else:
                        st.error(f"Ingestion failed: {res.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Error: {e}")

with col2:
    render_section_header("Ingested Projects Database")
    try:
        res = requests.get(f"{BACKEND_URL}/repository/")
        if res.status_code == 200:
            repos_list = res.json()
            if not repos_list:
                st.info("No repositories ingested yet.")
            else:
                display_data = []
                for r in repos_list:
                    active_label = "✅ Active" if st.session_state.get("selected_repo_name") == f"{r['owner']}/{r['name']}" else "Selectable"
                    display_data.append({
                        "Repository": f"{r['owner']}/{r['name']}",
                        "Language": r.get("language") or "N/A",
                        "Stars": f"{r.get('stars', 0):,}",
                        "Forks": f"{r.get('forks', 0):,}",
                        "Watchers": f"{r.get('watchers', 0):,}",
                        "Status": active_label
                    })
                st.dataframe(display_data, use_container_width=True, hide_index=True)
                
                st.subheader("Actions")
                selected_to_active = st.selectbox(
                    "Select Repository to Make Active",
                    options=[f"{r['owner']}/{r['name']}" for r in repos_list]
                )
                
                action_col1, action_col2 = st.columns(2)
                with action_col1:
                    if st.button("Set Active"):
                        repo_options = {f"{r['owner']}/{r['name']}": r for r in repos_list}
                        st.session_state.selected_repo_name = selected_to_active
                        st.session_state.active_repo = repo_options[selected_to_active]
                        st.success(f"Active repository set to **{selected_to_active}**")
                        st.rerun()
                with action_col2:
                    if st.button("Refresh Active Data"):
                        active_repo = st.session_state.get("active_repo")
                        if active_repo:
                            with st.spinner("Refreshing..."):
                                refresh_res = requests.post(
                                    f"{BACKEND_URL}/repository/refresh",
                                    json={"owner": active_repo["owner"], "repo": active_repo["name"]}
                                )
                                if refresh_res.status_code == 200:
                                    requests.post(f"{BACKEND_URL}/analytics/{active_repo['id']}")
                                    st.success("Refreshed repository and analytics!")
                                    st.rerun()
                                else:
                                    st.error("Failed to refresh data.")
                        else:
                            st.warning("Please set an active repository first.")
        else:
            st.error("Failed to load repositories.")
    except Exception as e:
        st.error(f"Backend API error: {e}")
