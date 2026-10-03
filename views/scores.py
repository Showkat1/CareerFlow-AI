import streamlit as st

from database.db import get_candidate_profile


# ============================================================
# HELPERS
# ============================================================

def safe_number(value, default=0):
    """
    Safely convert a value to a number.
    """

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def get_value(data, *keys, default=0):
    """
    Safely retrieve the first available value from a dictionary.
    """

    if not isinstance(data, dict):
        return default

    for key in keys:

        value = data.get(key)

        if value is not None:
            return value

    return default


def normalize_score(score):
    """
    Normalize resume_score so CareerFlow can handle
    both old and new data formats.

    Supported:

        82

    or:

        {
            "overall": 82,
            "ats_compatibility": 85,
            "skills": 90,
            ...
        }
    """

    # New/simple format:
    # resume_score = 82

    if isinstance(score, (int, float)):

        return {
            "overall": float(score),
            "ats_compatibility": 0,
            "skills": 0,
            "experience": 0,
            "keywords": 0,
            "formatting": 0,
        }

    # Detailed format:
    # resume_score = {...}

    if isinstance(score, dict):

        return {
            "overall": safe_number(
                get_value(
                    score,
                    "overall",
                    "overall_score",
                    "total",
                    "score",
                    default=0,
                )
            ),

            "ats_compatibility": safe_number(
                get_value(
                    score,
                    "ats_compatibility",
                    "ats",
                    "ats_score",
                    default=0,
                )
            ),

            "skills": safe_number(
                get_value(
                    score,
                    "skills",
                    "skill_score",
                    default=0,
                )
            ),

            "experience": safe_number(
                get_value(
                    score,
                    "experience",
                    "experience_score",
                    default=0,
                )
            ),

            "keywords": safe_number(
                get_value(
                    score,
                    "keywords",
                    "keyword_score",
                    default=0,
                )
            ),

            "formatting": safe_number(
                get_value(
                    score,
                    "formatting",
                    "formatting_score",
                    default=0,
                )
            ),
        }

    # Unknown format

    return {
        "overall": 0,
        "ats_compatibility": 0,
        "skills": 0,
        "experience": 0,
        "keywords": 0,
        "formatting": 0,
    }


def clamp_score(value):
    """
    Keep score between 0 and 100.
    """

    value = safe_number(
        value,
        0,
    )

    return min(
        max(
            value,
            0,
        ),
        100,
    )


def score_label(score):

    if score >= 85:
        return "Excellent"

    if score >= 75:
        return "Strong"

    if score >= 60:
        return "Good"

    if score >= 40:
        return "Needs Improvement"

    return "Needs Attention"


# ============================================================
# MAIN PAGE
# ============================================================

def show_scores():

    # ========================================================
    # HEADER
    # ========================================================

    st.caption(
        "CAREERFLOW AI · RESUME INTELLIGENCE"
    )

    st.title(
        "📊 Resume Score"
    )

    st.caption(
        "AI assessment of your resume readiness."
    )

    st.write(
        "Understand how your resume performs across "
        "ATS compatibility, skills, experience, keywords, "
        "and formatting."
    )

    st.divider()

    # ========================================================
    # LOAD PROFILE
    # ========================================================

    try:

        saved = get_candidate_profile()

    except Exception as exc:

        st.error(
            f"Unable to load your resume profile: {exc}"
        )

        return

    # ========================================================
    # EMPTY STATE
    # ========================================================

    if not saved:

        st.info(
            "Upload and analyze your resume first."
        )

        return

    # ========================================================
    # PROFILE
    # ========================================================

    profile = saved.get(
        "profile",
        {},
    )

    if not isinstance(
        profile,
        dict,
    ):

        st.error(
            "The saved resume profile has an invalid format."
        )

        return

    # ========================================================
    # RESUME SCORE
    # ========================================================

    raw_score = profile.get(
        "resume_score",
        0,
    )

    score = normalize_score(
        raw_score
    )

    overall = clamp_score(
        score["overall"]
    )

    # ========================================================
    # PROFILE HEADER
    # ========================================================

    candidate_name = profile.get(
        "name",
        "Candidate",
    )

    headline = profile.get(
        "headline",
        "Career Professional",
    )

    with st.container(
        border=True
    ):

        col1, col2 = st.columns(
            [3, 1]
        )

        with col1:

            st.subheader(
                candidate_name
            )

            st.caption(
                headline
            )

            st.write(
                "Your CareerFlow AI resume intelligence "
                "profile is being used to evaluate your "
                "career readiness."
            )

        with col2:

            st.metric(
                "Overall Score",
                f"{overall:.0f}/100",
            )

            st.caption(
                score_label(
                    overall
                )
            )

    # ========================================================
    # OVERALL SCORE
    # ========================================================

    st.divider()

    st.subheader(
        "Overall Resume Score"
    )

    st.progress(
        overall / 100,
        text=f"{overall:.0f}/100",
    )

    if overall >= 85:

        st.success(
            "Your resume has excellent overall positioning."
        )

    elif overall >= 75:

        st.info(
            "Your resume has strong positioning with room "
            "for targeted optimization."
        )

    elif overall >= 60:

        st.warning(
            "Your resume has a good foundation but "
            "can benefit from optimization."
        )

    elif overall >= 40:

        st.warning(
            "Your resume needs improvement before "
            "targeting highly competitive roles."
        )

    else:

        st.error(
            "Your resume requires significant optimization."
        )

    # ========================================================
    # DETAILED METRICS
    # ========================================================

    st.divider()

    st.subheader(
        "Resume Analysis"
    )

    metrics = [
        (
            "ATS Compatibility",
            score["ats_compatibility"],
        ),
        (
            "Skills",
            score["skills"],
        ),
        (
            "Experience",
            score["experience"],
        ),
        (
            "Keywords",
            score["keywords"],
        ),
        (
            "Formatting",
            score["formatting"],
        ),
    ]

    # ========================================================
    # METRIC CARDS
    # ========================================================

    metric_columns = st.columns(
        5
    )

    for column, (
        label,
        value,
    ) in zip(
        metric_columns,
        metrics,
    ):

        value = clamp_score(
            value
        )

        with column:

            with st.container(
                border=True
            ):

                st.metric(
                    label,
                    f"{value:.0f}/100",
                )

                st.progress(
                    value / 100
                )

    # ========================================================
    # DETAILED ANALYSIS
    # ========================================================

    st.divider()

    st.subheader(
        "Score Details"
    )

    for label, value in metrics:

        value = clamp_score(
            value
        )

        left, right = st.columns(
            [3, 1]
        )

        with left:

            st.write(
                f"**{label}**"
            )

            st.progress(
                value / 100
            )

        with right:

            st.write(
                f"**{value:.0f}/100**"
            )

    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    st.divider()

    st.subheader(
        "🚀 Recommendations"
    )

    recommendations = profile.get(
        "career_recommendations",
        [],
    )

    # Support alternative field names too.

    if not recommendations:

        recommendations = profile.get(
            "recommendations",
            [],
        )

    if not recommendations:

        recommendations = profile.get(
            "improvements",
            [],
        )

    if isinstance(
        recommendations,
        str,
    ):

        recommendations = [
            recommendations
        ]

    if not isinstance(
        recommendations,
        list,
    ):

        recommendations = []

    if recommendations:

        for item in recommendations:

            st.info(
                f"💡 {item}"
            )

    else:

        st.info(
            "No AI recommendations are currently available."
        )

        # Generate useful recommendations from the
        # available score information.

        generated = []

        if score["ats_compatibility"] < 70:

            generated.append(
                "Improve ATS compatibility by using clear "
                "section headings, standard terminology, "
                "and job-relevant keywords."
            )

        if score["skills"] < 70:

            generated.append(
                "Strengthen the skills section with relevant "
                "technical and domain-specific capabilities."
            )

        if score["experience"] < 70:

            generated.append(
                "Add measurable achievements and business "
                "impact to your professional experience."
            )

        if score["keywords"] < 70:

            generated.append(
                "Tailor keywords to each target job description."
            )

        if score["formatting"] < 70:

            generated.append(
                "Use a clean, consistent, ATS-friendly resume format."
            )

        if not generated:

            generated.append(
                "Continue tailoring your resume for individual "
                "target roles and maintain measurable achievements."
            )

        for item in generated:

            st.info(
                f"💡 {item}"
            )

    # ========================================================
    # CAREERFLOW AI WORKFORCE
    # ========================================================

    st.divider()

    st.subheader(
        "🤖 How CareerFlow AI Uses Your Resume Score"
    )

    agent1, agent2, agent3 = st.columns(
        3
    )

    with agent1:

        with st.container(
            border=True
        ):

            st.markdown(
                "### 🔎 Job Discovery"
            )

            st.write(
                "Identifies opportunities that align "
                "with your career profile."
            )

    with agent2:

        with st.container(
            border=True
        ):

            st.markdown(
                "### 🎯 Matching"
            )

            st.write(
                "Evaluates your fit against job requirements "
                "and identifies skill gaps."
            )

    with agent3:

        with st.container(
            border=True
        ):

            st.markdown(
                "### 📚 Learning"
            )

            st.write(
                "Uses identified gaps to build a "
                "targeted learning roadmap."
            )

    # ========================================================
    # FINAL STATUS
    # ========================================================

    st.divider()

    st.success(
        "Resume Intelligence is ready. "
        "Launch a Career Mission to continue your career workflow."
    )