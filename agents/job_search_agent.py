
import os

from core.agent_base import BaseAgent, AgentResult
from database.db import (
    get_job_preferences,
    save_job,
    log_agent_activity,
)
from services.job_source import get_demo_jobs
from services.adzuna_client import fetch_adzuna_jobs


def normalize_location(value):
    """Normalize location text for comparison."""
    return [
        part.strip().casefold()
        for part in value.split(",")
        if part.strip()
    ]


def matches_location(job_location, preferences):
    """Check whether a demo job matches saved location preferences."""
    preferred_locations = preferences.get("locations", [])

    if not preferred_locations:
        return True

    job_parts = normalize_location(job_location)

    if not job_parts:
        return False

    for preferred in preferred_locations:
        preferred_parts = normalize_location(preferred)

        if not preferred_parts:
            continue

        if len(preferred_parts) == 1:
            if preferred_parts[0] in job_parts:
                return True
            continue

        preferred_specific = preferred_parts[:-1]
        job_specific = job_parts[:-1]

        if preferred_specific and preferred_specific == job_specific:
            return True

        if (
            "remote" in preferred_parts
            and "remote" in job_parts
        ):
            return True

    return False


class JobSearchAgent(BaseAgent):

    name = "Job Discovery Agent"

    description = (
        "Discovers and stores relevant job opportunities "
        "from live and demo sources."
    )

    def __init__(self):
        super().__init__()

    def process_jobs(self, jobs):
        saved = 0
        duplicates = 0

        for job in jobs:
            result = save_job(job)

            if result:
                saved += 1
            else:
                duplicates += 1

        log_agent_activity(
            self.name,
            "Job ingestion",
            "SUCCESS",
            (
                f"Processed {len(jobs)} jobs. "
                f"Saved {saved}; "
                f"duplicates {duplicates}."
            ),
        )

        return {
            "saved": saved,
            "duplicates": duplicates,
            "total": len(jobs),
        }

    def execute(self, context):
        self.set_status("RUNNING")

        try:
            preferences = get_job_preferences()

            preferred_locations = preferences.get("locations", [])
            api_location = (
                preferred_locations[0]
                if preferred_locations
                else ""
            )

            query = os.getenv(
                "ADZUNA_QUERY",
                "cloud engineer",
            )

            country = os.getenv(
                "ADZUNA_COUNTRY",
                "in",
            )

            jobs = []
            source = "Adzuna"
            fallback_reason = None

            try:
                live_jobs = fetch_adzuna_jobs(
                    query=query,
                    location=api_location,
                    country=country,
                    results_per_page=20,
                )

                if live_jobs:
                    jobs = live_jobs
                else:
                    fallback_reason = (
                        "Adzuna returned no matching jobs."
                    )

            except Exception as exc:
                fallback_reason = str(exc)

            if not jobs:
                source = "Demo"
                all_demo_jobs = get_demo_jobs()

                jobs = [
                    job
                    for job in all_demo_jobs
                    if matches_location(
                        job.get("location", ""),
                        preferences,
                    )
                ]

            result = self.process_jobs(jobs)

            context.discovered_jobs = jobs

            self.set_status("COMPLETED")

            message = (
                f"Discovered {len(jobs)} opportunities "
                f"using {source}."
            )

            if fallback_reason:
                message += (
                    f" Live source unavailable or empty: "
                    f"{fallback_reason}"
                )

            return AgentResult(
                success=True,
                message=message,
                data={
                    **result,
                    "source": source,
                    "query": query,
                    "location": api_location,
                    "fallback_reason": fallback_reason,
                },
            )

        except Exception as exc:
            self.set_status("FAILED")

            log_agent_activity(
                self.name,
                "Job discovery",
                "FAILED",
                str(exc),
            )

            return AgentResult(
                success=False,
                message=str(exc),
            )