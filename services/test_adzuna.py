from services.adzuna_client import fetch_adzuna_jobs

jobs = fetch_adzuna_jobs(
    query="cloud engineer",
    location="Kolkata",
    country="in",
    results_per_page=5,
)

print(f"Jobs received: {len(jobs)}")

for job in jobs:
    print("-" * 40)
    print(job["title"])
    print(job["company"])
    print(job["location"])
    print(job["salary"])
    print(job["job_url"])