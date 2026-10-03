import streamlit as st

from database.db import (
    get_candidate_profile,
    save_candidate_profile,
)

from services.resume_parser import extract_resume_text
from services.ai_service import analyze_resume


# ============================================================
# HELPERS
# ============================================================

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


def safe_number(value, default=0):

    try:
        return float(value)

    except (TypeError, ValueError):

        return default


def normalize_score(score):

    if isinstance(score, (int, float)):

        return {
            "overall": float(score),
            "details": {},
        }

    if isinstance(score, dict):

        overall = get_value(
            score,
            "overall",
            "overall_score",
            "total",
            "score",
            default=0,
        )

        return {
            "overall": safe_number(
                overall
            ),
            "details": score,
        }

    return {
        "overall": 0,
        "details": {},
    }


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


def score_message(score):

    if score >= 85:

        return (
            "Your resume has strong overall positioning "
            "for targeted career opportunities."
        )

    if score >= 75:

        return (
            "Your resume has a strong foundation with "
            "some opportunities for optimization."
        )

    if score >= 60:

        return (
            "Your resume is workable, but targeted "
            "improvements can increase career matching."
        )

    if score >= 40:

        return (
            "Several areas of your resume should be improved "
            "before targeting competitive opportunities."
        )

    return (
        "Your resume needs focused optimization before "
        "starting a major application campaign."
    )


# ============================================================
# MAIN PAGE
# ============================================================

def show_resume():

    # ========================================================
    # HEADER
    # ========================================================

    st.caption(
        "CAREERFLOW AI · RESUME INTELLIGENCE"
    )

    st.title(
        "📄 My Resume"
    )

    st.write(
        "Build the career profile your AI workforce uses "
        "to discover opportunities, evaluate job fit, "
        "prepare applications, and identify skill gaps."
    )

    st.divider()

    # ========================================================
    # LOAD EXISTING PROFILE
    # ========================================================

    try:

        saved_profile = get_candidate_profile()

    except Exception as exc:

        saved_profile = None

        st.warning(
            f"Could not load the saved profile: {exc}"
        )

    existing_profile = {}
    existing_resume_text = ""
    existing_filename = ""

    if isinstance(
        saved_profile,
        dict,
    ):

        existing_profile = (
            saved_profile.get(
                "profile",
                {},
            )
            or {}
        )

        # Defensive protection against corrupted/legacy
        # database records.

        if not isinstance(
            existing_profile,
            dict,
        ):

            existing_profile = {}

        existing_resume_text = (
            saved_profile.get(
                "resume_text",
                "",
            )
            or ""
        )

        existing_filename = (
            saved_profile.get(
                "resume_filename",
                "",
            )
            or ""
        )

    # ========================================================
    # UPLOAD
    # ========================================================

    st.subheader(
        "Upload Your Resume"
    )

    st.caption(
        "Upload your latest resume as a PDF."
    )

    uploaded_file = st.file_uploader(
        "Resume PDF",
        type=["pdf"],
        help="Upload a text-based PDF resume.",
    )

    if uploaded_file:

        st.info(
            f"Selected resume: **{uploaded_file.name}**"
        )

        if st.button(
            "Analyze & Save Resume",
            type="primary",
            use_container_width=True,
        ):

            with st.status(
                "CareerFlow AI is processing your resume...",
                expanded=True,
            ) as status:

                try:

                    # ----------------------------------------
                    # EXTRACT
                    # ----------------------------------------

                    st.write(
                        "Extracting resume content..."
                    )

                    resume_text = extract_resume_text(
                        uploaded_file
                    )

                    if not resume_text:

                        status.update(
                            label="Resume extraction failed",
                            state="error",
                        )

                        st.error(
                            "No readable text was found in the PDF."
                        )

                        return

                    # ----------------------------------------
                    # AI ANALYSIS
                    # ----------------------------------------

                    st.write(
                        "Analyzing candidate profile..."
                    )

                    analysis = analyze_resume(
                        resume_text
                    )

                    if not isinstance(
                        analysis,
                        dict,
                    ):

                        analysis = {}

                    # ----------------------------------------
                    # PROFILE
                    # ----------------------------------------

                    profile = {

                        "name": get_value(
                            analysis,
                            "name",
                            "candidate_name",
                            "full_name",
                            default="Candidate",
                        ),

                        "headline": get_value(
                            analysis,
                            "headline",
                            "professional_title",
                            "title",
                            default="Career Professional",
                        ),

                        "summary": get_value(
                            analysis,
                            "summary",
                            "professional_summary",
                            "profile_summary",
                            default="",
                        ),

                        "skills": as_list(
                            get_value(
                                analysis,
                                "skills",
                                "technical_skills",
                                "key_skills",
                                default=[],
                            )
                        ),

                        "experience": as_list(
                            get_value(
                                analysis,
                                "experience",
                                "work_experience",
                                "experience_summary",
                                default=[],
                            )
                        ),

                        "education": as_list(
                            get_value(
                                analysis,
                                "education",
                                "education_details",
                                default=[],
                            )
                        ),

                        "certifications": as_list(
                            get_value(
                                analysis,
                                "certifications",
                                "certs",
                                default=[],
                            )
                        ),

                        "strengths": as_list(
                            get_value(
                                analysis,
                                "strengths",
                                "key_strengths",
                                default=[],
                            )
                        ),

                        "skill_gaps": as_list(
                            get_value(
                                analysis,
                                "skill_gaps",
                                "gaps",
                                "missing_skills",
                                default=[],
                            )
                        ),
                    }

                    # ----------------------------------------
                    # SCORE
                    # ----------------------------------------

                    score_value = get_value(
                        analysis,
                        "score",
                        "resume_score",
                        "overall_score",
                        default=0,
                    )

                    normalized_score = normalize_score(
                        score_value
                    )

                    profile[
                        "resume_score"
                    ] = normalized_score[
                        "overall"
                    ]

                    # ----------------------------------------
                    # FULL AI ANALYSIS
                    # ----------------------------------------

                    profile[
                        "analysis"
                    ] = analysis

                    # ----------------------------------------
                    # RECOMMENDATIONS
                    # ----------------------------------------

                    recommendations = as_list(
                        get_value(
                            analysis,
                            "career_recommendations",
                            "recommendations",
                            "improvements",
                            "suggestions",
                            default=[],
                        )
                    )

                    profile[
                        "career_recommendations"
                    ] = recommendations

                    # ----------------------------------------
                    # SAVE PROFILE
                    # ----------------------------------------

                    st.write(
                        "Saving candidate profile..."
                    )

                    # IMPORTANT:
                    # database.db.save_candidate_profile()
                    # expects:
                    #
                    #   resume_filename
                    #   resume_text
                    #   profile
                    #
                    # The database function itself converts
                    # the profile dictionary to JSON.

                    save_candidate_profile(
                        uploaded_file.name,
                        resume_text,
                        profile,
                    )

                    # ----------------------------------------
                    # SESSION STATE
                    # ----------------------------------------

                    st.session_state[
                        "resume_profile"
                    ] = profile

                    st.session_state[
                        "resume_text"
                    ] = resume_text

                    st.session_state[
                        "resume_filename"
                    ] = uploaded_file.name

                    status.update(
                        label="Resume analyzed successfully",
                        state="complete",
                        expanded=False,
                    )

                    st.success(
                        "Your resume intelligence profile "
                        "has been saved successfully."
                    )

                    st.rerun()

                except Exception as exc:

                    status.update(
                        label="Resume analysis failed",
                        state="error",
                        expanded=True,
                    )

                    st.error(
                        f"Resume processing failed: {exc}"
                    )

    # ========================================================
    # ACTIVE PROFILE
    # ========================================================

    profile = (
        st.session_state.get(
            "resume_profile"
        )
        or existing_profile
        or {}
    )

    resume_text = (
        st.session_state.get(
            "resume_text"
        )
        or existing_resume_text
        or ""
    )

    resume_filename = (
        st.session_state.get(
            "resume_filename"
        )
        or existing_filename
        or ""
    )

    # Defensive protection against corrupted data.

    if not isinstance(
        profile,
        dict,
    ):

        profile = {}

    # ========================================================
    # EMPTY STATE
    # ========================================================

    if not profile and not resume_text:

        st.divider()

        with st.container(
            border=True
        ):

            st.subheader(
                "Start Your Career Intelligence Profile"
            )

            st.write(
                "Upload your resume above to activate "
                "the Resume Intelligence Agent."
            )

            st.info(
                "Your profile becomes the foundation for "
                "job discovery, matching, applications, "
                "interview preparation, and learning."
            )

        return

    # ========================================================
    # PROFILE VALUES
    # ========================================================

    name = get_value(
        profile,
        "name",
        "candidate_name",
        "full_name",
        default="Candidate",
    )

    headline = get_value(
        profile,
        "headline",
        "professional_title",
        "title",
        default="Career Professional",
    )

    summary = get_value(
        profile,
        "summary",
        "professional_summary",
        "profile_summary",
        default="",
    )

    score_raw = get_value(
        profile,
        "resume_score",
        "score",
        default=0,
    )

    score_info = normalize_score(
        score_raw
    )

    overall_score = score_info[
        "overall"
    ]

    skills = as_list(
        get_value(
            profile,
            "skills",
            "technical_skills",
            "key_skills",
            default=[],
        )
    )

    experience = as_list(
        get_value(
            profile,
            "experience",
            "work_experience",
            default=[],
        )
    )

    education = as_list(
        get_value(
            profile,
            "education",
            default=[],
        )
    )

    certifications = as_list(
        get_value(
            profile,
            "certifications",
            "certs",
            default=[],
        )
    )

    strengths = as_list(
        get_value(
            profile,
            "strengths",
            "key_strengths",
            default=[],
        )
    )

    skill_gaps = as_list(
        get_value(
            profile,
            "skill_gaps",
            "gaps",
            "missing_skills",
            default=[],
        )
    )

    # ========================================================
    # PROFILE HEADER
    # ========================================================

    st.divider()

    st.subheader(
        "Candidate Profile"
    )

    with st.container(
        border=True
    ):

        col_profile, col_score = st.columns(
            [3.5, 1]
        )

        with col_profile:

            st.markdown(
                f"## {name}"
            )

            st.markdown(
                f"**{headline}**"
            )

            if summary:

                st.write(
                    summary
                )

            if resume_filename:

                st.caption(
                    f"Resume: {resume_filename}"
                )

        with col_score:

            st.metric(
                "Resume Score",
                f"{overall_score:.0f}/100",
            )

            st.caption(
                score_label(
                    overall_score
                )
            )

    # ========================================================
    # SCORE
    # ========================================================

    st.write("")

    st.progress(
        min(
            max(
                overall_score / 100,
                0,
            ),
            1,
        ),
        text=(
            f"Resume Strength · "
            f"{overall_score:.0f}%"
        ),
    )

    if overall_score >= 80:

        st.success(
            score_message(
                overall_score
            )
        )

    elif overall_score >= 60:

        st.info(
            score_message(
                overall_score
            )
        )

    else:

        st.warning(
            score_message(
                overall_score
            )
        )

    # ========================================================
    # SNAPSHOT
    # ========================================================

    st.divider()

    st.subheader(
        "Profile Snapshot"
    )

    c1, c2, c3, c4 = st.columns(
        4
    )

    with c1:

        st.metric(
            "Skills",
            len(skills),
        )

    with c2:

        st.metric(
            "Experience",
            len(experience),
        )

    with c3:

        st.metric(
            "Certifications",
            len(certifications),
        )

    with c4:

        st.metric(
            "Skill Gaps",
            len(skill_gaps),
        )

    # ========================================================
    # TABS
    # ========================================================

    st.divider()

    tabs = st.tabs(
        [
            "Skills",
            "Strengths",
            "Skill Gaps",
            "Experience",
            "Education",
            "Certifications",
            "AI Analysis",
            "Resume Text",
        ]
    )

    # ========================================================
    # SKILLS
    # ========================================================

    with tabs[0]:

        st.subheader(
            "Core Skills"
        )

        if skills:

            columns = st.columns(3)

            for index, skill in enumerate(
                skills
            ):

                with columns[
                    index % 3
                ]:

                    st.info(
                        f"**{skill}**"
                    )

        else:

            st.info(
                "No skills were extracted."
            )

    # ========================================================
    # STRENGTHS
    # ========================================================

    with tabs[1]:

        st.subheader(
            "Professional Strengths"
        )

        if strengths:

            for strength in strengths:

                st.success(
                    strength
                )

        else:

            st.info(
                "No explicit strengths were identified yet."
            )

    # ========================================================
    # SKILL GAPS
    # ========================================================

    with tabs[2]:

        st.subheader(
            "Priority Skill Gaps"
        )

        if skill_gaps:

            for gap in skill_gaps:

                st.warning(
                    gap
                )

        else:

            st.success(
                "No major skill gaps were identified."
            )

    # ========================================================
    # EXPERIENCE
    # ========================================================

    with tabs[3]:

        st.subheader(
            "Professional Experience"
        )

        if experience:

            for item in experience:

                with st.container(
                    border=True
                ):

                    st.write(
                        str(item)
                    )

        else:

            st.info(
                "No detailed experience information was extracted."
            )

    # ========================================================
    # EDUCATION
    # ========================================================

    with tabs[4]:

        st.subheader(
            "Education"
        )

        if education:

            for item in education:

                st.write(
                    f"• {item}"
                )

        else:

            st.info(
                "No education information was extracted."
            )

    # ========================================================
    # CERTIFICATIONS
    # ========================================================

    with tabs[5]:

        st.subheader(
            "Certifications"
        )

        if certifications:

            for item in certifications:

                st.success(
                    item
                )

        else:

            st.info(
                "No certifications were extracted."
            )

    # ========================================================
    # AI ANALYSIS
    # ========================================================

    with tabs[6]:

        st.subheader(
            "Resume Intelligence"
        )

        analysis = get_value(
            profile,
            "analysis",
            "resume_analysis",
            default={},
        )

        if not isinstance(
            analysis,
            dict,
        ):

            analysis = {}

        recommendations = as_list(
            get_value(
                analysis,
                "recommendations",
                "career_recommendations",
                "improvements",
                "suggestions",
                default=[],
            )
        )

        if recommendations:

            st.markdown(
                "### Recommended Improvements"
            )

            for item in recommendations:

                st.info(
                    item
                )

        with st.expander(
            "View Complete AI Analysis"
        ):

            if analysis:

                st.json(
                    analysis
                )

            else:

                st.info(
                    "Detailed AI analysis is not available."
                )

    # ========================================================
    # RESUME TEXT
    # ========================================================

    with tabs[7]:

        st.subheader(
            "Extracted Resume Text"
        )

        if resume_text:

            st.text_area(
                "Resume content",
                value=resume_text,
                height=500,
                disabled=True,
                label_visibility="collapsed",
            )

        else:

            st.info(
                "No extracted resume text is available."
            )

    # ========================================================
    # AI WORKFORCE
    # ========================================================

    st.divider()

    st.subheader(
        "Your AI Career Workforce"
    )

    w1, w2, w3 = st.columns(3)

    with w1:

        with st.container(
            border=True
        ):

            st.markdown(
                "### Job Discovery"
            )

            st.write(
                "Finds relevant opportunities based "
                "on your career profile."
            )

    with w2:

        with st.container(
            border=True
        ):

            st.markdown(
                "### Matching Agent"
            )

            st.write(
                "Evaluates your fit against job "
                "requirements."
            )

    with w3:

        with st.container(
            border=True
        ):

            st.markdown(
                "### Learning Agent"
            )

            st.write(
                "Uses your skill gaps to create "
                "a development roadmap."
            )

    # ========================================================
    # FINAL STATUS
    # ========================================================

    st.divider()

    st.success(
        "Resume Intelligence is ready. "
        "Launch a Career Mission to activate your AI workforce."
    )