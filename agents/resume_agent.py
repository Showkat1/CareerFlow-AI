from core.agent_base import BaseAgent, AgentResult
from database.db import log_agent_activity


class ResumeIntelligenceAgent(BaseAgent):
    name = "Resume Intelligence Agent"
    description = "Understands the candidate profile, strengths, gaps, and career direction."

    def __init__(self):
        super().__init__()

    def execute(self, context):
        self.set_status("RUNNING")

        try:
            if not context.candidate_profile:
                raise ValueError("Candidate profile is required.")

            profile = context.candidate_profile

            # Normalize common profile fields so downstream agents
            # have a consistent structure.
            normalized_profile = {
                "name": profile.get("name", ""),
                "summary": profile.get("summary", ""),
                "current_role": profile.get("current_role", ""),
                "experience_years": profile.get("experience_years", 0),
                "skills": profile.get("skills", []),
                "target_roles": profile.get("target_roles", []),
                "strengths": profile.get("strengths", []),
                "gaps": profile.get("gaps", []),
                "keywords": profile.get("keywords", []),
                "resume_score": profile.get("resume_score", 0),
            }

            # Preserve the original profile while adding intelligence.
            context.candidate_profile = normalized_profile

            intelligence = {
                "career_identity": normalized_profile.get("current_role", ""),
                "target_roles": normalized_profile.get("target_roles", []),
                "core_skills": normalized_profile.get("skills", []),
                "strengths": normalized_profile.get("strengths", []),
                "skill_gaps": normalized_profile.get("gaps", []),
                "resume_score": normalized_profile.get("resume_score", 0),
            }

            context.career_intelligence["resume"] = intelligence

            log_agent_activity(
                self.name,
                "Resume intelligence",
                "SUCCESS",
                "Candidate profile analyzed and normalized."
            )

            self.set_status("COMPLETED")

            return AgentResult(
                success=True,
                message="Resume intelligence profile prepared.",
                data=intelligence
            )

        except Exception as exc:
            self.set_status("FAILED")

            log_agent_activity(
                self.name,
                "Resume intelligence",
                "FAILED",
                str(exc)
            )

            return AgentResult(
                success=False,
                message=str(exc)
            )