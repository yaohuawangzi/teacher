import yaml
from pathlib import Path

class SkillConfig:
    def __init__(self, config):
        self.name = config['name']
        self.description = config['description']
        self.skills = config['skills']

class SkillManager:
    def __init__(self):
        self.skills = {}
        self.config_path = Path("../skills")
        self.load_agents()

    def load_agents(self):
        for config_file in self.config_path.glob("**/*.yaml"):
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                name = config['name']
                # 此处可以根据 config['type'] 实例化不同的 Agent 类
                self.skills[name] = self._create_skill_from_config(config)
                print(f"Agent '{name}' loaded.")

    def _create_skill_from_config(self, config):
        # 伪代码：实际会更复杂，包括加载 Skill, Tool, Knowledge Base 等
        agent_class = SkillConfig(config)
        return agent_class

    def get_skill(self, id):
        return self.agents.get(id)

if __name__ == "__main__":
    skill_manager = SkillManager()
    assistant_agent = skill_manager.get_skill("智能助教")

