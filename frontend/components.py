import streamlit as st

def render_section_header(title, subtitle=None):
    st.subheader(title)
    if subtitle:
        st.caption(subtitle)

def render_hero_banner(title, subtitle):
    st.title(title)
    st.write(subtitle)
    st.divider()

def render_health_score_gauge(score):
    if score >= 75:
        status = "Healthy Repository"
        desc = "Excellent metrics across commits, pull requests, and contributor engagement."
    elif score >= 50:
        status = "Repository Needs Attention"
        desc = "Moderate activity. Minor weaknesses in merge rate or contributor growth."
    else:
        status = "Repository At Risk"
        desc = "Critical developer churn risk or severe decline in activity levels."

    st.metric("GitInsight Health Score", f"{score}/100", delta=status)
    st.caption(desc)
