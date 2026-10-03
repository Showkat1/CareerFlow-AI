from core.agent_base import BaseAgent, AgentResult
from database.db import log_agent_activity
from services.ai_service import generate_application_package


class ApplicationAgent(BaseAgent):
    name = "Application Agent"
    description = "Creates tailored application packages for high-fit opportunities."

    def __init__(self):
        super().__init__()

    def select_opportunities(self, matched_jobs, minimum_score=70, limit=3):
        """
        Select the highest-quality opportunities for application generation.
        """

        selected = [
            item
            for item in matched_jobs
            if item.get("score", 0) >= minimum_score
        ]

        selected.sort(
            key=lambda item: item.get("score", 0),
            reverse=True
        )

        return selected[:limit]

    def execute(self, context):
        self.set_status("RUNNING")

        try:
            if not context.candidate_profile:
                raise ValueError("Candidate profile is required.")

            if not context.matched_jobs:
                raise ValueError("Matched jobs are required before application generation.")

            opportunities = self.select_opportunities(
                context.matched_jobs,
                minimum_score=70,
                limit=3
            )

            packages = []

            for item in opportunities:

                job = item.get("job", {})
                score = item.get("score", 0)
                match_result = item.get("result", {})

                application = generate_application_package(
                    context.candidate_profile,
                    job
                )

                package = {
                    "job": job,
                    "match_score": score,
                    "match_result": match_result,
                    "application": application
                }

                packages.append(package)

            context.application_packages = packages

            log_agent_activity(
                self.name,
                "Application generation",
                "SUCCESS",
                f"Generated {len(packages)} tailored application packages."
            )

            self.set_status("COMPLETED")

            return AgentResult(
                success=True,
                message=f"Generated {len(packages)} tailored application packages.",
                data={
                    "applications_generated": len(packages),
                    "minimum_match_score": 70
                }
            )

        except Exception as exc:
            self.set_status("FAILED")

            log_agent_activity(
                self.name,
                "Application generation",
                "FAILED",
                str(exc)
            )

            return AgentResult(
                success=False,
                message=str(exc)
            )