
import streamlit as st


# CareerFlow AI design tokens
COLORS = {
    "primary": "#6366F1",
    "primary_dark": "#4F46E5",
    "accent": "#8B5CF6",
    "background": "#F8FAFC",
    "surface": "#FFFFFF",
    "text": "#0F172A",
    "muted": "#64748B",
    "border": "#E2E8F0",
    "sidebar": "#0B1424",
    "sidebar_text": "#F1F5F9",
    "success": "#16A34A",
    "warning": "#D97706",
    "danger": "#DC2626",
}

TYPOGRAPHY = {
    "font_family": "Inter, sans-serif",
    "heading_weight": 750,
    "body_weight": 400,
}

SPACING = {
    "page_top": "2rem",
    "page_bottom": "3rem",
    "card_padding": "1.25rem",
    "card_radius": "14px",
}


def apply_theme():
    """Apply the shared CareerFlow AI visual theme."""

    st.markdown(
        f"""
        <style>
        :root {{
            --cf-primary: {COLORS["primary"]};
            --cf-primary-dark: {COLORS["primary_dark"]};
            --cf-accent: {COLORS["accent"]};
            --cf-background: {COLORS["background"]};
            --cf-surface: {COLORS["surface"]};
            --cf-text: {COLORS["text"]};
            --cf-muted: {COLORS["muted"]};
            --cf-border: {COLORS["border"]};
        }}

        .stApp {{
            background: var(--cf-background);
            font-family: {TYPOGRAPHY["font_family"]};
        }}

        .main .block-container {{
            max-width: 1500px;
            padding-top: {SPACING["page_top"]};
            padding-bottom: {SPACING["page_bottom"]};
        }}

        h1, h2, h3, h4 {{
            color: var(--cf-text);
            letter-spacing: -0.02em;
        }}

        p {{
            color: #475569;
        }}

        section[data-testid="stSidebar"] {{
            background: linear-gradient(
                180deg,
                #07101F 0%,
                {COLORS["sidebar"]} 55%,
                #101A2C 100%
            );
            border-right: 1px solid #243149;
        }}

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4 {{
            color: #FFFFFF !important;
        }}

        section[data-testid="stSidebar"] p {{
            color: #DBEAFE !important;
        }}

        .stButton > button {{
            border-radius: 9px;
            font-weight: 650;
            min-height: 40px;
            transition: transform 0.12s ease,
                        box-shadow 0.12s ease;
        }}

        .stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 5px 14px rgba(15, 23, 42, 0.08);
        }}

        .stButton > button[kind="primary"] {{
            background: linear-gradient(
                135deg,
                var(--cf-primary),
                var(--cf-accent)
            );
            color: white;
            border: none;
            box-shadow: 0 6px 16px rgba(99, 102, 241, 0.24);
        }}

        div[data-testid="stMetric"] {{
            background: var(--cf-surface);
            border: 1px solid var(--cf-border);
            border-radius: {SPACING["card_radius"]};
            padding: 15px 17px;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.035);
        }}

        div[data-testid="stMetricLabel"] {{
            color: var(--cf-muted);
            font-size: 12px;
            font-weight: 600;
        }}

        div[data-testid="stMetricValue"] {{
            color: var(--cf-text);
            font-weight: 800;
        }}

        div[data-baseweb="input"],
        div[data-baseweb="textarea"] {{
            border-radius: 9px;
        }}

        div[data-testid="stAlert"] {{
            border-radius: 10px;
        }}

        .main hr {{
            border-color: var(--cf-border);
        }}

        @media (max-width: 1000px) {{
            .main .block-container {{
                padding-top: 1rem;
                padding-bottom: 2rem;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )