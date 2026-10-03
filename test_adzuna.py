
from services.adzuna_client import fetch_adzuna_jobs

try:
    jobs = fetch_adzuna_jobs(
        query="cloud engineer",
        location="Kolkata",
        country="in",
        results_per_page=5,
    )

    print(f"Jobs received: {len(jobs)}")

    for job in jobs:
        print("\n" + "=" * 40)
        print("Title:", job["title"])
        print("Company:", job["company"])
        print("Location:", job["location"])
        print("Salary:", job["salary"])
        print("URL:", job["job_url"])

except Exception as exc:
    print(f"Adzuna test failed: {exc}")