import json
import sqlite3
from pathlib import Path

DB_PATH = Path("data/jobs.db")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                external_id TEXT UNIQUE,
                title TEXT NOT NULL,
                company TEXT,
                location TEXT,
                description TEXT,
                job_url TEXT,
                source TEXT,
                salary TEXT,
                posted_date TEXT,
                match_score REAL DEFAULT 0,
                match_reason TEXT,
                status TEXT DEFAULT 'NEW',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS candidate_profile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resume_filename TEXT,
                resume_text TEXT,
                profile_json TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS job_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_roles TEXT,
                locations TEXT,
                work_modes TEXT,
                experience_level TEXT,
                minimum_salary TEXT,
                industries TEXT,
                keywords TEXT,
                excluded_keywords TEXT,
                minimum_match_score INTEGER DEFAULT 70,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER,
                status TEXT DEFAULT 'READY_TO_APPLY',
                resume_version TEXT,
                cover_letter TEXT,
                application_answers TEXT,
                notes TEXT,
                applied_at TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(job_id) REFERENCES jobs(id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent TEXT,
                action TEXT,
                status TEXT,
                details TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.commit()
    finally:
        connection.close()


# Candidate profile

def save_candidate_profile(resume_filename, resume_text, profile):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM candidate_profile")
        cursor.execute("""
            INSERT INTO candidate_profile (
                resume_filename, resume_text, profile_json
            )
            VALUES (?, ?, ?)
        """, (resume_filename, resume_text, json.dumps(profile)))
        connection.commit()
    finally:
        connection.close()


def get_candidate_profile():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT resume_filename, resume_text, profile_json
            FROM candidate_profile
            ORDER BY updated_at DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        if row is None:
            return None
        return {
            "resume_filename": row["resume_filename"],
            "resume_text": row["resume_text"],
            "profile": json.loads(row["profile_json"] or "{}"),
        }
    finally:
        connection.close()


def reset_candidate_profile():
    """Delete the saved resume and candidate profile only."""
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM candidate_profile")
        connection.commit()
        return cursor.rowcount
    finally:
        connection.close()


# Job preferences

def save_job_preferences(preferences):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM job_preferences")
        cursor.execute("""
            INSERT INTO job_preferences (
                target_roles, locations, work_modes, experience_level,
                minimum_salary, industries, keywords, excluded_keywords,
                minimum_match_score
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            json.dumps(preferences.get("target_roles", [])),
            json.dumps(preferences.get("locations", [])),
            json.dumps(preferences.get("work_modes", [])),
            preferences.get("experience_level", ""),
            preferences.get("minimum_salary", ""),
            json.dumps(preferences.get("industries", [])),
            json.dumps(preferences.get("keywords", [])),
            json.dumps(preferences.get("excluded_keywords", [])),
            preferences.get("minimum_match_score", 70),
        ))
        connection.commit()
    finally:
        connection.close()


def get_job_preferences():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT *
            FROM job_preferences
            ORDER BY updated_at DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        if row is None:
            return {
                "target_roles": [],
                "locations": [],
                "work_modes": [],
                "experience_level": "",
                "minimum_salary": "",
                "industries": [],
                "keywords": [],
                "excluded_keywords": [],
                "minimum_match_score": 70,
            }
        return {
            "target_roles": json.loads(row["target_roles"] or "[]"),
            "locations": json.loads(row["locations"] or "[]"),
            "work_modes": json.loads(row["work_modes"] or "[]"),
            "experience_level": row["experience_level"] or "",
            "minimum_salary": row["minimum_salary"] or "",
            "industries": json.loads(row["industries"] or "[]"),
            "keywords": json.loads(row["keywords"] or "[]"),
            "excluded_keywords": json.loads(row["excluded_keywords"] or "[]"),
            "minimum_match_score": row["minimum_match_score"],
        }
    finally:
        connection.close()


# Jobs

def save_job(job):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO jobs (
                external_id, title, company, location, description,
                job_url, source, salary, posted_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            job["external_id"],
            job["title"],
            job.get("company", ""),
            job.get("location", ""),
            job.get("description", ""),
            job.get("job_url", ""),
            job.get("source", ""),
            job.get("salary"),
            job.get("posted_date"),
        ))
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        connection.close()


def get_jobs():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM jobs ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]
    finally:
        connection.close()


def get_job(job_id):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        connection.close()


def update_job_match(job_id, score, reason):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE jobs
            SET match_score = ?, match_reason = ?, status = 'MATCHED'
            WHERE id = ?
        """, (score, reason, job_id))
        connection.commit()
    finally:
        connection.close()


# Applications

APPLICATION_STATUSES = (
    "READY_TO_APPLY",
    "APPLIED",
    "SCREENING",
    "ASSESSMENT",
    "INTERVIEW",
    "OFFER",
    "REJECTED",
    "WITHDRAWN",
)


def create_application(
    job_id,
    resume_version="",
    cover_letter="",
    application_answers="",
):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO applications (
                job_id, status, resume_version, cover_letter,
                application_answers
            )
            VALUES (?, 'READY_TO_APPLY', ?, ?, ?)
        """, (job_id, resume_version, cover_letter, application_answers))
        connection.commit()
        return cursor.lastrowid
    finally:
        connection.close()


def get_applications(status=None):
    """Return applications with associated job details."""
    connection = get_connection()
    try:
        cursor = connection.cursor()
        query = """
            SELECT
                applications.*,
                jobs.title,
                jobs.company,
                jobs.location,
                jobs.job_url,
                jobs.match_score
            FROM applications
            JOIN jobs ON applications.job_id = jobs.id
        """
        params = []

        if isinstance(status, str):
            query += " WHERE applications.status = ?"
            params.append(status)
        elif status:
            statuses = list(status)
            if statuses:
                placeholders = ",".join("?" for _ in statuses)
                query += f" WHERE applications.status IN ({placeholders})"
                params.extend(statuses)

        query += " ORDER BY applications.updated_at DESC"
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    finally:
        connection.close()


def update_application_status(application_id, status):
    """Update application status and its applied_at timestamp."""
    if status not in APPLICATION_STATUSES:
        raise ValueError(f"Unsupported application status: {status}")

    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE applications
            SET
                status = ?,
                applied_at = CASE
                    WHEN ? = 'APPLIED' AND applied_at IS NULL
                        THEN CURRENT_TIMESTAMP
                    WHEN ? = 'READY_TO_APPLY'
                        THEN NULL
                    ELSE applied_at
                END,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (status, status, status, application_id))
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


# Agent activity

def log_agent_activity(agent, action, status, details=""):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO agent_activity (agent, action, status, details)
            VALUES (?, ?, ?, ?)
        """, (agent, action, status, details))
        connection.commit()
    finally:
        connection.close()


def get_agent_activity(limit=50):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT *
            FROM agent_activity
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))
        return [dict(row) for row in cursor.fetchall()]
    finally:
        connection.close()
