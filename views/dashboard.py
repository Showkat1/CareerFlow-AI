import streamlit as st

from database.db import (
    get_candidate_profile,
    get_jobs,
    get_applications,
    get_agent_activity,
)


# ============================================================
# HELPERS
# ============================================================

def safe_number(value, default=0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def get_value(data, *keys, default=None):
    if not isinstance(data, dict):
        return default

    for key in keys:
        value = data.get(key)

        if value is not None and value != "":
            return value

    return default


def as_list(value):
    if value is None:
        return []

    if isinstance(value, str):
        value = value.strip()
        return [value] if value else []

    if isinstance(value, (list, tuple, set)):
        return [
            str(item).strip()
            for item in value
            if str(item).strip()
        ]

    return [str(value).strip()]


def get_match_score(job):
    if not isinstance(job, dict):
        return 0

    return safe_number(
        get_value(
            job,
            "match_score",
            "score",
            "match_percentage",
            default=0,
        )
    )


def get_agent_completed(context, agent_name):
    if not context:
        return False

    results = getattr(context, "agent_results", []) or []

    target = agent_name.lower()

    for item in results:
        if not isinstance(item, dict):
            continue

        recorded = str(
            item.get("agent", "")
        ).lower()

        if target in recorded:
            return True

    return False


def get_agent_status(context, agent_name):
    if not context:
        return "READY"

    results = getattr(context, "agent_results", []) or []

    target = agent_name.lower()

    for item in reversed(results):
        if not isinstance(item, dict):
            continue

        recorded = str(
            item.get("agent", "")
        ).lower()

        if target in recorded:
            if item.get("success"):
                return "COMPLETED"

            return "FAILED"

    return "READY"


def status_label(status):
    if status == "COMPLETED":
        return "● Completed"

    if status == "FAILED":
        return "● Attention"

    return "○ Ready"


# ============================================================
# COMMAND CENTER
# ============================================================

def show_dashboard():

    # ========================================================
    # LOAD DATA
    # ========================================================

    try:
        candidate = get_candidate_profile()
    except Exception:
        candidate = None

    try:
        jobs = get_jobs()
    except Exception:
        jobs = []

    try:
        applications = get_applications()
    except Exception:
        applications = []

    try:
        agent_activity = get_agent_activity()
    except Exception:
        agent_activity = []

    context = st.session_state.get(
        "career_mission_context"
    )

    # ========================================================
    # HEADER
    # ========================================================

    st.caption(
        "CAREERFLOW AI · COMMAND CENTER"
    )

    st.title(
        "🚀 Career Command Center"
    )

    st.write(
        "Your AI-powered career operating system for "
        "discovering opportunities, evaluating fit, "
        "building applications, preparing for interviews, "
        "and continuously improving."
    )

    # ========================================================
    # PROFILE STATE
    # ========================================================

    profile = {}

    if isinstance(candidate, dict):
        profile = candidate.get(
            "profile",
            {}
        ) or {}

    if not isinstance(profile, dict):
        profile = {}

    candidate_name = get_value(
        profile,
        "name",
        "candidate_name",
        "full_name",
        default="Career Professional",
    )

    headline = get_value(
        profile,
        "headline",
        "professional_title",
        "title",
        default="Build your next career opportunity",
    )

    # ========================================================
    # HERO / PROFILE STATUS
    # ========================================================

    with st.container(border=True):

        hero_left, hero_right = st.columns(
            [3.5, 1.2]
        )

        with hero_left:

            st.markdown(
                f"### Welcome back, {candidate_name} 👋"
            )

            st.write(
                headline
            )

            if context:
                st.success(
                    "⚡ Career Mission completed and "
                    "your AI workforce has generated "
                    "personalized intelligence."
                )
            elif profile:
                st.info(
                    "Your career profile is active. "
                    "Launch a Career Mission to activate "
                    "the full AI workforce."
                )
            else:
                st.warning(
                    "Upload your resume first to create "
                    "your Career Intelligence profile."
                )

        with hero_right:

            profile_score = safe_number(
                get_value(
                    profile,
                    "resume_score",
                    "score",
                    default=0,
                )
            )

            st.metric(
                "Resume Score",
                f"{profile_score:.0f}/100"
            )

    # ========================================================
    # CAREER READINESS
    # ========================================================

    readiness_values = []

    interview_readiness = 0
    learning_readiness = 0
    match_readiness = 0

    if context:

        interview_plan = getattr(
            context,
            "interview_plan",
            {}
        )

        if isinstance(interview_plan, dict):

            interview_readiness = safe_number(
                get_value(
                    interview_plan,
                    "readiness_score",
                    "score",
                    default=0,
                )
            )

        learning_plan = getattr(
            context,
            "learning_plan",
            {}
        )

        if isinstance(learning_plan, dict):

            learning_readiness = safe_number(
                get_value(
                    learning_plan,
                    "readiness_score",
                    "score",
                    default=0,
                )
            )

        matched_jobs = getattr(
            context,
            "matched_jobs",
            []
        ) or []

        match_scores = [
            get_match_score(job)
            for job in matched_jobs
            if get_match_score(job) > 0
        ]

        if match_scores:
            match_readiness = (
                sum(match_scores)
                / len(match_scores)
            )

        readiness_values = [
            value
            for value in [
                interview_readiness,
                learning_readiness,
                match_readiness,
            ]
            if value > 0
        ]

    readiness = (
        sum(readiness_values)
        / len(readiness_values)
        if readiness_values
        else 0
    )

    # ========================================================
    # KPI ROW
    # ========================================================

    st.subheader(
        "Career Snapshot"
    )

    matched_jobs = (
        getattr(
            context,
            "matched_jobs",
            []
        ) or []
        if context
        else []
    )

    application_list = (
        applications
        if isinstance(applications, list)
        else []
    )

    activity_list = (
        agent_activity
        if isinstance(agent_activity, list)
        else []
    )

    agent_results = (
        getattr(
            context,
            "agent_results",
            []
        ) or []
        if context
        else []
    )

    k1, k2, k3, k4 = st.columns(4)

    with k1:

        st.metric(
            "Career Readiness",
            f"{readiness:.0f}%"
        )

        if readiness > 0:
            st.progress(
                min(
                    max(
                        readiness / 100,
                        0,
                    ),
                    1,
                )
            )

    with k2:

        st.metric(
            "Top Matches",
            len(matched_jobs)
        )

    with k3:

        st.metric(
            "Applications",
            len(application_list)
        )

    with k4:

        st.metric(
            "Agents Completed",
            len(agent_results)
        )

    # ========================================================
    # ACTIVE CAREER MISSION
    # ========================================================

    st.divider()

    st.subheader(
        "⚡ Career Mission"
    )

    if context:

        goal = getattr(
            context,
            "user_goal",
            ""
        ) or "Career mission in progress."

        st.markdown(
            f"**Mission Goal**  \n{goal}"
        )

        total_agents = 6

        completed_agents = len(
            agent_results
        )

        progress = min(
            completed_agents / total_agents,
            1.0,
        )

        st.progress(
            progress,
            text=(
                f"Mission Progress · "
                f"{completed_agents}/{total_agents} "
                f"agents completed"
            ),
        )

        st.write("")

        mission_agents = [
            ("🧠", "Resume Intelligence Agent"),
            ("🔎", "Job Discovery Agent"),
            ("🎯", "Matching Agent"),
            ("📝", "Application Agent"),
            ("🎤", "Interview Agent"),
            ("📚", "Learning Agent"),
        ]

        columns = st.columns(6)

        for index, (
            icon,
            agent_name,
        ) in enumerate(mission_agents):

            with columns[index]:

                status = get_agent_status(
                    context,
                    agent_name,
                )

                if status == "COMPLETED":

                    st.success(
                        f"{icon} {agent_name.replace(' Agent', '')}"
                    )

                    st.caption(
                        "Completed"
                    )

                elif status == "FAILED":

                    st.warning(
                        f"{icon} {agent_name.replace(' Agent', '')}"
                    )

                    st.caption(
                        "Needs attention"
                    )

                else:

                    st.info(
                        f"{icon} {agent_name.replace(' Agent', '')}"
                    )

                    st.caption(
                        "Ready"

                    )

    else:

        with st.container(border=True):

            st.markdown(
                "### Start your first Career Mission"
            )

            st.write(
                "Give CareerFlow AI a career goal and "
                "your AI workforce will coordinate "
                "resume intelligence, job discovery, "
                "matching, applications, interview "
                "preparation, and learning."
            )

            if st.button(
                "⚡ Launch Career Mission",
                type="primary",
                use_container_width=True,
            ):

                st.session_state[
                    "dashboard_start_mission"
                ] = True

                st.info(
                    "Open **Career Mission** from the "
                    "sidebar to define your career goal."
                )

    # ========================================================
    # OPPORTUNITIES
    # ========================================================

    st.divider()

    left, right = st.columns(
        [1.5, 1]
    )

    with left:

        st.subheader(
            "🎯 Top Career Opportunities"
        )

        st.caption(
            "Opportunities with the strongest "
            "alignment to your career profile."
        )

        if not matched_jobs:

            st.info(
                "No personalized matches yet. "
                "Run a Career Mission to generate "
                "your opportunity intelligence."
            )

        else:

            sorted_jobs = sorted(
                matched_jobs,
                key=get_match_score,
                reverse=True,
            )

            for job in sorted_jobs[:4]:

                if not isinstance(job, dict):
                    continue

                title = get_value(
                    job,
                    "title",
                    "job_title",
                    default="Career Opportunity",
                )

                company = get_value(
                    job,
                    "company",
                    "company_name",
                    default="Company",
                )

                location = get_value(
                    job,
                    "location",
                    "job_location",
                    default="Location not specified",
                )

                score = get_match_score(
                    job
                )

                with st.container(border=True):

                    job_left, job_right = st.columns(
                        [4, 1]
                    )

                    with job_left:

                        st.markdown(
                            f"### {title}"
                        )

                        st.caption(
                            f"🏢 {company} · 📍 {location}"
                        )

                    with job_right:

                        st.metric(
                            "Match",
                            f"{score:.0f}%"
                        )

                    if score >= 80:

                        st.caption(
                            "Strong alignment with your "
                            "current career profile."
                        )

                    elif score >= 60:

                        st.caption(
                            "Good alignment with some "
                            "areas to strengthen."
                        )

                    else:

                        st.caption(
                            "Potential opportunity with "
                            "additional skill alignment needed."
                        )

    # ========================================================
    # AI WORKFORCE
    # ========================================================

    with right:

        st.subheader(
            "🤖 AI Workforce"
        )

        st.caption(
            "Six specialized agents working as one "
            "career intelligence system."
        )

        workforce = [
            (
                "🧠",
                "Resume Intelligence",
                "Understands your career profile",
            ),
            (
                "🔎",
                "Job Discovery",
                "Finds relevant opportunities",
            ),
            (
                "🎯",
                "Matching",
                "Evaluates job fit",
            ),
            (
                "📝",
                "Application",
                "Builds application strategy",
            ),
            (
                "🎤",
                "Interview",
                "Prepares you for interviews",
            ),
            (
                "📚",
                "Learning",
                "Closes priority skill gaps",
            ),
        ]

        for (
            icon,
            name,
            description,
        ) in workforce:

            completed = get_agent_completed(
                context,
                name,
            )

            with st.container(
                border=True
            ):

                if completed:

                    st.markdown(
                        f"**{icon} {name}** · ✓"
                    )

                else:

                    st.markdown(
                        f"**{icon} {name}**"
                    )

                st.caption(
                    description
                )

    # ========================================================
    # CAREER INTELLIGENCE
    # ========================================================

    st.divider()

    st.subheader(
        "📊 Career Intelligence"
    )

    ci1, ci2, ci3 = st.columns(3)

    # --------------------------------------------------------
    # STRENGTHS
    # --------------------------------------------------------

    with ci1:

        with st.container(
            border=True
        ):

            st.markdown(
                "### 💪 Strengths"
            )

            strengths = []

            if context:

                career_intelligence = getattr(
                    context,
                    "career_intelligence",
                    {}
                )

                if isinstance(
                    career_intelligence,
                    dict,
                ):

                    resume_data = career_intelligence.get(
                        "resume",
                        {}
                    )

                    if isinstance(
                        resume_data,
                        dict,
                    ):

                        strengths = as_list(
                            get_value(
                                resume_data,
                                "strengths",
                                "skills",
                                "key_skills",
                                default=[],
                            )
                        )

            if not strengths:

                strengths = as_list(
                    get_value(
                        profile,
                        "strengths",
                        "key_strengths",
                        "skills",
                        default=[],
                    )
                )

            if strengths:

                for skill in strengths[:6]:

                    st.write(
                        f"• {skill}"
                    )

            else:

                st.caption(
                    "Your Resume Intelligence Agent "
                    "will identify your strongest "
                    "career capabilities."
                )

    # --------------------------------------------------------
    # SKILL GAPS
    # --------------------------------------------------------

    with ci2:

        with st.container(
            border=True
        ):

            st.markdown(
                "### 🎯 Skill Gaps"
            )

            gaps = []

            if context:

                learning_plan = getattr(
                    context,
                    "learning_plan",
                    {}
                )

                if isinstance(
                    learning_plan,
                    dict,
                ):

                    gaps = as_list(
                        get_value(
                            learning_plan,
                            "skill_gaps",
                            "gaps",
                            default=[],
                        )
                    )

            if not gaps:

                gaps = as_list(
                    get_value(
                        profile,
                        "skill_gaps",
                        "gaps",
                        "missing_skills",
                        default=[],
                    )
                )

            if gaps:

                for gap in gaps[:6]:

                    st.write(
                        f"• {gap}"
                    )

            else:

                st.caption(
                    "Your Learning Agent will identify "
                    "the highest-priority skills to develop."
                )

    # --------------------------------------------------------
    # INTERVIEW
    # --------------------------------------------------------

    with ci3:

        with st.container(
            border=True
        ):

            st.markdown(
                "### 🎤 Interview Readiness"
            )

            st.metric(
                "Readiness",
                f"{interview_readiness:.0f}%"
            )

            if interview_readiness > 0:

                st.progress(
                    min(
                        max(
                            interview_readiness / 100,
                            0,
                        ),
                        1,
                    )
                )

                st.caption(
                    "Your Interview Agent has created "
                    "a personalized preparation plan."
                )

            else:

                st.caption(
                    "Run a Career Mission to generate "
                    "personalized interview preparation."
                )

    # ========================================================
    # CAREER LOOP
    # ========================================================

    st.divider()

    st.subheader(
        "🔄 Your Career Improvement Loop"
    )

    loop_columns = st.columns(6)

    loop_steps = [
        ("01", "Discover"),
        ("02", "Match"),
        ("03", "Apply"),
        ("04", "Interview"),
        ("05", "Learn"),
        ("06", "Improve"),
    ]

    for index, (
        number,
        label,
    ) in enumerate(loop_steps):

        with loop_columns[index]:

            with st.container(
                border=True
            ):

                st.caption(
                    number
                )

                st.markdown(
                    f"**{label}**"
                )

    st.caption(
        "CareerFlow AI continuously turns your career "
        "activity into the next improvement opportunity."
    )

    # ========================================================
    # RECENT AGENT ACTIVITY
    # ========================================================

    st.divider()

    st.subheader(
        "🕒 Recent Agent Activity"
    )

    if activity_list:

        recent = activity_list[-6:]

        for item in reversed(
            recent
        ):

            if not isinstance(
                item,
                dict,
            ):
                continue

            agent = get_value(
                item,
                "agent_name",
                "agent",
                default="Agent",
            )

            action = get_value(
                item,
                "action",
                "message",
                "activity",
                default="Activity recorded",
            )

            status = get_value(
                item,
                "status",
                default="INFO",
            )

            with st.container(
                border=True
            ):

                activity_left, activity_right = st.columns(
                    [4, 1]
                )

                with activity_left:

                    st.markdown(
                        f"**{agent}**"
                    )

                    st.caption(
                        str(action)
                    )

                with activity_right:

                    st.caption(
                        str(status)
                    )

    else:

        st.info(
            "Agent activity will appear here after "
            "your Career Mission runs."
        )

    # ========================================================
    # FINAL CTA
    # ========================================================

    st.divider()

    if context:

        st.success(
            "🚀 Your CareerFlow AI workforce is active. "
            "Review your matches, applications, interview "
            "preparation, and learning roadmap."
        )

    elif profile:

        st.info(
            "💡 Your career profile is ready. "
            "Launch a Career Mission to let six specialized "
            "AI agents work together toward your goal."
        )

    else:

        st.warning(
            "📄 Start by uploading your resume. "
            "CareerFlow AI will transform it into your "
            "Career Intelligence profile."
        )