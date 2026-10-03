import streamlit as st

from core.mission import CareerMission


AGENT_STEPS = [
    ("🧠", "Resume Intelligence", "Profile analysis"),
    ("🔎", "Job Discovery", "Opportunity discovery"),
    ("🎯", "Matching", "Career fit evaluation"),
    ("📝", "Application", "Application strategy"),
    ("🎤", "Interview", "Interview preparation"),
    ("📚", "Learning", "Skill improvement"),
]


# ============================================================
# HELPERS
# ============================================================

def safe_number(value, default=0.0):
    """Safely convert a value to a number."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def get_value(data, *keys, default=None):
    """Return the first available non-empty dictionary value."""
    if not isinstance(data, dict):
        return default

    for key in keys:
        value = data.get(key)
        if value is not None and value != "":
            return value

    return default


def as_items(value):
    """Normalize a value into a list."""
    if value is None:
        return []

    if isinstance(value, (list, tuple)):
        return list(value)

    return [value]


def display_text(value, default=""):
    """Safely format values for display."""
    if value is None or isinstance(value, (dict, list, tuple)):
        return default

    return str(value)


def normalize_agent_name(value):
    """Normalize agent names for progress matching."""
    return " ".join(
        str(value or "")
        .lower()
        .replace(" agent", "")
        .split()
    )


def agent_completion(context):
    """
    Derive agent completion from successful recorded results.
    Cards and progress bar use this same state.
    """
    results = getattr(context, "agent_results", []) or []
    recorded = set()

    for item in results:
        if not isinstance(item, dict):
            continue

        if not item.get("success", True):
            continue

        name = normalize_agent_name(item.get("agent"))

        if name:
            recorded.add(name)

    states = {}

    for _, name, _ in AGENT_STEPS:
        normalized = normalize_agent_name(name)

        states[name] = any(
            normalized == value
            or normalized in value
            or value in normalized
            for value in recorded
        )

    return states


def unwrap_match(item):
    """
    Convert the Matching Agent's nested result into
    a display-friendly structure.
    """
    if not isinstance(item, dict):
        return {}

    job = (
        item.get("job")
        if isinstance(item.get("job"), dict)
        else {}
    )

    analysis = (
        item.get("result")
        if isinstance(item.get("result"), dict)
        else {}
    )

    return {
        "title": get_value(
            job,
            "title",
            "job_title",
            "role",
            default=get_value(
                item,
                "title",
                "job_title",
                default="Career Opportunity",
            ),
        ),

        "company": get_value(
            job,
            "company",
            "company_name",
            "employer",
            default=get_value(
                item,
                "company",
                "company_name",
                default="Company not specified",
            ),
        ),

        "location": get_value(
            job,
            "location",
            "city",
            default="",
        ),

        "score": safe_number(
            get_value(
                item,
                "score",
                "match_score",
                "match_percentage",
                default=get_value(
                    analysis,
                    "match_score",
                    "score",
                    default=0,
                ),
            )
        ),

        "reason": get_value(
            analysis,
            "reason",
            "match_reason",
            "why_match",
            default=get_value(
                item,
                "reason",
                "match_reason",
                default="",
            ),
        ),

        "matching_skills": as_items(
            get_value(
                analysis,
                "matching_skills",
                "matched_skills",
                default=get_value(
                    item,
                    "matching_skills",
                    "matched_skills",
                    default=[],
                ),
            )
        ),

        "missing_skills": as_items(
            get_value(
                analysis,
                "missing_skills",
                "skill_gaps",
                default=get_value(
                    item,
                    "missing_skills",
                    "skill_gaps",
                    default=[],
                ),
            )
        ),

        "url": get_value(
            job,
            "url",
            "job_url",
            "link",
            default=get_value(
                item,
                "url",
                "job_url",
                default="",
            ),
        ),
    }


def render_questions(items):
    """Render plain-text or structured interview questions."""
    for index, item in enumerate(items, 1):

        if isinstance(item, dict):

            question = display_text(
                item.get("question"),
                "Question",
            )

            st.markdown(
                f"**{index}. {question}**"
            )

            if item.get("why_asked"):
                st.caption(
                    f"Why it may be asked: {item['why_asked']}"
                )

            if item.get("answer_guidance"):
                st.write(
                    f"**Answer guidance:** {item['answer_guidance']}"
                )

        else:
            st.markdown(
                f"{index}. {display_text(item)}"
            )


def render_learning_item(item, index):
    """Render structured skill-gap and roadmap records."""
    if not isinstance(item, dict):
        st.write(
            f"{index}. {display_text(item)}"
        )
        return

    title = get_value(
        item,
        "title",
        "skill",
        "phase",
        default="Learning item",
    )

    st.markdown(
        f"**{index}. {title}**"
    )

    fields = [
        ("importance", "Importance"),
        ("reason", "Why it matters"),
        ("current_level", "Current level"),
        ("target_level", "Target level"),
        ("duration", "Duration"),
    ]

    for key, label in fields:
        if item.get(key):
            st.markdown(
                f"- **{label}:** {item[key]}"
            )

    list_fields = [
        ("objectives", "Objectives"),
        ("practice_tasks", "Practice tasks"),
    ]

    for key, label in list_fields:
        values = as_items(
            item.get(key)
        )

        if values:
            st.markdown(
                f"**{label}**"
            )

            for value in values:
                st.markdown(
                    f"- {display_text(value)}"
                )


# ============================================================
# CAREER MISSION
# ============================================================

def show_mission():

    # ========================================================
    # HEADER
    # ========================================================

    st.caption(
        "CAREERFLOW AI · MISSION CONTROL"
    )

    st.title(
        "⚡ Career Mission"
    )

    st.write(
        "Turn a career goal into an AI-powered execution plan. "
        "Your specialized agents analyze your profile, discover "
        "opportunities, evaluate fit, prepare applications, "
        "coach interviews, and identify skills to build."
    )

    st.divider()

    # ========================================================
    # MISSION INPUT
    # ========================================================

    with st.container(border=True):

        st.subheader(
            "🎯 Define Your Career Mission"
        )

        st.caption(
            "Tell your AI workforce what you want to achieve."
        )

        goal = st.text_area(
            "Career goal",
            value=st.session_state.get(
                "career_mission_goal",
                "",
            ),
            placeholder=(
                "Example: I want to become a GCP Cloud Architect "
                "and find suitable opportunities."
            ),
            height=120,
            key="career_mission_goal_input",
        )

        launch = st.button(
            "⚡ Launch Career Mission",
            type="primary",
            use_container_width=True,
        )

    # ========================================================
    # EXECUTE MISSION
    # ========================================================

    if launch:

        cleaned_goal = (goal or "").strip()

        if not cleaned_goal:

            st.warning(
                "Please enter a career goal before launching your mission."
            )

            return

        st.session_state[
            "career_mission_goal"
        ] = cleaned_goal

        with st.status(
            "⚡ CareerFlow AI is coordinating your AI workforce...",
            expanded=True,
        ) as status:

            for icon, name, _ in AGENT_STEPS:
                st.write(
                    f"{icon} {name} Agent"
                )

            try:

                context = CareerMission().start(
                    cleaned_goal
                )

                st.session_state[
                    "career_mission_context"
                ] = context

                if getattr(context, "errors", []):

                    status.update(
                        label="Mission completed with issues",
                        state="error",
                        expanded=False,
                    )

                else:

                    status.update(
                        label="Career Mission completed",
                        state="complete",
                        expanded=False,
                    )

            except Exception as exc:

                status.update(
                    label="Career Mission failed",
                    state="error",
                    expanded=True,
                )

                st.exception(exc)

                return

    # ========================================================
    # LOAD MISSION
    # ========================================================

    context = st.session_state.get(
        "career_mission_context"
    )

    if context is None:

        st.info(
            "Enter a career goal above and launch your first Career Mission."
        )

        return

    # ========================================================
    # MISSION OVERVIEW
    # ========================================================

    st.divider()

    st.subheader(
        "Mission Overview"
    )

    st.caption(
        "Results from the most recently launched mission."
    )

    try:
        summary = context.summary() or {}
    except Exception:
        summary = {}

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Jobs Discovered",
        summary.get(
            "discovered_jobs",
            len(
                getattr(context, "discovered_jobs", []) or []
            ),
        ),
    )

    c2.metric(
        "Jobs Matched",
        summary.get(
            "matched_jobs",
            len(
                getattr(context, "matched_jobs", []) or []
            ),
        ),
    )

    c3.metric(
        "Applications",
        summary.get(
            "applications",
            len(
                getattr(context, "application_packages", []) or []
            ),
        ),
    )

    c4.metric(
        "Agents Executed",
        summary.get(
            "agents_executed",
            len(
                getattr(context, "agent_results", []) or []
            ),
        ),
    )

    if summary.get("mission_id"):

        st.caption(
            f"Mission ID: {summary['mission_id']}"
        )

    # ========================================================
    # MISSION GOAL
    # ========================================================

    st.subheader(
        "🎯 Mission Goal"
    )

    st.info(
        getattr(context, "user_goal", "")
        or "Career goal unavailable."
    )

    # ========================================================
    # AI WORKFORCE
    # ========================================================

    st.divider()

    st.subheader(
        "🤖 AI Workforce"
    )

    st.caption(
        "Six specialized agents collaborating across your career journey."
    )

    states = agent_completion(context)

    cols = st.columns(3)

    for index, (
        icon,
        name,
        description,
    ) in enumerate(AGENT_STEPS):

        with cols[index % 3]:

            with st.container(border=True):

                st.markdown(
                    f"### {icon}"
                )

                st.markdown(
                    f"**{name} Agent**"
                )

                if states[name]:

                    st.success(
                        f"● Completed · {description}"
                    )

                else:

                    st.caption(
                        f"○ Pending · {description}"
                    )

    completed = sum(
        bool(states[name])
        for _, name, _ in AGENT_STEPS
    )

    st.progress(
        completed / len(AGENT_STEPS),
        text=(
            f"AI Workforce Progress · "
            f"{completed}/{len(AGENT_STEPS)} agents completed"
        ),
    )

    # ========================================================
    # TOP CAREER OPPORTUNITIES
    # ========================================================

    st.divider()

    st.subheader(
        "🚀 Top Career Opportunities"
    )

    st.caption(
        "Opportunities identified and evaluated by your AI workforce."
    )

    matches = getattr(
        context,
        "matched_jobs",
        [],
    ) or []

    if not matches:

        st.info(
            "No matched opportunities were returned."
        )

    else:

        count = 0

        for item in matches:

            if count >= 5:
                break

            opportunity = unwrap_match(item)

            if not opportunity:
                continue

            count += 1

            score = max(
                0,
                min(
                    100,
                    opportunity["score"],
                ),
            )

            if score >= 80:
                label = "Strong Match"
            elif score >= 65:
                label = "Good Match"
            else:
                label = "Potential Match"

            with st.container(border=True):

                left, middle, right = st.columns(
                    [5, 3, 1.2]
                )

                with left:

                    st.markdown(
                        f"### {opportunity['title']}"
                    )

                    company = opportunity["company"]

                    if opportunity["location"]:
                        company += (
                            f" · {opportunity['location']}"
                        )

                    st.caption(
                        f"🏢 {company}"
                    )

                    if opportunity["reason"]:

                        st.write(
                            display_text(
                                opportunity["reason"]
                            )
                        )

                with middle:

                    if opportunity["matching_skills"]:

                        st.markdown(
                            "**Matching skills**"
                        )

                        st.write(
                            ", ".join(
                                display_text(value)
                                for value in opportunity["matching_skills"]
                            )
                        )

                    if opportunity["missing_skills"]:

                        st.markdown(
                            "**Skill gaps**"
                        )

                        st.caption(
                            ", ".join(
                                display_text(value)
                                for value in opportunity["missing_skills"]
                            )
                        )

                with right:

                    st.metric(
                        "Match",
                        f"{score:.0f}%",
                    )

                    st.caption(
                        label
                    )

                url = opportunity["url"]

                if (
                    isinstance(url, str)
                    and url.startswith(("https://", "http://"))
                ):

                    st.link_button(
                        "View Opportunity ↗",
                        url,
                    )

    # ========================================================
    # APPLICATION INTELLIGENCE
    # ========================================================

    packages = getattr(
        context,
        "application_packages",
        [],
    ) or []

    if packages:

        st.divider()

        st.subheader(
            "📝 Application Intelligence"
        )

        st.caption(
            "Personalized application strategies generated by the Application Agent."
        )

        for package in packages[:3]:

            if not isinstance(package, dict):
                continue

            job_info = (
                package.get("job")
                if isinstance(package.get("job"), dict)
                else {}
            )

            content = (
                package.get("package")
                if isinstance(package.get("package"), dict)
                else package
            )

            title = get_value(
                job_info,
                "title",
                "job_title",
                default=get_value(
                    package,
                    "job_title",
                    "title",
                    default="Application Strategy",
                ),
            )

            with st.expander(
                f"📝 {title}"
            ):

                fields = [
                    (
                        "Application Strategy",
                        ("application_strategy", "strategy"),
                    ),
                    (
                        "Suggested Headline",
                        ("resume_headline", "headline"),
                    ),
                    (
                        "Professional Positioning",
                        ("professional_summary", "summary"),
                    ),
                    (
                        "Cover Letter",
                        ("cover_letter",),
                    ),
                ]

                for label, keys in fields:

                    value = get_value(
                        content,
                        *keys,
                    )

                    if value:

                        st.markdown(
                            f"**{label}**"
                        )

                        st.write(
                            display_text(value)
                        )

                list_fields = [
                    (
                        "Key Talking Points",
                        "key_talking_points",
                    ),
                    (
                        "Skills to Emphasize",
                        "skills_to_emphasize",
                    ),
                    (
                        "Potential Gaps",
                        "potential_gaps",
                    ),
                ]

                for label, key in list_fields:

                    values = as_items(
                        content.get(key)
                    )

                    if values:

                        st.markdown(
                            f"**{label}**"
                        )

                        for value in values:

                            st.markdown(
                                f"- {display_text(value)}"
                            )

    # ========================================================
    # INTERVIEW INTELLIGENCE
    # ========================================================

    interview_data = getattr(
        context,
        "interview_plan",
        {},
    ) or {}

    if interview_data:

        st.divider()

        st.subheader(
            "🎤 Interview Intelligence"
        )

        st.caption(
            "Personalized preparation generated for your strongest opportunity."
        )

        if isinstance(interview_data, dict):

            plan = interview_data.get("plan")

            if not isinstance(plan, dict):
                plan = interview_data

            readiness = safe_number(
                get_value(
                    plan,
                    "readiness_score",
                    "interview_readiness",
                    "score",
                    default=0,
                )
            )

            readiness = max(
                0,
                min(100, readiness),
            )

            col1, col2 = st.columns(
                [1, 3]
            )

            col1.metric(
                "Interview Readiness",
                f"{readiness:.0f}%",
            )

            col2.info(
                display_text(
                    get_value(
                        plan,
                        "readiness_summary",
                        default=(
                            "Personalized interview preparation generated."
                        ),
                    )
                )
            )

            focus = as_items(
                plan.get("interview_focus")
            )

            if focus:

                st.markdown(
                    "**Preparation Focus**"
                )

                for value in focus:

                    st.markdown(
                        f"- {display_text(value)}"
                    )

            question_groups = [
                (
                    "💻 Technical Questions",
                    "technical_questions",
                ),
                (
                    "🧩 Behavioral Questions",
                    "behavioral_questions",
                ),
                (
                    "🎯 Candidate-Specific Questions",
                    "candidate_specific_questions",
                ),
            ]

            for label, key in question_groups:

                questions = as_items(
                    plan.get(key)
                )

                if questions:

                    with st.expander(label):

                        render_questions(
                            questions
                        )

            stories = as_items(
                plan.get("star_stories")
            )

            if stories:

                with st.expander(
                    "⭐ STAR Story Frameworks"
                ):

                    for index, story in enumerate(
                        stories,
                        1,
                    ):

                        if isinstance(story, dict):

                            st.markdown(
                                f"**{index}. {story.get('topic', 'Story')}**"
                            )

                            for key in (
                                "situation",
                                "task",
                                "action",
                                "result",
                            ):

                                if story.get(key):

                                    st.markdown(
                                        f"- **{key.title()}:** {story[key]}"
                                    )

                        else:

                            st.write(
                                display_text(story)
                            )

            gaps = as_items(
                plan.get("preparation_gaps")
            )

            if gaps:

                st.markdown(
                    "**Preparation Gaps**"
                )

                for gap in gaps:

                    st.markdown(
                        f"- {display_text(gap)}"
                    )

    # ========================================================
    # LEARNING INTELLIGENCE
    # ========================================================

    learning_data = getattr(
        context,
        "learning_plan",
        {},
    ) or []

    if learning_data:

        st.divider()

        st.subheader(
            "📚 Learning Intelligence"
        )

        st.caption(
            "Skills and actions identified by the Learning Agent."
        )

        if isinstance(learning_data, dict):

            plan = learning_data.get("plan")

            if not isinstance(plan, dict):
                plan = learning_data

            readiness = safe_number(
                get_value(
                    plan,
                    "overall_readiness",
                    "readiness_score",
                    "score",
                    default=0,
                )
            )

            readiness = max(
                0,
                min(100, readiness),
            )

            priority = display_text(
                get_value(
                    plan,
                    "priority_level",
                    "priority",
                    default="Not specified",
                )
            )

            col1, col2 = st.columns(2)

            col1.metric(
                "Career Readiness",
                f"{readiness:.0f}%",
            )

            col2.metric(
                "Learning Priority",
                priority,
            )

            learning_summary = get_value(
                plan,
                "learning_summary",
                "summary",
                default="",
            )

            if learning_summary:

                st.info(
                    display_text(learning_summary)
                )

            skill_gaps = as_items(
                get_value(
                    plan,
                    "skill_gaps",
                    "gaps",
                    default=[],
                )
            )

            if skill_gaps:

                with st.expander(
                    "🎯 Priority Skill Gaps",
                    expanded=True,
                ):

                    for index, item in enumerate(
                        skill_gaps,
                        1,
                    ):

                        render_learning_item(
                            item,
                            index,
                        )

            roadmap = as_items(
                get_value(
                    plan,
                    "learning_roadmap",
                    "roadmap",
                    default=[],
                )
            )

            if roadmap:

                with st.expander(
                    "🗺️ Learning Roadmap",
                    expanded=True,
                ):

                    for index, item in enumerate(
                        roadmap,
                        1,
                    ):

                        render_learning_item(
                            item,
                            index,
                        )

            sections = [
                (
                    "🛠️ Recommended Projects",
                    "project_ideas",
                ),
                (
                    "🎤 Interview Practice",
                    "interview_practice",
                ),
                (
                    "⚡ Next Actions",
                    "recommended_next_actions",
                ),
            ]

            for label, key in sections:

                values = as_items(
                    plan.get(key)
                )

                if values:

                    with st.expander(
                        label,
                        expanded=(
                            key == "recommended_next_actions"
                        ),
                    ):

                        for value in values:

                            st.markdown(
                                f"- {display_text(value)}"
                            )

    # ========================================================
    # ERRORS
    # ========================================================

    errors = getattr(
        context,
        "errors",
        [],
    ) or []

    if errors:

        st.divider()

        st.warning(
            "Some mission components reported issues."
        )

        for error in errors:

            if isinstance(error, dict):

                agent = error.get(
                    "agent",
                    "Agent",
                )

                message = error.get(
                    "error",
                    error.get(
                        "message",
                        "Unknown error",
                    ),
                )

                st.caption(
                    f"{agent}: {message}"
                )

            else:

                st.caption(
                    str(error)
                )

    # ========================================================
    # COMPLETION
    # ========================================================

    st.divider()

    if errors:

        st.info(
            "Mission results are available above. "
            "Review the reported issues before relying on every section."
        )

    else:

        st.success(
            "🚀 Mission Intelligence Ready — "
            "your CareerFlow AI workforce has completed "
            "the current career mission."
        )