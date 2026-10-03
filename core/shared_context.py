from datetime import datetime


class MissionContext:

    def __init__(self, user_goal=""):

        self.mission_id = datetime.now().strftime("%Y%m%d%H%M%S")

        self.user_goal = user_goal

        # Candidate information
        self.candidate_profile = None
        self.resume_text = ""
        self.resume_filename = ""
        self.preferences = {}

        # Agent outputs
        self.discovered_jobs = []
        self.matched_jobs = []

        self.application_packages = []

        self.interview_plan = {}
        self.learning_plan = {}

        self.career_intelligence = {}

        # Execution tracking
        self.agent_results = []
        self.errors = []

        self.started_at = datetime.now()
        self.completed_at = None

    def add_agent_result(self, agent_name, result):

        self.agent_results.append({
            "agent": agent_name,
            "success": result.success,
            "message": result.message,
            "data": result.data,
            "timestamp": datetime.now().isoformat()
        })

    def add_error(self, agent_name, error):

        self.errors.append({
            "agent": agent_name,
            "error": str(error),
            "timestamp": datetime.now().isoformat()
        })

    def complete(self):

        self.completed_at = datetime.now()

    def summary(self):

        return {
            "mission_id": self.mission_id,
            "user_goal": self.user_goal,

            "discovered_jobs": len(self.discovered_jobs),

            "matched_jobs": len(self.matched_jobs),

            "applications": len(self.application_packages),

            "agents_executed": len(self.agent_results),

            "errors": len(self.errors),

            "started_at": self.started_at.isoformat(),

            "completed_at": (
                self.completed_at.isoformat()
                if self.completed_at
                else None
            )
        }