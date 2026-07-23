import os
import sys
import streamlit as st
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from components import render_hero_banner, render_section_header
from auth import Auth

st.set_page_config(
    page_title="GitInsight AI | Repository Assistant",
    page_icon="🚀",
    layout="wide"
)

if not Auth.is_authenticated():
    st.error("🔒 Authentication Required")
    st.info("Please log in or register on the **Home** page to access the AI Chatbot Assistant.")
    st.stop()

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

def get_headers():
    token = Auth.get_token()
    return {"Authorization": f"Bearer {token}"} if token else {}

render_hero_banner(
    "AI Repository Chat Assistant",
    "Interact with our LLM assistant to ask repository questions, request summaries, or analyze community health."
)

if not st.session_state.get("active_repo"):
    st.info("No active repository selected. Please go to Home or Repository page.")
else:
    repo = st.session_state.active_repo
    repo_id = repo["id"]
    
    chat_key = f"chat_history_{repo_id}"
    if chat_key not in st.session_state:
        st.session_state[chat_key] = [
            {"role": "assistant", "content": f"Hello! Ask me anything about **{repo['full_name']}**!"}
        ]
        
    col_chat, col_shortcuts = st.columns([3, 1])
    
    with col_chat:
        render_section_header("Chat Feed")
        
        for msg in st.session_state[chat_key]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                
        user_input = st.chat_input("Ask a question about this repository...")
        
        if "shortcut_trigger" in st.session_state and st.session_state.shortcut_trigger:
            user_input = st.session_state.shortcut_trigger
            del st.session_state.shortcut_trigger
            
        if user_input:
            st.session_state[chat_key].append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)
                
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        res = requests.post(
                            f"{BACKEND_URL}/chatbot/repository/{repo_id}",
                            json={"question": user_input},
                            headers=get_headers()
                        )
                        if res.status_code == 200:
                            ans = res.json().get("response", "No response received.")
                            st.write(ans)
                            st.session_state[chat_key].append({"role": "assistant", "content": ans})
                        else:
                            st.error("Failed to fetch answer from backend.")
                    except Exception as e:
                        st.error(f"Error: {e}")
            st.rerun()

    with col_shortcuts:
        render_section_header("Quick Templates")
        templates = [
            "Summarize the overall health of this repository.",
            "Who are the top contributors and what are their contribution shares?",
            "Explain the codebase language distribution and sizes.",
            "What is the status of the pull request backlog and merge rate?",
            "Provide 3 actionable recommendations to improve community health."
        ]
        
        for t in templates:
            if st.button(t, key=t, use_container_width=True):
                st.session_state.shortcut_trigger = t
                st.rerun()
                
        st.divider()
        if st.button("Clear Chat History", use_container_width=True):
            st.session_state[chat_key] = [
                {"role": "assistant", "content": f"Chat log cleared. How can I help with **{repo['full_name']}**?"}
            ]
            st.rerun()
