import streamlit as st

from database.db import get_jobs


# ============================================================
# HELPERS
# ============================================================

def row_to_dict(row):
    """
    Convert sqlite rows / dictionaries / objects
    into a normal dictionary.
    """

    if row is None:
        return {}

    if isinstance(row, dict):
        return dict(row)

    try:
        return dict(row)
    except Exception:
        pass

    result = {}

    for key in [
        "id",
        "job_id",
        "title",
        "job_title",
        "company",
        "company_name",
        "location",
        "description",
        "skills",
        "required_skills",
        "source",
        "url",
        "job_url",
        "match_score",
        "score",
        "status",
    ]:

        if hasattr(row, key):
            result[key] = getattr(row, key)

    return result


def get_value(data, *keys, default=None):

    for key in keys:

        value = data.get(key)

        if value is not None and value != "":
            return value

    return default


def as_list(value):

    if value is None:
        return []

    if isinstance(value, str):

        # Handle comma-separated values.
        if "," in value:

            return [
                item.strip()
                for item in value.split(",")
                if item.strip()
            ]

        return [value]

    if isinstance(value, (list, tuple)):

        return [
            str(item)
            for item in value
        ]

    return [str(value)]


def safe_number(value, default=0):

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


# ============================================================
# DISCOVER JOBS
# ============================================================

def show_jobs():

    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.caption(
        "CAREERFLOW AI · OPPORTUNITY DISCOVERY"
    )

    st.title(
        "🔎 Discover Jobs"
    )

    st.write(
        "Explore opportunities available to your CareerFlow AI "
        "workforce. Search, filter, review, and identify roles "
        "that align with your career direction."
    )

    st.divider()

    # ========================================================
    # LOAD JOBS
    # ========================================================

    try:

        raw_jobs = get_jobs()

        if raw_jobs is None:
            raw_jobs = []

        jobs = [
            row_to_dict(job)
            for job in raw_jobs
        ]

    except Exception as exc:

        st.error(
            f"Unable to load jobs: {exc}"
        )

        return

    # ========================================================
    # SEARCH / FILTER
    # ========================================================

    st.subheader(
        "Find Your Next Opportunity"
    )

    search_col, location_col, source_col = st.columns(
        [2.2, 1.3, 1.1]
    )

    with search_col:

        search = st.text_input(
            "Search",
            placeholder=(
                "Search role, company, skill..."
            ),
        )

    with location_col:

        locations = sorted(
            {
                str(
                    get_value(
                        job,
                        "location",
                        default="",
                    )
                )
                for job in jobs
                if get_value(
                    job,
                    "location",
                    default="",
                )
            }
        )

        selected_location = st.selectbox(
            "Location",
            ["All locations"] + locations,
        )

    with source_col:

        sources = sorted(
            {
                str(
                    get_value(
                        job,
                        "source",
                        default="",
                    )
                )
                for job in jobs
                if get_value(
                    job,
                    "source",
                    default="",
                )
            }
        )

        selected_source = st.selectbox(
            "Source",
            ["All sources"] + sources,
        )

    # ========================================================
    # FILTER
    # ========================================================

    filtered_jobs = []

    search_text = search.strip().lower()

    for job in jobs:

        title = str(
            get_value(
                job,
                "title",
                "job_title",
                default="",
            )
        )

        company = str(
            get_value(
                job,
                "company",
                "company_name",
                default="",
            )
        )

        location = str(
            get_value(
                job,
                "location",
                default="",
            )
        )

        description = str(
            get_value(
                job,
                "description",
                default="",
            )
        )

        skills = " ".join(
            as_list(
                get_value(
                    job,
                    "skills",
                    "required_skills",
                    default=[],
                )
            )
        )

        searchable = " ".join(
            [
                title,
                company,
                location,
                description,
                skills,
            ]
        ).lower()

        if search_text and search_text not in searchable:
            continue

        if (
            selected_location != "All locations"
            and location != selected_location
        ):
            continue

        source = str(
            get_value(
                job,
                "source",
                default="",
            )
        )

        if (
            selected_source != "All sources"
            and source != selected_source
        ):
            continue

        filtered_jobs.append(job)

    # ========================================================
    # SUMMARY
    # ========================================================

    st.divider()

    summary_col1, summary_col2, summary_col3 = st.columns(3)

    with summary_col1:

        st.metric(
            "Available Opportunities",
            len(jobs),
        )

    with summary_col2:

        st.metric(
            "Showing",
            len(filtered_jobs),
        )

    with summary_col3:

        mission_context = st.session_state.get(
            "career_mission_context"
        )

        if mission_context:

            st.metric(
                "Mission Matches",
                len(
                    mission_context.matched_jobs
                    or []
                ),
            )

        else:

            st.metric(
                "Mission Matches",
                0,
            )

    # ========================================================
    # EMPTY STATE
    # ========================================================

    if not filtered_jobs:

        st.info(
            "No opportunities match your current filters."
        )

        return

    # ========================================================
    # JOB RESULTS
    # ========================================================

    st.subheader(
        "Available Opportunities"
    )

    st.caption(
        "Review a role before sending it into your matching workflow."
    )

    for index, job in enumerate(
        filtered_jobs
    ):

        title = get_value(
            job,
            "title",
            "job_title",
            default="Untitled Opportunity",
        )

        company = get_value(
            job,
            "company",
            "company_name",
            default="Company not specified",
        )

        location = get_value(
            job,
            "location",
            default="Location not specified",
        )

        source = get_value(
            job,
            "source",
            default="CareerFlow",
        )

        description = get_value(
            job,
            "description",
            default="No job description available.",
        )

        skills = as_list(
            get_value(
                job,
                "skills",
                "required_skills",
                default=[],
            )
        )

        url = get_value(
            job,
            "url",
            "job_url",
            default="",
        )

        score = safe_number(
            get_value(
                job,
                "match_score",
                "score",
                default=0,
            )
        )

        # ----------------------------------------------------
        # CARD
        # ----------------------------------------------------

        with st.container(
            border=True
        ):

            top_left, top_right = st.columns(
                [5, 1]
            )

            with top_left:

                st.markdown(
                    f"### {title}"
                )

                st.markdown(
                    f"**🏢 {company}**"
                )

                st.caption(
                    f"📍 {location}  ·  🔗 {source}"
                )

            with top_right:

                if score > 0:

                    st.metric(
                        "Match",
                        f"{score:.0f}%",
                    )

            st.write(
                description[:700]
                + (
                    "..."
                    if len(description) > 700
                    else ""
                )
            )

            if skills:

                st.markdown(
                    "**Key Skills**"
                )

                skill_columns = st.columns(
                    min(len(skills[:6]), 3)
                    or 1
                )

                for column, skill in zip(
                    skill_columns,
                    skills[:6],
                ):

                    with column:

                        st.caption(
                            f"• {skill}"
                        )

            # ------------------------------------------------
            # ACTIONS
            # ------------------------------------------------

            action1, action2 = st.columns(
                [1, 1]
            )

            with action1:

                if url:

                    st.link_button(
                        "View Opportunity ↗",
                        url,
                        use_container_width=True,
                    )

                else:

                    st.button(
                        "Opportunity Details",
                        disabled=True,
                        use_container_width=True,
                        key=f"details_{index}",
                    )

            with action2:

                if st.button(
                    "🎯 Evaluate Match",
                    use_container_width=True,
                    key=f"match_{index}",
                ):

                    st.session_state[
                        "selected_job"
                    ] = job

                    st.success(
                        "Opportunity selected. "
                        "Open **Job Matches** to review your fit."
                    )

        if index < len(filtered_jobs) - 1:

            st.write("")


# ============================================================
# END
# ============================================================