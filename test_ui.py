
import streamlit as st

from ui.components import (
    section_header,
    info_card,
    status_message,
)

st.set_page_config(
    page_title="CareerFlow UI Test",
    layout="wide",
)

st.title("CareerFlow AI — UI Component Test")

section_header(
    "Career Mission",
    "Your AI agents coordinate your career goals.",
    icon="🚀",
)

col1, col2 = st.columns(2)

with col1:
    info_card(
        "Resume Intelligence",
        "Analyze your resume and identify relevant skills.",
        icon="📄",
    )

with col2:
    info_card(
        "Job Discovery",
        "Discover opportunities based on your career goals.",
        icon="🔎",
    )

status_message(
    "UI components loaded successfully.",
    status="success",
)

if st.button("Test button"):
    st.success("Button interaction works.")