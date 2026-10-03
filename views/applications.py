import streamlit as st

from database.db import (
    get_applications,
    update_application_status,
)


PIPELINE_STATUSES = [
    "APPLIED",
    "SCREENING",
    "ASSESSMENT",
    "INTERVIEW",
    "OFFER",
    "REJECTED",
    "WITHDRAWN",
]

STATUS_LABELS = {
    "READY_TO_APPLY": "Ready to Apply",
    "APPLIED": "Applied",
    "SCREENING": "Screening",
    "ASSESSMENT": "Assessment",
    "INTERVIEW": "Interview",
    "OFFER": "Offer",
    "REJECTED": "Rejected",
    "WITHDRAWN": "Withdrawn",
}


def _format_status(status):
    return STATUS_LABELS.get(
        status,
        str(status).replace("_", " ").title()
    )


def _render_job_details(application):
    title = application.get("title") or "Untitled role"
    company = application.get("company") or "Company not specified"
    location = application.get("location") or "Location not specified"

    score = application.get("match_score")
    try:
        score_text = f"{float(score or 0):.0f}%"
    except (TypeError, ValueError):
        score_text = "—"

    st.markdown(f"### {title}")
    st.write(f"**{company}** · {location}")

    left, right = st.columns([1, 2])
    left.metric("Match score", score_text)

    applied_at = application.get("applied_at")
    if applied_at:
        right.caption(f"Applied on: {applied_at}")

    job_url = application.get("job_url")
    if job_url and str(job_url).startswith(("https://", "http://")):
        st.link_button(
            "Open original job listing",
            job_url,
            use_container_width=False
        )


def _render_queue_item(application):
    application_id = application["id"]

    with st.container(border=True):
        _render_job_details(application)

        st.caption(
            "Review the role and submit your application on the "
            "employer's website before marking it as applied."
        )

        if st.button(
            "Mark as Applied",
            key=f"queue_applied_{application_id}",
            type="primary",
            use_container_width=True,
        ):
            updated = update_application_status(
                application_id,
                "APPLIED"
            )

            if updated:
                st.success("Application moved to your tracker.")
            else:
                st.error("The application could not be updated.")

            st.rerun()


def _render_tracker_item(application):
    application_id = application["id"]
    current_status = application.get("status", "APPLIED")

    with st.container(border=True):
        _render_job_details(application)

        st.write(f"**Current status:** {_format_status(current_status)}")

        status_options = PIPELINE_STATUSES
        selected_status = st.selectbox(
            "Update application status",
            options=status_options,
            index=(
                status_options.index(current_status)
                if current_status in status_options
                else 0
            ),
            format_func=_format_status,
            key=f"tracker_status_{application_id}",
        )

        if st.button(
            "Save status",
            key=f"tracker_save_{application_id}",
            use_container_width=True,
        ):
            if selected_status == current_status:
                st.info("No status changes to save.")
            else:
                updated = update_application_status(
                    application_id,
                    selected_status
                )

                if updated:
                    st.success("Application status updated.")
                else:
                    st.error("The application could not be updated.")

                st.rerun()


def show_application_queue():
    st.title("📥 Application Queue")
    st.caption(
        "Review prepared applications and track which ones are ready "
        "for submission."
    )

    queued = get_applications(status="READY_TO_APPLY")

    st.metric("Ready to apply", len(queued))
    st.divider()

    if not queued:
        st.info(
            "Your application queue is empty. Save an application "
            "from a job match to see it here."
        )
        return

    search = st.text_input(
        "Search queued applications",
        placeholder="Search by job title, company, or location",
        key="queue_search",
    )

    search_term = search.strip().lower()

    visible = [
        application
        for application in queued
        if not search_term
        or search_term in str(application.get("title", "")).lower()
        or search_term in str(application.get("company", "")).lower()
        or search_term in str(application.get("location", "")).lower()
    ]

    st.caption(f"Showing {len(visible)} of {len(queued)} queued applications")

    for application in visible:
        _render_queue_item(application)


def show_applications():
    st.title("📤 Applications")
    st.caption(
        "Track the progress of applications you have marked as submitted."
    )

    applications = get_applications(status=PIPELINE_STATUSES)

    total = len(applications)
    active = sum(
        application.get("status") in {"APPLIED", "SCREENING", "ASSESSMENT", "INTERVIEW"}
        for application in applications
    )
    interviews = sum(
        application.get("status") == "INTERVIEW"
        for application in applications
    )
    offers = sum(
        application.get("status") == "OFFER"
        for application in applications
    )

    metric_columns = st.columns(4)
    metric_columns[0].metric("Tracked", total)
    metric_columns[1].metric("Active", active)
    metric_columns[2].metric("Interviews", interviews)
    metric_columns[3].metric("Offers", offers)

    st.divider()

    if not applications:
        st.info(
            "No submitted applications to track yet. "
            "After submitting an application externally, mark it as "
            "applied in the Application Queue."
        )
        return

    filter_options = ["All"] + PIPELINE_STATUSES

    selected_status = st.selectbox(
        "Filter by status",
        options=filter_options,
        format_func=lambda value: (
            "All statuses" if value == "All" else _format_status(value)
        ),
        key="applications_filter",
    )

    search = st.text_input(
        "Search applications",
        placeholder="Search by job title, company, or location",
        key="applications_search",
    )

    search_term = search.strip().lower()

    visible = [
        application
        for application in applications
        if (
            selected_status == "All"
            or application.get("status") == selected_status
        )
        and (
            not search_term
            or search_term in str(application.get("title", "")).lower()
            or search_term in str(application.get("company", "")).lower()
            or search_term in str(application.get("location", "")).lower()
        )
    ]

    st.caption(f"Showing {len(visible)} of {total} applications")

    for application in visible:
        _render_tracker_item(application)