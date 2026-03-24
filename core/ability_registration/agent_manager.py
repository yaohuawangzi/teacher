import yaml
from pathlib import Path

class AgentConfig:
    def __init__(self, config):
        self.id = config['id']
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
        if 'request_schema' in config:
            self.request_schema = config['request_schema']
        if 'skills' in config:
            self.skills = config['skills']

class AgentManager:
    def __init__(self):
        self.agents = {}
        # 关键修复：基于当前文件的绝对路径拼接agents目录
        # 1. 获取当前文件（agent_manager.py）的绝对路径
        current_file_path = Path(__file__).absolute()
        # 2. 获取当前文件所在目录（core/）
        current_dir = current_file_path.parent
        # 3. 拼接上级目录的agents（core/../agents → project/agents）
        self.config_path = current_dir / "../../agents"
        # 4. 转换为绝对路径（消除../，避免路径歧义）
        self.config_path = self.config_path.resolve()
        self.load_agents()

    def load_agents(self):
        for config_file in self.config_path.glob("**/*.yaml"):
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                agent_id = config['id']
                # 此处可以根据 config['type'] 实例化不同的 Agent 类
                self.agents[agent_id] = self._create_agent_from_config(config)
                print(f"✅ 注册agent: {agent_id} - {config['name']}")

    def _create_agent_from_config(self, config):
        # 伪代码：实际会更复杂，包括加载 Skill, Tool, Knowledge Base 等
        agent_class = AgentConfig(config)
        return agent_class

    def get_agent(self, id):
        return self.agents.get(id)

    def get_agent_map(self):
        return self.agents

if __name__ == "__main__":
    agent_manager = AgentManager()
    assistant_agent = agent_manager.get_agent("academic_tutor")

