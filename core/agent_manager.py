import yaml
from pathlib import Path

class AgentConfig:
    def __init__(self, config):
        self.name = config['name']
        if 'enabled' in config:
            self.enabled = config['enabled']
        else:
            self.enabled = True
        self.description = config['description']
        self.personality = config['personality']
        if 'core_competency' in config:
            self.core_competency = config['core_competency']
        if 'constraints' in config:
            self.constraints = config['constraints']
        if 'response_schema' in config:
            self.response_schema = config['response_schema']
        if 'skills' in config:
            self.skills = config['skills']

class AgentManager:
    def __init__(self):
        self.agents = {}
        self.config_path = Path("../agents")
        self.load_agents()

    def load_agents(self):
        for config_file in self.config_path.glob("**/*.yaml"):
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                agent_name = config['name']
                # 此处可以根据 config['type'] 实例化不同的 Agent 类
                self.agents[agent_name] = self._create_agent_from_config(config)
                print(f"Agent '{agent_name}' loaded.")

    def _create_agent_from_config(self, config):
        # 伪代码：实际会更复杂，包括加载 Skill, Tool, Knowledge Base 等
        agent_class = AgentConfig(config)
        return agent_class

    def get_agent(self, name):
        return self.agents.get(name)

if __name__ == "__main__":
    agent_manager = AgentManager()
    assistant_agent = agent_manager.get_agent("academic_tutor")

