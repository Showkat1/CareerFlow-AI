from core.agent_registry import AgentRegistry
from core.shared_context import MissionContext

from agents.resume_agent import ResumeIntelligenceAgent
from agents.job_search_agent import JobSearchAgent
from agents.matching_agent import MatchingAgent
from agents.application_agent import ApplicationAgent
from agents.interview_agent import InterviewAgent
from agents.learning_agent import LearningAgent

from database.db import (
    get_candidate_profile,
    get_job_preferences,
    log_agent_activity
)


class CareerOrchestrator:

    def __init__(self):

        self.registry = AgentRegistry()

        self.register_agents()

    # ============================================================
    # AGENT REGISTRATION
    # ============================================================

    def register_agents(self):

        self.registry.register(
            ResumeIntelligenceAgent()
        )

        self.registry.register(
            JobSearchAgent()
        )

        self.registry.register(
            MatchingAgent()
        )

        self.registry.register(
            ApplicationAgent()
        )

        self.registry.register(
            InterviewAgent()
        )

        self.registry.register(
            LearningAgent()
        )

    # ============================================================
    # GET AGENT
    # ============================================================

    def get_agent(self, name):

        return self.registry.get(
            name
        )

    # ============================================================
    # EXECUTE AGENT
    # ============================================================

    def execute_agent(
        self,
        agent_name,
        context
    ):

        agent = self.get_agent(
            agent_name
        )

        if not agent:

            raise ValueError(
                f"Agent not registered: {agent_name}"
            )

        result = agent.execute(
            context
        )

        context.add_agent_result(
            agent.name,
            result
        )

        return result

    # ============================================================
    # RUN CAREER MISSION
    # ============================================================

    def run_mission(
        self,
        user_goal
    ):

        context = MissionContext(
            user_goal=user_goal
        )

        log_agent_activity(
            "Orchestrator",
            "Mission started",
            "RUNNING",
            user_goal
        )

        try:

            # ====================================================
            # LOAD CANDIDATE PROFILE
            # ====================================================

            saved_profile = get_candidate_profile()

            if not saved_profile:

                context.add_error(
                    "Orchestrator",
                    "No candidate profile found."
                )

                context.complete()

                return context

            context.candidate_profile = (
                saved_profile["profile"]
            )

            context.resume_text = (
                saved_profile["resume_text"]
            )

            context.resume_filename = (
                saved_profile["resume_filename"]
            )

            context.preferences = (
                get_job_preferences()
            )

            # ====================================================
            # AGENT 1
            # RESUME INTELLIGENCE
            # ====================================================

            result = self.execute_agent(
                "Resume Intelligence Agent",
                context
            )

            if not result.success:

                context.complete()

                return context

            # ====================================================
            # AGENT 2
            # JOB DISCOVERY
            # ====================================================

            result = self.execute_agent(
                "Job Discovery Agent",
                context
            )

            if not result.success:

                context.complete()

                return context

            # ====================================================
            # AGENT 3
            # MATCHING
            # ====================================================

            result = self.execute_agent(
                "Matching Agent",
                context
            )

            if not result.success:

                context.complete()

                return context

            # ====================================================
            # AGENT 4
            # APPLICATION
            # ====================================================

            result = self.execute_agent(
                "Application Agent",
                context
            )

            if not result.success:

                context.complete()

                return context

            # ====================================================
            # AGENT 5
            # INTERVIEW
            # ====================================================

            result = self.execute_agent(
                "Interview Agent",
                context
            )

            if not result.success:

                context.complete()

                return context

            # ====================================================
            # AGENT 6
            # LEARNING
            # ====================================================

            result = self.execute_agent(
                "Learning Agent",
                context
            )

            if not result.success:

                context.complete()

                return context

            # ====================================================
            # MISSION COMPLETED
            # ====================================================

            context.complete()

            log_agent_activity(
                "Orchestrator",
                "Mission completed",
                "SUCCESS",
                str(
                    context.summary()
                )
            )

            return context

        except Exception as exc:

            context.add_error(
                "Orchestrator",
                str(exc)
            )

            context.complete()

            log_agent_activity(
                "Orchestrator",
                "Mission failed",
                "FAILED",
                str(exc)
            )

            return context