import streamlit as st

from database.db import initialize_database

from views.dashboard import show_dashboard
from views.mission import show_mission
from views.resume import show_resume
from views.jobs import show_jobs
from views.matches import show_matches
from views.applications import show_applications
from views.scores import show_scores
from views.analytics import show_analytics
from views.settings import show_settings
from views.interview import show_interview
from views.career import show_career
from views.agent_activity import show_agent_activity
from views.applications import (
    show_applications,
    show_application_queue,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CareerFlow AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# GLOBAL DESIGN SYSTEM
# ============================================================

st.markdown(
    """
<style>

/* ============================================================
   MAIN APPLICATION
   ============================================================ */

.stApp {
    background: #f8fafc;
}

.main .block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* ============================================================
   MAIN TYPOGRAPHY
   ============================================================ */

h1,
h2,
h3,
h4 {
    color: #0f172a;
    letter-spacing: -0.02em;
}

p {
    color: #475569;
}


/* ============================================================
   SIDEBAR CONTAINER
   ============================================================ */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #07101f 0%,
            #0b1424 48%,
            #101a2c 100%
        );

    border-right:
        1px solid #243149;

    min-width: 285px;
    max-width: 305px;
}


/* ============================================================
   SIDEBAR INNER CONTENT
   ============================================================ */

section[data-testid="stSidebar"] > div {

    padding-top: 1.25rem;
    padding-left: 1rem;
    padding-right: 1rem;
    padding-bottom: 1.5rem;
}


/* ============================================================
   IMPORTANT:
   FORCE ALL SIDEBAR MARKDOWN TEXT TO BE VISIBLE
   ============================================================ */

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] h4 {

    color: #ffffff !important;

    opacity: 1 !important;
}


/* Sidebar normal text */

section[data-testid="stSidebar"] p {

    color: #dbeafe !important;

    opacity: 1 !important;
}


/* Sidebar captions */

section[data-testid="stSidebar"]
div[data-testid="stCaptionContainer"] p {

    color: #cbd5e1 !important;

    font-size: 12px !important;

    line-height: 1.5 !important;

    opacity: 1 !important;
}


/* ============================================================
   SIDEBAR BRAND
   ============================================================ */

section[data-testid="stSidebar"] h1 {

    font-size: 25px !important;

    font-weight: 800 !important;

    line-height: 1.15 !important;

    letter-spacing: -0.5px !important;

    margin-top: 0.15rem !important;

    margin-bottom: 0.35rem !important;

    color: #ffffff !important;
}


/* ============================================================
   SIDEBAR TAGLINE
   ============================================================ */

section[data-testid="stSidebar"]
div[data-testid="stCaptionContainer"]:first-of-type p {

    color: #cbd5e1 !important;

    font-size: 12px !important;

    font-weight: 500 !important;

    line-height: 1.45 !important;
}


/* ============================================================
   SIDEBAR DIVIDERS
   ============================================================ */

section[data-testid="stSidebar"] hr {

    border-color:
        rgba(255,255,255,0.12) !important;

    margin-top: 16px !important;

    margin-bottom: 16px !important;
}


/* ============================================================
   WORKSPACE LABEL
   ============================================================ */

section[data-testid="stSidebar"]
div[data-testid="stCaptionContainer"] p {

    color: #a5b4fc !important;

    font-size: 11px !important;

    font-weight: 800 !important;

    letter-spacing: 0.12em !important;

    line-height: 1.4 !important;
}


/* ============================================================
   SIDEBAR NAVIGATION
   ============================================================ */

section[data-testid="stSidebar"]
div[data-testid="stRadio"] {

    width: 100%;
}


/* Navigation item */

section[data-testid="stSidebar"]
div[data-testid="stRadio"] label {

    min-height: 42px !important;

    padding:
        8px 11px !important;

    margin:
        3px 0 !important;

    border-radius:
        9px !important;

    transition:
        background 0.15s ease,
        transform 0.15s ease;

    display: flex !important;

    align-items: center !important;
}


/* Navigation item hover */

section[data-testid="stSidebar"]
div[data-testid="stRadio"] label:hover {

    background:
        rgba(99,102,241,0.16) !important;

    transform:
        translateX(2px);
}


/* Navigation text */

section[data-testid="stSidebar"]
div[data-testid="stRadio"] label p {

    color: #f1f5f9 !important;

    font-size: 15px !important;

    font-weight: 600 !important;

    line-height: 1.4 !important;

    margin: 0 !important;

    opacity: 1 !important;
}


/* Radio circle */

section[data-testid="stSidebar"]
div[data-testid="stRadio"] label div[role="radio"] {

    transform: scale(1.05);

}


/* ============================================================
   BOTTOM PRODUCT MESSAGE
   ============================================================ */

.cf-bottom-title {

    color: #ffffff;

    font-size: 16px;

    font-weight: 750;

    line-height: 1.35;

    margin-top: 3px;
}

.cf-bottom-description {

    color: #dbeafe;

    font-size: 13px;

    font-weight: 450;

    line-height: 1.6;

    margin-top: 7px;
}

.cf-bottom-label {

    color: #a5b4fc;

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 0.12em;

    margin-bottom: 5px;
}

.cf-bottom-flow {

    color: #818cf8;

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 0.08em;

    line-height: 1.5;

    margin-top: 12px;
}


/* ============================================================
   GENERAL BUTTONS
   ============================================================ */

.stButton > button {

    border-radius: 9px;

    font-weight: 650;

    min-height: 40px;

    transition:
        transform 0.12s ease,
        box-shadow 0.12s ease;
}


.stButton > button:hover {

    transform:
        translateY(-1px);

    box-shadow:
        0 5px 14px
        rgba(15,23,42,0.08);
}


.stButton > button[kind="primary"] {

    background:
        linear-gradient(
            135deg,
            #6366f1,
            #7c3aed
        );

    color: white;

    border: none;

    box-shadow:
        0 6px 16px
        rgba(99,102,241,0.24);
}


/* ============================================================
   METRICS
   ============================================================ */

div[data-testid="stMetric"] {

    background: #ffffff;

    border:
        1px solid #e2e8f0;

    border-radius: 13px;

    padding: 15px 17px;

    box-shadow:
        0 2px 8px
        rgba(15,23,42,0.035);
}


div[data-testid="stMetricLabel"] {

    color: #64748b;

    font-size: 12px;

    font-weight: 600;
}


div[data-testid="stMetricValue"] {

    color: #0f172a;

    font-weight: 800;
}


/* ============================================================
   CONTAINERS
   ============================================================ */

div[data-testid="stVerticalBlockBorderWrapper"] {

    border-radius: 14px;
}


/* ============================================================
   INPUTS
   ============================================================ */

div[data-baseweb="input"],
div[data-baseweb="textarea"] {

    border-radius: 9px;
}


/* ============================================================
   TABS
   ============================================================ */

button[data-baseweb="tab"] {

    font-weight: 650;
}


/* ============================================================
   ALERTS
   ============================================================ */

div[data-testid="stAlert"] {

    border-radius: 10px;
}


/* ============================================================
   PROGRESS BAR
   ============================================================ */

div[data-testid="stProgressBar"] {

    border-radius: 999px;
}


/* ============================================================
   MAIN DIVIDERS
   ============================================================ */

.main hr {

    border-color: #e2e8f0;
}


/* ============================================================
   RESPONSIVE
   ============================================================ */

@media (max-width: 1000px) {

    section[data-testid="stSidebar"] {

        min-width: 255px;
        max-width: 275px;
    }

    section[data-testid="stSidebar"] h1 {

        font-size: 22px !important;
    }

    section[data-testid="stSidebar"]
    div[data-testid="stRadio"] label p {

        font-size: 14px !important;
    }

}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

initialize_database()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # ========================================================
    # BRAND
    # ========================================================

    st.markdown(
        "# 🚀 CareerFlow AI"
    )

    st.caption(
        "Multi-Agent Career Operating System"
    )

    st.divider()

    # ========================================================
    # WORKSPACE
    # ========================================================

    st.caption(
        "WORKSPACE"
    )

    selected_page = st.radio(
        "Navigation",

        [
            "Command Center",
            "⚡ Career Mission",
            "My Resume",
            "Discover Jobs",
            "Job Matches",
            "Application Queue",
            "Applications",
            "Interview Prep",
            "Career Intelligence",
            "Resume Score",
            "Agent Activity",
            "Analytics",
            "Settings",
        ],

        label_visibility="collapsed",
    )

    st.divider()

    # ========================================================
    # CAREERFLOW AI VALUE PROPOSITION
    # ========================================================

    st.markdown(
        "### 🤖 Your AI Career Team"
    )

    st.markdown(
        """
        <div class="cf-bottom-description">
        Discover opportunities, match your skills,
        prepare applications, practice interviews,
        and continuously improve your career strategy.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="cf-bottom-flow">
        DISCOVER&nbsp;&nbsp;·&nbsp;&nbsp;
        MATCH&nbsp;&nbsp;·&nbsp;&nbsp;
        APPLY&nbsp;&nbsp;·&nbsp;&nbsp;
        IMPROVE
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# PAGE ROUTING
# ============================================================

if selected_page == "Command Center":

    show_dashboard()

elif selected_page == "⚡ Career Mission":

    show_mission()

elif selected_page == "My Resume":

    show_resume()

elif selected_page == "Discover Jobs":

    show_jobs()

elif selected_page == "Job Matches":

    show_matches()

elif selected_page == "Application Queue":
    show_application_queue()

elif selected_page == "Applications":
    show_applications()

elif selected_page == "Interview Prep":

    show_interview()

elif selected_page == "Career Intelligence":

    show_career()

elif selected_page == "Resume Score":

    show_scores()

elif selected_page == "Agent Activity":

    show_agent_activity()

elif selected_page == "Analytics":

    show_analytics()

elif selected_page == "Settings":

    show_settings()