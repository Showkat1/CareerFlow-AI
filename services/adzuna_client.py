
import os
import json
import re
import html
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api/jobs"


def clean_html(value):
    """Remove HTML tags and decode entities from job descriptions."""
    text = re.sub(r"<[^>]+>", " ", str(value or ""))
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def format_salary(job):
    """Format salary range when available."""
    minimum = job.get("salary_min")
    maximum = job.get("salary_max")

    if minimum is None and maximum is None:
        return "Not disclosed"

    currency = job.get("salary_currency", "")
    symbol = "₹" if currency.upper() == "INR" else f"{currency} "

    if minimum is not None and maximum is not None:
        return f"{symbol}{minimum:,.0f} - {maximum:,.0f}"

    amount = minimum if minimum is not None else maximum
    return f"{symbol}{amount:,.0f}"


def normalize_job(job):
    """Convert an Adzuna result into CareerFlow's job structure."""
    location = job.get("location") or {}
    company = job.get("company") or {}

    return {
        "external_id": f"adzuna-{job.get('id', '')}",
        "title": job.get("title", "Untitled"),
        "company": company.get("display_name", "Not specified"),
        "location": location.get("display_name", "Not specified"),
        "description": clean_html(job.get("description", "")),
        "job_url": job.get("redirect_url", ""),
        "source": "Adzuna",
        "salary": format_salary(job),
        "posted_date": (job.get("created") or "")[:10],
    }


def fetch_adzuna_jobs(
    query="cloud engineer",
    location="",
    country="in",
    page=1,
    results_per_page=20,
):
    """
    Fetch jobs from Adzuna.

    Requires ADZUNA_APP_ID and ADZUNA_APP_KEY environment variables.
    Raises RuntimeError if credentials or the API request fail.
    """
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")

    if not app_id or not app_key:
        raise RuntimeError("Adzuna API credentials are not configured.")

    params = {
        "app_id": app_id,
        "app_key": app_key,
        "results_per_page": results_per_page,
        "what": query,
        "content-type": "application/json",
    }

    if location:
        params["where"] = location

    url = (
        f"{ADZUNA_BASE_URL}/{country}/search/{page}?"
        f"{urlencode(params)}"
    )

    request = Request(
        url,
        headers={"Accept": "application/json"},
        method="GET",
    )

    try:
        with urlopen(request, timeout=15) as response:
            payload = json.loads(response.read().decode("utf-8"))

        results = payload.get("results", [])
        return [normalize_job(job) for job in results]

    except HTTPError as exc:
        raise RuntimeError(
            f"Adzuna returned HTTP {exc.code}."
        ) from exc

    except (URLError, TimeoutError) as exc:
        raise RuntimeError(
            f"Could not connect to Adzuna: {exc}"
        ) from exc

    except (ValueError, TypeError) as exc:
        raise RuntimeError(
            f"Invalid response from Adzuna: {exc}"
        ) from exc