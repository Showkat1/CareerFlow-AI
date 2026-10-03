import streamlit as st

from database.db import (
    get_jobs,
    get_applications
)


def show_analytics():

    st.title("📈 Analytics")

    st.caption(
        "Understand your job search performance."
    )

    st.divider()

    jobs = get_jobs()
    applications = get_applications()

    total_jobs = len(jobs)

    high_matches = len([
        job
        for job in jobs
        if job.get("match_score", 0) >= 80
    ])

    total_applications = len(
        applications
    )

    interviews = len([
        app
        for app in applications
        if app["status"] == "INTERVIEW"
    ])

    offers = len([
        app
        for app in applications
        if app["status"] == "OFFER"
    ])

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Jobs",
            total_jobs
        )

    with col2:
        st.metric(
            "Strong Matches",
            high_matches
        )

    with col3:
        st.metric(
            "Applications",
            total_applications
        )

    with col4:
        st.metric(
            "Interviews",
            interviews
        )

    with col5:
        st.metric(
            "Offers",
            offers
        )

    st.divider()

    if total_jobs:

        match_rate = (
            high_matches / total_jobs
        ) * 100

        st.subheader(
            "Job Match Rate"
        )

        st.progress(
            match_rate / 100
        )

        st.caption(
            f"{match_rate:.1f}% of discovered "
            "jobs are strong matches."
        )

    if total_applications:

        interview_rate = (
            interviews /
            total_applications
        ) * 100

        st.subheader(
            "Interview Conversion"
        )

        st.progress(
            interview_rate / 100
        )

        st.caption(
            f"{interview_rate:.1f}% of applications "
            "have reached interview stage."
        )