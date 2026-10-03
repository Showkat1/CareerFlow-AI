
import math

from core.agent_base import BaseAgent, AgentResult
from database.db import get_jobs, update_job_match, log_agent_activity
from services.ai_service import match_job_to_resume


class MatchingAgent(BaseAgent):
    name = "Matching Agent"

    description = (
        "Evaluates candidate-job compatibility using "
        "skills, experience, role alignment and career goals."
    )

    def __init__(self):
        super().__init__()
        self.last_stats = {}

    @staticmethod
    def _valid_jobs(jobs):
        """Keep only dictionary job records."""
        if not isinstance(jobs, list):
            return []

        return [
            job for job in jobs
            if isinstance(job, dict)
        ]

    @staticmethod
    def _job_id(job):
        """Return a usable database job ID, if present."""
        job_id = job.get("id")
        return job_id if job_id is not None else None

    def match_all(self, candidate_profile, jobs=None):
        """
        Evaluate the supplied mission jobs.

        If no job list is supplied, fall back to database jobs.
        """
        if jobs is None:
            jobs = get_jobs()

        jobs = self._valid_jobs(jobs)
        results = []

        successful = 0
        failed = 0

        for job in jobs:
            try:
                result = match_job_to_resume(
                    candidate_profile,
                    job,
                )

                if not isinstance(result, dict):
                    raise ValueError(
                        "AI matching response must be a dictionary."
                    )

                raw_score = result.get("match_score")

                if isinstance(raw_score, bool):
                    raise ValueError("Invalid match score.")

                score = float(raw_score)

                if not math.isfinite(score):
                    raise ValueError("Match score is not finite.")

                score = max(0.0, min(100.0, score))

                reason = result.get("reason", "")
                if not isinstance(reason, str):
                    reason = str(reason)

                # Persist only when this job has a database ID.
                job_id = self._job_id(job)

                if job_id is not None:
                    update_job_match(
                        job_id,
                        score,
                        reason,
                    )

                results.append({
                    "job": job,
                    "score": score,
                    "result": result,
                    "evaluation_status": "SUCCESS",
                })

                successful += 1

            except Exception as exc:
                results.append({
                    "job": job,
                    "score": 0,
                    "result": {
                        "reason": (
                            "Evaluation failed. "
                            "This is not a genuine zero match."
                        ),
                        "matching_skills": [],
                        "missing_skills": [],
                    },
                    "evaluation_status": "FAILED",
                    "error": str(exc),
                })

                failed += 1

        self.last_stats = {
            "total_analyzed": len(jobs),
            "successful_evaluations": successful,
            "failed_evaluations": failed,
        }

        return results

    def execute(self, context):
        self.set_status("RUNNING")

        try:
            if not context.candidate_profile:
                raise ValueError(
                    "Candidate profile is required before matching jobs."
                )

            # Prefer this mission's discovered opportunities.
            discovered = getattr(
                context,
                "discovered_jobs",
                None,
            )

            if discovered is not None:
                jobs = self._valid_jobs(discovered)
            else:
                jobs = None

            results = self.match_all(
                context.candidate_profile,
                jobs=jobs,
            )

            context.matched_jobs = sorted(
                results,
                key=lambda item: (
                    item.get("evaluation_status") == "SUCCESS",
                    item.get("score", 0),
                ),
                reverse=True,
            )

            successful_results = [
                item for item in results
                if item.get("evaluation_status") == "SUCCESS"
            ]

            strong_matches = [
                item for item in successful_results
                if item.get("score", 0) >= 70
            ]

            good_matches = [
                item for item in successful_results
                if item.get("score", 0) >= 60
            ]

            total = len(results)
            successful = len(successful_results)
            failed = total - successful

            average_score = (
                sum(item.get("score", 0) for item in successful_results)
                / successful
                if successful
                else 0
            )

            stats = {
                "total_analyzed": total,
                "successful_evaluations": successful,
                "failed_evaluations": failed,
                "strong_matches": len(strong_matches),
                "good_matches": len(good_matches),
                "average_score": round(average_score, 1),
            }

            if total == 0:
                message = "No jobs available for matching."
                status = "SUCCESS"
            elif successful == 0:
                message = (
                    "No jobs could be evaluated. "
                    "Check the AI service and retry."
                )
                status = "FAILED"
            else:
                message = (
                    f"Evaluated {successful} of {total} jobs. "
                    f"Identified {len(strong_matches)} strong matches."
                )
                status = "SUCCESS"

            log_agent_activity(
                self.name,
                "Job matching",
                status,
                (
                    f"Analyzed: {total}; "
                    f"Successful: {successful}; "
                    f"Failed: {failed}; "
                    f"Strong matches: {len(strong_matches)}; "
                    f"Average score: {average_score:.1f}."
                ),
            )

            if status == "FAILED":
                self.set_status("FAILED")
            else:
                self.set_status("COMPLETED")

            return AgentResult(
                success=(status == "SUCCESS"),
                message=message,
                data=stats,
            )

        except Exception as exc:
            self.set_status("FAILED")

            log_agent_activity(
                self.name,
                "Job matching",
                "FAILED",
                str(exc),
            )

            return AgentResult(
                success=False,
                message=str(exc),
            )