import streamlit as st

from database.db import (
    get_candidate_profile,
    get_jobs,
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

        if not value:
            return []

        if "," in value:
            return [
                item.strip()
                for item in value.split(",")
                if item.strip()
            ]

        return [value]

    if isinstance(value, (list, tuple, set)):
        return [
            str(item).strip()
            for item in value
            if str(item).strip()
        ]

    return [str(value).strip()]


def normalize_jobs(value):
    if not isinstance(value, list):
        return []

    return [
        item
        for item in value
        if isinstance(item, dict)
    ]


def get_match_score(job):
    return safe_number(
        get_value(
            job,
            "match_score",
            "score",
            "match_percentage",
            "fit_score",
            default=0,
        )
    )


def get_evaluation_result(job):
    result = get_value(job, "result", default={})
    return result if isinstance(result, dict) else {}


def get_evaluation_status(job):
    status = get_value(job, "evaluation_status", default=None)

    if status:
        return str(status).upper()

    if get_value(job, "error", default=None):
        return "FAILED"

    return "SUCCESS"


def get_breakdown(job):
    breakdown = get_evaluation_result(job).get(
        "score_breakdown",
        {},
    )
    return breakdown if isinstance(breakdown, dict) else {}


def get_match_field(job, *keys, default=None):
    value = get_value(job, *keys, default=None)

    if value is not None:
        return value

    return get_value(
        get_evaluation_result(job),
        *keys,
        default=default,
    )


def get_job_title(job):
    return get_value(
        job,
        "title",
        "job_title",
        "role",
        "position",
        default="Career Opportunity",
    )


def get_company(job):
    return get_value(
        job,
        "company",
        "company_name",
        "organization",
        default="Company",
    )


def get_location(job):
    return get_value(
        job,
        "location",
        "job_location",
        default="Location not specified",
    )


def get_job_url(job):
    return get_value(
        job,
        "url",
        "job_url",
        "link",
        default="",
    )


def match_label(score):
    if score >= 85:
        return "Excellent Match"

    if score >= 75:
        return "Strong Match"

    if score >= 60:
        return "Good Match"

    if score >= 40:
        return "Potential Match"

    return "Low Alignment"


def match_message(score):
    if score >= 85:
        return (
            "Your profile has strong alignment with "
            "this opportunity."
        )

    if score >= 75:
        return (
            "Your profile aligns well with the "
            "requirements of this opportunity."
        )

    if score >= 60:
        return (
            "There is meaningful alignment with "
            "some areas that may need improvement."
        )

    if score >= 40:
        return (
            "This opportunity has some alignment, "
            "but several areas may require attention."
        )

    return (
        "The current profile shows limited alignment "
        "with this opportunity."
    )


# ============================================================
# JOB CARD
# ============================================================

def render_match_card(job, index):
    title = get_job_title(job)
    company = get_company(job)
    location = get_location(job)
    url = get_job_url(job)
    score = get_match_score(job)

    evaluation_status = get_evaluation_status(job)

    reason = get_match_field(
        job,
        "match_reason",
        "reason",
        "why_match",
        "match_explanation",
        "explanation",
        default="",
    )

    matching_skills = as_list(
        get_match_field(
            job,
            "matching_skills",
            "matched_skills",
            "skills_match",
            "common_skills",
            default=[],
        )
    )

    missing_skills = as_list(
        get_match_field(
            job,
            "missing_skills",
            "skill_gaps",
            "gaps",
            "skills_gap",
            default=[],
        )
    )

    recommendations = as_list(
        get_match_field(
            job,
            "recommendations",
            "recommended_actions",
            "actions",
            "recommendation",
            default=[],
        )
    )

    label = match_label(score)

    with st.container(border=True):

        # HEADER
        left, right = st.columns([4.5, 1.2])

        with left:
            st.markdown(f"### {title}")
            st.caption(f"🏢 {company} · 📍 {location}")

        with right:
            st.metric("Match", f"{score:.0f}%")
            st.caption(label)

        # MATCH PROGRESS
        if evaluation_status != "FAILED":
            st.progress(
                min(max(score / 100, 0), 1),
                text=f"Career Fit · {score:.0f}%",
            )

        if evaluation_status == "FAILED":
            st.warning(
                "Evaluation failed — this is not a "
                "verified current match score."
            )
        else:
            breakdown = get_breakdown(job)

            if breakdown:
                st.markdown("**Match Score Breakdown**")

                cols = st.columns(4)

                for col, key, label in zip(
                    cols,
                    (
                        "skills",
                        "experience",
                        "role_alignment",
                        "evidence",
                    ),
                    (
                        "Skills",
                        "Experience",
                        "Role alignment",
                        "Evidence",
                    ),
                ):
                    value = safe_number(
                        breakdown.get(key),
                        None,
                    )

                    with col:
                        st.metric(
                            label,
                            "—" if value is None else f"{value:.0f}%",
                        )

        # WHY MATCH
        if reason:
            st.markdown("**Why this opportunity matches**")
            st.write(reason)
        else:
            st.caption(match_message(score))

        # SKILLS
        skill_left, skill_right = st.columns(2)

        with skill_left:
            if matching_skills:
                st.markdown("**✓ Matching Skills**")

                for skill in matching_skills[:8]:
                    st.write(f"• {skill}")
            else:
                st.caption(
                    "No specific matching skills were returned."
                )

        with skill_right:
            if missing_skills:
                st.markdown("**△ Skill Gaps**")

                for gap in missing_skills[:8]:
                    st.write(f"• {gap}")
            else:
                st.success(
                    "No major skill gaps identified."
                )

        # RECOMMENDATIONS
        if recommendations:
            with st.expander("⚡ Recommended Actions"):
                for action in recommendations[:8]:
                    st.write(f"• {action}")

        # ACTION
        if url:
            st.link_button(
                "View Opportunity ↗",
                url,
                use_container_width=True,
            )


# ============================================================
# MAIN PAGE
# ============================================================

def show_matches():

    # HEADER
    st.caption("CAREERFLOW AI · MATCH INTELLIGENCE")
    st.title("🎯 Job Matches")

    st.write(
        "Explore opportunities evaluated against your "
        "career profile by the CareerFlow AI Matching Agent."
    )

    # LOAD DATA
    try:
        candidate = get_candidate_profile()
    except Exception:
        candidate = None

    try:
        jobs = get_jobs()
    except Exception:
        jobs = []

    # PROFILE
    profile = {}

    if isinstance(candidate, dict):
        profile = candidate.get("profile", {}) or {}

    if not isinstance(profile, dict):
        profile = {}

    candidate_name = get_value(
        profile,
        "name",
        "candidate_name",
        "full_name",
        default="Career Professional",
    )

    # MISSION CONTEXT
    context = st.session_state.get(
        "career_mission_context"
    )

    mission_matches = []

    if context:
        mission_matches = normalize_jobs(
            getattr(
                context,
                "matched_jobs",
                [],
            )
        )

    # FALLBACK
    database_jobs = normalize_jobs(jobs)

    if mission_matches:
        matches = mission_matches
        source_label = "Personalized Career Mission results"
    else:
        matches = database_jobs
        source_label = "Available opportunities"

    # EMPTY STATE
    if not matches:
        st.divider()

        with st.container(border=True):
            st.markdown("### 🚀 No personalized matches yet")

            st.write(
                f"Welcome, {candidate_name}. "
                "Run a Career Mission to let the "
                "Matching Agent evaluate opportunities "
                "against your profile."
            )

            st.info(
                "CareerFlow AI uses your resume intelligence, "
                "career goal, skills, and opportunity "
                "requirements to generate personalized matches."
            )

        return

    # NORMALIZE / SORT
    matches = sorted(
        matches,
        key=get_match_score,
        reverse=True,
    )

    # SUMMARY
    valid_matches = [
        job
        for job in matches
        if get_evaluation_status(job) != "FAILED"
    ]

    scores = [
        get_match_score(job)
        for job in valid_matches
        if get_match_score(job) > 0
    ]

    average_score = (
        sum(scores) / len(scores)
        if scores
        else 0
    )

    strong_matches = sum(
        1
        for score in scores
        if score >= 75
    )

    skill_gap_count = 0

    for job in matches:
        gaps = as_list(
            get_value(
                job,
                "missing_skills",
                "skill_gaps",
                "gaps",
                default=[],
            )
        )

        skill_gap_count += len(gaps)

    failed_evaluations = sum(
        1
        for job in matches
        if get_evaluation_status(job) == "FAILED"
    )

    # MATCH SNAPSHOT
    st.subheader("Match Intelligence")
    st.caption(source_label)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Opportunities", len(matches))

    with c2:
        st.metric("Average Match", f"{average_score:.0f}%")

    with c3:
        st.metric("Strong Matches", strong_matches)

    with c4:
        st.metric("Skill Gaps", skill_gap_count)

    if failed_evaluations:
        st.warning(
            f"{failed_evaluations} evaluation(s) failed. "
            "They are excluded from match averages."
        )

    # MISSION CONTEXT
    if context:
        st.divider()
        st.subheader("⚡ Mission Match Results")

        goal = getattr(
            context,
            "user_goal",
            "",
        )

        if goal:
            st.info(f"**Career Goal:** {goal}")

        st.caption(
            "These opportunities were evaluated as part "
            "of your Career Mission."
        )

    # FILTERS
    st.divider()
    st.subheader("🔎 Explore Matches")

    f1, f2 = st.columns(2)

    with f1:
        minimum_score = st.slider(
            "Minimum Match Score",
            min_value=0,
            max_value=100,
            value=0,
            step=5,
        )

    with f2:
        search_text = st.text_input(
            "Search opportunities",
            placeholder="Role, company, skill...",
        )

    filtered_matches = []
    search_value = search_text.strip().lower()

    for job in matches:
        score = get_match_score(job)

        if score < minimum_score:
            continue

        if search_value:
            searchable = " ".join(
                [
                    str(get_job_title(job)),
                    str(get_company(job)),
                    str(get_location(job)),
                    " ".join(
                        as_list(
                            get_value(
                                job,
                                "matching_skills",
                                "matched_skills",
                                default=[],
                            )
                        )
                    ),
                ]
            ).lower()

            if search_value not in searchable:
                continue

        filtered_matches.append(job)

    st.caption(
        f"Showing {len(filtered_matches)} "
        f"of {len(matches)} opportunities"
    )

    # NO FILTER RESULTS
    if not filtered_matches:
        st.warning(
            "No opportunities match your current filters."
        )
        return

    # MATCH CARDS
    for index, job in enumerate(
        filtered_matches,
        start=1,
    ):
        render_match_card(job, index)

    # CAREER INSIGHT
    st.divider()
    st.subheader("🧠 Career Insight")

    top_job = filtered_matches[0]
    top_title = get_job_title(top_job)
    top_score = get_match_score(top_job)

    top_skills = as_list(
        get_value(
            top_job,
            "matching_skills",
            "matched_skills",
            default=[],
        )
    )

    top_gaps = as_list(
        get_value(
            top_job,
            "missing_skills",
            "skill_gaps",
            "gaps",
            default=[],
        )
    )

    insight_left, insight_right = st.columns(2)

    with insight_left:
        with st.container(border=True):
            st.markdown("### 🎯 Strongest Current Alignment")
            st.markdown(f"**{top_title}**")
            st.metric("Match Score", f"{top_score:.0f}%")

            if top_skills:
                st.caption("Key matching capabilities")

                for skill in top_skills[:5]:
                    st.write(f"• {skill}")

    with insight_right:
        with st.container(border=True):
            st.markdown("### 📚 Development Focus")

            if top_gaps:
                st.caption(
                    "Skills that may improve your alignment"
                )

                for gap in top_gaps[:5]:
                    st.write(f"• {gap}")
            else:
                st.success(
                    "No major skill gaps identified."
                )

    # WORKFLOW
    st.divider()
    st.subheader("🔄 What happens next?")

    workflow = st.columns(4)

    steps = [
        (
            "01",
            "Evaluate",
            "Review your strongest matches.",
        ),
        (
            "02",
            "Apply",
            "Use Application Intelligence.",
        ),
        (
            "03",
            "Prepare",
            "Practice with Interview Intelligence.",
        ),
        (
            "04",
            "Improve",
            "Close skill gaps with Learning Intelligence.",
        ),
    ]

    for index, (number, title, description) in enumerate(steps):
        with workflow[index]:
            with st.container(border=True):
                st.caption(number)
                st.markdown(f"**{title}**")
                st.caption(description)

    st.success(
        "Discover → Match → Apply → Interview → "
        "Learn → Improve"
    )