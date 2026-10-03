import os
import json

from dotenv import load_dotenv
from groq import Groq


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# GROQ CONFIGURATION
# ============================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b"
)


if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not configured in the .env file."
    )


# ============================================================
# GROQ CLIENT
# ============================================================

client = Groq(
    api_key=GROQ_API_KEY
)


# ============================================================
# JSON CLEANING
# ============================================================

def clean_json_response(text):
    """
    Convert an AI response into a Python object.

    Handles:
    - Plain JSON
    - ```json fenced JSON
    - ``` fenced JSON
    - JSON embedded in additional text
    """

    if not text:
        raise ValueError(
            "Groq returned an empty response."
        )

    text = text.strip()

    # --------------------------------------------------------
    # Remove markdown code fences
    # --------------------------------------------------------

    if text.startswith("```"):
        lines = text.splitlines()

        if lines:
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        text = "\n".join(lines).strip()

    # --------------------------------------------------------
    # Try direct JSON
    # --------------------------------------------------------

    try:
        return json.loads(text)

    except json.JSONDecodeError:
        pass

    # --------------------------------------------------------
    # Try extracting JSON object
    # --------------------------------------------------------

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1 and end > start:

        json_text = text[start:end + 1]

        try:
            return json.loads(json_text)

        except json.JSONDecodeError:
            pass

    # --------------------------------------------------------
    # Try extracting JSON array
    # --------------------------------------------------------

    start = text.find("[")
    end = text.rfind("]")

    if start != -1 and end != -1 and end > start:

        json_text = text[start:end + 1]

        try:
            return json.loads(json_text)

        except json.JSONDecodeError:
            pass

    raise ValueError(
        "Groq returned invalid JSON.\n\n"
        f"Response:\n{text}"
    )


# ============================================================
# GROQ TEXT GENERATION
# ============================================================

def generate_text(
    prompt,
    system_message=None,
    temperature=0.2,
    max_tokens=4096
):
    """
    Central Groq request function used by CareerFlow.

    GPT-OSS reasoning is disabled because CareerFlow
    needs the final answer/content directly.
    """

    messages = []

    if system_message:
        messages.append({
            "role": "system",
            "content": system_message
        })

    messages.append({
        "role": "user",
        "content": prompt
    })

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=temperature,
        max_completion_tokens=max_tokens,
        include_reasoning=False
    )

    if not response.choices:
        raise ValueError(
            "Groq returned no choices."
        )

    message = response.choices[0].message

    content = message.content

    if not content:
        raise ValueError(
            "Groq returned empty content."
        )

    return content


# ============================================================
# STRUCTURED JSON REQUEST
# ============================================================

def generate_json(
    prompt,
    system_message=None,
    temperature=0.2,
    max_tokens=4096
):
    """
    Generate structured JSON from Groq.
    """

    response = generate_text(
        prompt=prompt,
        system_message=system_message,
        temperature=temperature,
        max_tokens=max_tokens
    )

    return clean_json_response(
        response
    )


# ============================================================
# RESUME ANALYSIS
# ============================================================

def analyze_resume(resume_text):

    if not resume_text:
        raise ValueError(
            "Resume text is required."
        )

    prompt = f"""
Analyze the candidate resume below.

RESUME:
{resume_text}

Return ONLY valid JSON:

{{
    "name": "Candidate name",
    "summary": "Professional summary",
    "current_role": "Current or most recent role",
    "experience_years": 0,
    "skills": [
        "Skill 1",
        "Skill 2"
    ],
    "target_roles": [
        "Target role 1",
        "Target role 2"
    ],
    "strengths": [
        "Strength 1",
        "Strength 2"
    ],
    "gaps": [
        "Potential skill gap 1"
    ],
    "keywords": [
        "Keyword 1",
        "Keyword 2"
    ],
    "resume_score": 0
}}

Rules:

- Do not invent information.
- Extract only information supported by the resume.
- Estimate experience conservatively.
- Identify realistic target roles.
- Identify meaningful strengths.
- Identify realistic gaps.
- Score the resume from 0 to 100.
- Return ONLY JSON.
"""

    return generate_json(
        prompt=prompt,
        system_message=(
            "You are CareerFlow's Resume Intelligence Agent."
        ),
        temperature=0.1,
        max_tokens=3000
    )


# ============================================================
# JOB MATCHING
# ============================================================

def match_job_to_resume(
    candidate_profile,
    job
):

    if not candidate_profile:
        raise ValueError(
            "Candidate profile is required."
        )

    if not job:
        raise ValueError(
            "Job information is required."
        )

    prompt = f"""
Evaluate how well the candidate matches this job.

CANDIDATE PROFILE:
{candidate_profile}

JOB:
{job}

Return ONLY valid JSON:

{{
    "match_score": 0,
    "reason": "Short explanation of the overall match.",
    "matching_skills": [
        "Matching skill 1",
        "Matching skill 2"
    ],
    "missing_skills": [
        "Missing skill 1",
        "Missing skill 2"
    ],
    "experience_alignment": "Short explanation",
    "role_alignment": "Short explanation",
    "recommendation": "Short factual recommendation"
}}

Rules:

- match_score must be between 0 and 100.
- Compare skills.
- Compare experience.
- Compare target role alignment.
- Identify missing skills.
- Do not invent candidate experience.
- Return ONLY JSON.
"""

    return generate_json(
        prompt=prompt,
        system_message=(
            "You are CareerFlow's Matching Agent."
        ),
        temperature=0.1,
        max_tokens=2500
    )


# ============================================================
# APPLICATION PACKAGE
# ============================================================

def generate_application_package(
    candidate_profile,
    job
):

    if not candidate_profile:
        raise ValueError(
            "Candidate profile is required."
        )

    if not job:
        raise ValueError(
            "Job information is required."
        )

    prompt = f"""
Create a highly tailored application package.

CANDIDATE PROFILE:
{candidate_profile}

JOB:
{job}

Return ONLY valid JSON:

{{
    "application_strategy": "Short explanation of how the candidate should approach this role.",
    "resume_headline": "Tailored professional headline",
    "professional_summary": "Tailored professional summary",
    "cover_letter": "Professional cover letter",
    "key_talking_points": [
        "Talking point 1",
        "Talking point 2",
        "Talking point 3"
    ],
    "matching_skills": [
        "Skill 1",
        "Skill 2"
    ],
    "skills_to_emphasize": [
        "Skill 1",
        "Skill 2"
    ],
    "potential_gaps": [
        "Gap 1"
    ],
    "interview_focus": [
        "Interview topic 1",
        "Interview topic 2"
    ]
}}

Rules:

- Do not invent qualifications.
- Do not claim experience that is not present.
- Use only information supported by the candidate profile.
- Make content specific to the job.
- Keep the cover letter professional and concise.
- Return ONLY JSON.
"""

    return generate_json(
        prompt=prompt,
        system_message=(
            "You are CareerFlow's Application Agent."
        ),
        temperature=0.3,
        max_tokens=4500
    )


# ============================================================
# INTERVIEW PREPARATION
# ============================================================

def generate_interview_plan(
    candidate_profile,
    job,
    application_package=None
):

    if not candidate_profile:
        raise ValueError(
            "Candidate profile is required."
        )

    if not job:
        raise ValueError(
            "Job information is required."
        )

    application_package = (
        application_package or {}
    )

    prompt = f"""
Prepare a personalized interview preparation plan.

CANDIDATE PROFILE:
{candidate_profile}

TARGET JOB:
{job}

APPLICATION PACKAGE:
{application_package}

Return ONLY valid JSON:

{{
    "readiness_summary": "Short summary of interview readiness.",
    "readiness_score": 0,

    "technical_questions": [
        {{
            "question": "Technical interview question",
            "why_asked": "Why an interviewer may ask this",
            "answer_guidance": "What a strong answer should cover"
        }}
    ],

    "behavioral_questions": [
        {{
            "question": "Behavioral interview question",
            "answer_guidance": "How the candidate should structure the answer"
        }}
    ],

    "candidate_specific_questions": [
        {{
            "question": "Question specifically relevant to this candidate",
            "answer_guidance": "Answer guidance"
        }}
    ],

    "star_stories": [
        {{
            "topic": "Story topic",
            "situation": "Situation",
            "task": "Task",
            "action": "Action",
            "result": "Result"
        }}
    ],

    "preparation_gaps": [
        "Preparation gap"
    ],

    "interview_focus": [
        "Priority preparation topic"
    ]
}}

Rules:

- Do not invent candidate experience.
- Use only information supported by the profile.
- Tailor questions to the target job.
- Include technical questions.
- Include behavioral questions.
- Include candidate-specific questions.
- Create practical STAR frameworks.
- Identify preparation gaps honestly.
- Generate approximately 5 technical questions.
- Generate approximately 5 behavioral questions.
- Generate approximately 3 candidate-specific questions.
- Generate approximately 3 STAR stories.
- Return ONLY JSON.
"""

    return generate_json(
        prompt=prompt,
        system_message=(
            "You are CareerFlow's Interview Agent."
        ),
        temperature=0.2,
        max_tokens=5000
    )


# ============================================================
# LEARNING PLAN
# ============================================================

def generate_learning_plan(
    candidate_profile,
    job,
    match_result=None,
    interview_plan=None
):

    if not candidate_profile:
        raise ValueError(
            "Candidate profile is required."
        )

    if not job:
        raise ValueError(
            "Job information is required."
        )

    match_result = (
        match_result or {}
    )

    interview_plan = (
        interview_plan or {}
    )

    prompt = f"""
Create a personalized learning and improvement plan.

CANDIDATE PROFILE:
{candidate_profile}

TARGET JOB:
{job}

JOB MATCH ANALYSIS:
{match_result}

INTERVIEW PREPARATION:
{interview_plan}

Return ONLY valid JSON:

{{
    "learning_summary": "Main development priorities.",

    "priority_level": "HIGH",

    "overall_readiness": 0,

    "skill_gaps": [
        {{
            "skill": "Skill name",
            "importance": "HIGH",
            "reason": "Why this skill matters",
            "current_level": "Estimated current level based only on available evidence",
            "target_level": "Level needed for the role"
        }}
    ],

    "learning_roadmap": [
        {{
            "phase": "Phase 1",
            "title": "Learning phase title",
            "duration": "1-2 weeks",
            "objectives": [
                "Objective 1",
                "Objective 2"
            ],
            "practice_tasks": [
                "Practical task 1",
                "Practical task 2"
            ]
        }}
    ],

    "project_ideas": [
        "Practical project idea 1",
        "Practical project idea 2"
    ],

    "interview_practice": [
        "Practice topic 1",
        "Practice topic 2"
    ],

    "recommended_next_actions": [
        "Action 1",
        "Action 2",
        "Action 3"
    ]
}}

Rules:

- Do not invent candidate experience.
- Identify realistic skill gaps.
- Prioritize skills important for the target role.
- Focus on practical learning.
- Include hands-on projects.
- Connect learning to interview preparation.
- Make the roadmap achievable.
- Avoid generic unrelated learning.
- Return ONLY JSON.
"""

    return generate_json(
        prompt=prompt,
        system_message=(
            "You are CareerFlow's Learning Agent."
        ),
        temperature=0.2,
        max_tokens=5000
    )