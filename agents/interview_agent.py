from core.agent_base import BaseAgent, AgentResult

from database.db import log_agent_activity

from services.ai_service import generate_interview_plan


class InterviewAgent(BaseAgent):

    name = "Interview Agent"

    description = (
        "Prepares personalized interview questions, "
        "answers and preparation plans."
    )

    def __init__(self):
        super().__init__()

    def select_target(self, context):

        if not context.matched_jobs:

            return None

        # Prefer the highest scoring opportunity.
        sorted_jobs = sorted(
            context.matched_jobs,
            key=lambda item: item.get(
                "score",
                0
            ),
            reverse=True
        )

        return sorted_jobs[0]

    def execute(self, context):

        self.set_status("RUNNING")

        try:

            if not context.candidate_profile:

                raise ValueError(
                    "Candidate profile is required."
                )

            target = self.select_target(
                context
            )

            if not target:

                raise ValueError(
                    "No matched opportunity is available "
                    "for interview preparation."
                )

            job = target.get(
                "job",
                {}
            )

            application_package = {}

            # Find the application package for
            # the selected opportunity.
            for package in context.application_packages:

                package_job = package.get(
                    "job",
                    {}
                )

                if (
                    package_job.get("id")
                    == job.get("id")
                ):

                    application_package = (
                        package.get(
                            "application",
                            {}
                        )
                    )

                    break

            interview_plan = generate_interview_plan(
                candidate_profile=context.candidate_profile,
                job=job,
                application_package=application_package
            )

            context.interview_plan = {
                "job": job,
                "match_score": target.get(
                    "score",
                    0
                ),
                "plan": interview_plan
            }

            log_agent_activity(
                self.name,
                "Interview preparation",
                "SUCCESS",
                (
                    "Generated interview preparation "
                    f"for {job.get('title', 'target opportunity')}."
                )
            )

            self.set_status("COMPLETED")

            return AgentResult(
                success=True,
                message=(
                    "Personalized interview preparation "
                    "plan generated."
                ),
                data={
                    "target_job": job.get(
                        "title",
                        "Opportunity"
                    ),
                    "match_score": target.get(
                        "score",
                        0
                    )
                }
            )

        except Exception as exc:

            self.set_status("FAILED")

            log_agent_activity(
                self.name,
                "Interview preparation",
                "FAILED",
                str(exc)
            )

            return AgentResult(
                success=False,
                message=str(exc)
            )