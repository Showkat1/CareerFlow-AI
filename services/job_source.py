from datetime import date


def get_demo_jobs():

    today = str(date.today())

    return [

        {
            "external_id": "demo-001",
            "title": "Cloud Engineer",
            "company": "Demo Technologies",
            "location": "Bangalore, India",
            "description": """
            We are looking for a Cloud Engineer with
            experience in AWS, Linux, networking, Python,
            cloud infrastructure and automation.
            """,
            "job_url": "https://example.com/job/001",
            "source": "Demo",
            "salary": "₹12-18 LPA",
            "posted_date": today
        },

        {
            "external_id": "demo-002",
            "title": "AWS Cloud Engineer",
            "company": "Cloud Systems",
            "location": "Remote, India",
            "description": """
            AWS Cloud Engineer required with experience
            in AWS, EC2, S3, IAM, Python and Terraform.
            """,
            "job_url": "https://example.com/job/002",
            "source": "Demo",
            "salary": "₹15-22 LPA",
            "posted_date": today
        },

        {
            "external_id": "demo-003",
            "title": "Frontend Developer",
            "company": "Web Solutions",
            "location": "Delhi, India",
            "description": """
            Looking for a React and JavaScript developer
            with frontend development experience.
            """,
            "job_url": "https://example.com/job/003",
            "source": "Demo",
            "salary": "₹8-12 LPA",
            "posted_date": today
        },

        {
            "external_id": "demo-004",
            "title": "DevOps Engineer",
            "company": "CloudOps Labs",
            "location": "Remote, India",
            "description": """
            DevOps Engineer with AWS, Docker, Kubernetes,
            Terraform, CI/CD, Linux and Python experience.
            """,
            "job_url": "https://example.com/job/004",
            "source": "Demo",
            "salary": "₹14-24 LPA",
            "posted_date": today
        }
    ]