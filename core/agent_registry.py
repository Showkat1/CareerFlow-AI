class AgentRegistry:

    def __init__(self):
        self._agents = {}

    def register(self, agent):
        self._agents[agent.name] = agent

    def get(self, agent_name):
        return self._agents.get(agent_name)

    def all(self):
        return list(self._agents.values())

    def names(self):
        return list(self._agents.keys())