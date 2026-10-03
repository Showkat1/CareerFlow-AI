from abc import ABC, abstractmethod


class AgentResult:

    def __init__(self, success=True, message="", data=None):
        self.success = success
        self.message = message
        self.data = data or {}

    def to_dict(self):
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data
        }


class BaseAgent(ABC):

    name = "Base Agent"
    description = "Generic CareerFlow agent"

    def __init__(self):
        self.status = "IDLE"

    def set_status(self, status):
        self.status = status

    @abstractmethod
    def execute(self, context):
        raise NotImplementedError