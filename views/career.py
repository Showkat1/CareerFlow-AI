import streamlit as st

from database.db import get_candidate_profile


def show_career():

    st.title("🧠 Career Intelligence")

    st.caption(
        "Understand your career position and next opportunities."
    )

    st.divider()

    saved = get_candidate_profile()

    if not saved:

        st.info(
            "Upload your resume to activate "
            "Career Intelligence."
        )

        return

    profile = saved["profile"]

    st.subheader(
        "🎯 Recommended Roles"
    )

    roles = profile.get(
        "target_roles",
        []
    )

    if roles:

        for role in roles:

            st.success(
                f"✓ {role}"
            )

    else:

        st.info(
            "No target roles identified yet."
        )

    st.subheader(
        "💪 Career Strengths"
    )

    for item in profile.get(
        "career_strengths",
        []
    ):

        st.write(
            f"• {item}"
        )

    st.subheader(
        "⚠ Skill Gaps"
    )

    for item in profile.get(
        "potential_skill_gaps",
        []
    ):

        st.warning(
            f"• {item}"
        )

    st.subheader(
        "🚀 Recommendations"
    )

    for item in profile.get(
        "career_recommendations",
        []
    ):

        st.info(
            f"💡 {item}"
        )