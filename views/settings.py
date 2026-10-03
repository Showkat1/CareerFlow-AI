
import streamlit as st

from database.db import (
    get_job_preferences,
    save_job_preferences,
)

from ui.components import section_header, status_message
from locations.location_selector import location_selector


def show_settings():
    st.title("⚙️ Settings")
    st.caption(
        "Personalize your job search and career preferences."
    )

    preferences = get_job_preferences()

    experience_levels = [
        "",
        "Entry Level",
        "Mid Level",
        "Senior",
        "Lead",
        "Manager",
    ]

    current_level = preferences.get("experience_level", "")
    level_index = (
        experience_levels.index(current_level)
        if current_level in experience_levels
        else 0
    )

    section_header(
        "Job Search Preferences",
        "Configure how CareerFlow AI discovers and evaluates opportunities.",
        icon="🎯",
    )

    # Location selector must remain outside the form.
    selected_locations = location_selector(
        initial_locations=preferences.get("locations", []),
        key="settings_locations",
    )

    with st.form("careerflow_settings_form"):
        st.markdown("#### 💼 Career Goals")

        col1, col2 = st.columns(2)

        with col1:
            target_roles = st.text_input(
                "Target roles",
                value=", ".join(
                    preferences.get("target_roles", [])
                ),
                placeholder="Cloud Engineer, Solutions Architect",
            )

            experience_level = st.selectbox(
                "Experience level",
                experience_levels,
                index=level_index,
            )

            industries = st.text_input(
                "Preferred industries",
                value=", ".join(
                    preferences.get("industries", [])
                ),
                placeholder="Technology, Finance, Healthcare",
            )

        with col2:
            work_modes = st.multiselect(
                "Work mode",
                ["Remote", "Hybrid", "On-site"],
                default=preferences.get("work_modes", []),
            )

            minimum_salary = st.text_input(
                "Minimum salary",
                value=preferences.get("minimum_salary", ""),
                placeholder="₹12 LPA",
            )

        st.divider()

        st.markdown("#### 🔎 Matching Preferences")

        col3, col4 = st.columns(2)

        with col3:
            keywords = st.text_input(
                "Required keywords",
                value=", ".join(
                    preferences.get("keywords", [])
                ),
                placeholder="GCP, Python, AI",
            )

        with col4:
            excluded_keywords = st.text_input(
                "Excluded keywords",
                value=", ".join(
                    preferences.get("excluded_keywords", [])
                ),
                placeholder="Intern, unpaid",
            )

        minimum_match_score = st.slider(
            "Minimum match score",
            min_value=50,
            max_value=100,
            value=int(
                preferences.get("minimum_match_score", 70)
            ),
            help="Set the minimum score for considering a job match.",
        )

        st.divider()

        submitted = st.form_submit_button(
            "💾 Save Preferences",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        new_preferences = {
            "target_roles": [
                item.strip()
                for item in target_roles.split(",")
                if item.strip()
            ],
            "locations": selected_locations,
            "work_modes": work_modes,
            "experience_level": experience_level,
            "minimum_salary": minimum_salary,
            "industries": [
                item.strip()
                for item in industries.split(",")
                if item.strip()
            ],
            "keywords": [
                item.strip()
                for item in keywords.split(",")
                if item.strip()
            ],
            "excluded_keywords": [
                item.strip()
                for item in excluded_keywords.split(",")
                if item.strip()
            ],
            "minimum_match_score": minimum_match_score,
        }

        save_job_preferences(new_preferences)

        status_message(
            "Your job search preferences have been saved.",
            status="success",
        )