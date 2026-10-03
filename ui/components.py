
import streamlit as st


def section_header(title, description=None, icon=None):
    """Display a consistent section heading."""

    heading = f"{icon} {title}" if icon else title
    st.subheader(heading)

    if description:
        st.caption(description)


def info_card(title, description, icon="ℹ️"):
    """Display a simple informational card."""

    st.markdown(
        f"""
        <div style="
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 18px;
            margin: 8px 0;
        ">
            <div style="
                font-size: 16px;
                font-weight: 700;
                color: #0f172a;
                margin-bottom: 8px;
            ">
                {icon} {title}
            </div>
            <div style="
                color: #64748b;
                font-size: 14px;
                line-height: 1.6;
            ">
                {description}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_message(message, status="info"):
    """Show a consistent status message."""

    handlers = {
        "info": st.info,
        "success": st.success,
        "warning": st.warning,
        "error": st.error,
    }

    handlers.get(status, st.info)(message)