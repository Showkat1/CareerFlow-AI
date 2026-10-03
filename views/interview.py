import streamlit as st


def show_interview():

    st.title("🎤 Interview Prep")

    st.caption(
        "AI-powered preparation for your target roles."
    )

    st.divider()

    st.info(
        "Interview preparation will become active "
        "once applications reach the interview stage."
    )

    st.subheader(
        "Planned capabilities"
    )

    items = [
        "Technical interview questions",
        "Behavioral questions",
        "STAR answer coaching",
        "Company-specific preparation",
        "Role-specific questions",
        "Mock interview",
        "Answer evaluation"
    ]

    for item in items:

        st.write(
            f"✓ {item}"
        )