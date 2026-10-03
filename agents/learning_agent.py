from core.agent_base import BaseAgent, AgentResult

from database.db import log_agent_activity

from services.ai_service import generate_learning_plan


class LearningAgent(BaseAgent):

    name = "Learning Agent"

    description = (
        "Identifies career skill gaps and creates "
        "personalized learning and improvement plans."
    )

    def __init__(self):
        super().__init__()

    def select_target(self, context):

        if not context.matched_jobs:
            return None

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
                    "for learning analysis."
                )

            job = target.get(
                "job",
                {}
            )

            match_result = target.get(
                "result",
                {}
            )

            interview_data = (
                context.interview_plan or {}
            )

            interview_plan = interview_data.get(
                "plan",
                {}
            )

            learning_plan = generate_learning_plan(

                candidate_profile=(
                    context.candidate_profile
                ),

                job=job,

                match_result=match_result,

                interview_plan=interview_plan
            )

            context.learning_plan = {

                "job": job,

                "match_score": target.get(
                    "score",
                    0
                ),

                "plan": learning_plan

            }

            log_agent_activity(

                self.name,

                "Learning plan generation",

                "SUCCESS",

                (
                    "Generated personalized learning "
                    f"plan for {job.get('title', 'target opportunity')}."
                )

            )

            self.set_status("COMPLETED")

            return AgentResult(

                success=True,

                message=(
                    "Personalized learning and "
                    "career improvement plan generated."
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

                "Learning plan generation",

                "FAILED",

                str(exc)

            )

            return AgentResult(

                success=False,

                message=str(exc)

            )