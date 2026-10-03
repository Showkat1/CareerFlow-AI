from core.orchestrator import CareerOrchestrator


class CareerMission:

    def __init__(self):
        self.orchestrator = CareerOrchestrator()

    def start(self, goal):
        return self.orchestrator.run_mission(goal)