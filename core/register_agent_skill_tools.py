class AgentRegister:
    def __init__(self):
        self.agents = {}

    def register_agent(self):
        self.agents[agent_id] = agent_class

    def get_agent(self, agent_id):
        return self.agents.get(agent_id)