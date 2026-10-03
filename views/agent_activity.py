import streamlit as st

from database.db import get_agent_activity


# ============================================================
# HELPERS
# ============================================================

def safe_text(value, default=""):
    if value is None:
        return default

    text = str(value).strip()

    return text if text else default


def normalize_status(status):
    value = safe_text(
        status,
        "INFO",
    ).upper()

    if value in {
        "SUCCESS",
        "COMPLETED",
        "COMPLETE",
        "DONE",
    }:
        return "SUCCESS"

    if value in {
        "FAILED",
        "FAILURE",
        "ERROR",
    }:
        return "FAILED"

    if value in {
        "RUNNING",
        "IN_PROGRESS",
        "PROCESSING",
    }:
        return "RUNNING"

    return "INFO"


def status_label(status):
    if status == "SUCCESS":
        return "● Completed"

    if status == "FAILED":
        return "● Failed"

    if status == "RUNNING":
        return "● Running"

    return "● Activity"


def agent_icon(agent):
    name = safe_text(
        agent,
        "Agent",
    ).lower()

    if "orchestrator" in name:
        return "⚡"

    if "resume" in name:
        return "🧠"

    if "discovery" in name or "search" in name:
        return "🔎"

    if "matching" in name or "match" in name:
        return "🎯"

    if "application" in name:
        return "📝"

    if "interview" in name:
        return "🎤"

    if "learning" in name:
        return "📚"

    return "🤖"


def status_message(status):
    if status == "SUCCESS":
        return "Completed successfully."

    if status == "FAILED":
        return "Reported an execution issue."

    if status == "RUNNING":
        return "Currently executing."

    return "Activity recorded."


# ============================================================
# AGENT ACTIVITY
# ============================================================

def show_agent_activity():

    # ========================================================
    # HEADER
    # ========================================================

    st.caption(
        "CAREERFLOW AI · AI WORKFORCE OPERATIONS"
    )

    st.title(
        "🤖 AI Workforce Activity"
    )

    st.write(
        "Observe how CareerFlow AI's specialized agents "
        "execute tasks, coordinate intelligence, and "
        "move your career mission forward."
    )

    # ========================================================
    # LOAD ACTIVITY
    # ========================================================

    try:

        activity = get_agent_activity()

    except Exception as exc:

        st.error(
            f"Unable to load agent activity: {exc}"
        )

        return

    if not isinstance(
        activity,
        list,
    ):

        activity = []

    # ========================================================
    # EMPTY STATE
    # ========================================================

    if not activity:

        st.divider()

        with st.container(
            border=True
        ):

            st.markdown(
                "### 🚀 Your AI workforce is waiting"
            )

            st.write(
                "Agent activity will appear here when "
                "you launch a Career Mission."
            )

            st.info(
                "Start a Career Mission to see the "
                "Orchestrator and six specialized agents "
                "work together."
            )

        return

    # ========================================================
    # NORMALIZE ACTIVITY
    # ========================================================

    normalized = []

    for item in activity:

        if not isinstance(
            item,
            dict,
        ):
            continue

        agent = safe_text(
            item.get("agent"),
            "Agent",
        )

        action = safe_text(
            item.get("action"),
            "Activity recorded",
        )

        status = normalize_status(
            item.get("status")
        )

        created_at = safe_text(
            item.get("created_at"),
            "Time unavailable",
        )

        details = safe_text(
            item.get("details")
        )

        normalized.append(
            {
                "agent": agent,
                "action": action,
                "status": status,
                "created_at": created_at,
                "details": details,
            }
        )

    # ========================================================
    # SUMMARY
    # ========================================================

    success_count = sum(
        1
        for item in normalized
        if item["status"] == "SUCCESS"
    )

    failed_count = sum(
        1
        for item in normalized
        if item["status"] == "FAILED"
    )

    running_count = sum(
        1
        for item in normalized
        if item["status"] == "RUNNING"
    )

    total_count = len(
        normalized
    )

    st.subheader(
        "Workforce Overview"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Total Activities",
            total_count,
        )

    with c2:

        st.metric(
            "Completed",
            success_count,
        )

    with c3:

        st.metric(
            "Running",
            running_count,
        )

    with c4:

        st.metric(
            "Issues",
            failed_count,
        )

    # ========================================================
    # WORKFORCE ARCHITECTURE
    # ========================================================

    st.divider()

    st.subheader(
        "🧩 Multi-Agent Workforce"
    )

    st.caption(
        "CareerFlow AI coordinates specialized agents "
        "through a central orchestration layer."
    )

    workforce = [
        (
            "⚡",
            "Career Orchestrator",
            "Coordinates the mission",
        ),
        (
            "🧠",
            "Resume Intelligence",
            "Understands the candidate profile",
        ),
        (
            "🔎",
            "Job Discovery",
            "Discovers relevant opportunities",
        ),
        (
            "🎯",
            "Matching",
            "Evaluates career fit",
        ),
        (
            "📝",
            "Application",
            "Builds application intelligence",
        ),
        (
            "🎤",
            "Interview",
            "Generates interview preparation",
        ),
        (
            "📚",
            "Learning",
            "Identifies skill development priorities",
        ),
    ]

    columns = st.columns(4)

    for index, (
        icon,
        name,
        description,
    ) in enumerate(workforce):

        with columns[index % 4]:

            with st.container(
                border=True
            ):

                st.markdown(
                    f"### {icon}"
                )

                st.markdown(
                    f"**{name}**"
                )

                st.caption(
                    description
                )

    # ========================================================
    # FILTERS
    # ========================================================

    st.divider()

    st.subheader(
        "🔍 Activity Stream"
    )

    filter_col, status_col = st.columns(
        [2, 1]
    )

    agent_options = sorted(
        {
            item["agent"]
            for item in normalized
        }
    )

    with filter_col:

        selected_agent = st.selectbox(
            "Agent",
            options=[
                "All Agents"
            ] + agent_options,
        )

    with status_col:

        selected_status = st.selectbox(
            "Status",
            options=[
                "All Statuses",
                "Completed",
                "Running",
                "Failed",
                "Activity",
            ],
        )

    # ========================================================
    # APPLY FILTERS
    # ========================================================

    filtered = normalized

    if selected_agent != "All Agents":

        filtered = [
            item
            for item in filtered
            if item["agent"] == selected_agent
        ]

    status_mapping = {
        "Completed": "SUCCESS",
        "Running": "RUNNING",
        "Failed": "FAILED",
        "Activity": "INFO",
    }

    if selected_status != "All Statuses":

        target_status = status_mapping[
            selected_status
        ]

        filtered = [
            item
            for item in filtered
            if item["status"] == target_status
        ]

    # ========================================================
    # ACTIVITY RESULTS
    # ========================================================

    st.caption(
        f"Showing {len(filtered)} of "
        f"{len(normalized)} activities"
    )

    if not filtered:

        st.info(
            "No activities match the selected filters."
        )

        return

    # Newest activity first.
    for item in reversed(
        filtered
    ):

        agent = item["agent"]
        action = item["action"]
        status = item["status"]
        created_at = item["created_at"]
        details = item["details"]

        icon = agent_icon(
            agent
        )

        with st.container(
            border=True
        ):

            left, middle, right = st.columns(
                [0.7, 4.5, 1.5]
            )

            with left:

                st.markdown(
                    f"## {icon}"
                )

            with middle:

                st.markdown(
                    f"**{agent}**"
                )

                st.write(
                    action
                )

                st.caption(
                    status_message(
                        status
                    )
                )

            with right:

                if status == "SUCCESS":

                    st.success(
                        status_label(status)
                    )

                elif status == "FAILED":

                    st.error(
                        status_label(status)
                    )

                elif status == "RUNNING":

                    st.warning(
                        status_label(status)
                    )

                else:

                    st.info(
                        status_label(status)
                    )

                st.caption(
                    created_at
                )

            if details:

                with st.expander(
                    "View execution details"
                ):

                    st.write(
                        details
                    )

    # ========================================================
    # ARCHITECTURE MESSAGE
    # ========================================================

    st.divider()

    with st.container(
        border=True
    ):

        st.markdown(
            "### ⚡ From activity to intelligence"
        )

        st.write(
            "CareerFlow AI turns individual agent actions "
            "into a coordinated career workflow — from "
            "understanding your profile to discovering "
            "opportunities, evaluating fit, preparing "
            "applications, coaching interviews, and "
            "closing skill gaps."
        )

        st.success(
            "Discover → Match → Apply → Interview → "
            "Learn → Improve"
        )