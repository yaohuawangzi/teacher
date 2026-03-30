import yaml
from pathlib import Path
import os.path
class AgentConfig:
    def __init__(self, config):
        self.id = config['id']
        self.name = config['name']
        self.description = config['description']
        self.markDown = config['markdown']
        self.baseDir = config['baseDir']



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
        for config_file in self.config_path.glob("**/*.md"):
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # 分割 YAML 头和 Markdown 正文
                if "---" not in content:
                    continue
                parts = content.split("---", 2)
                if len(parts) < 3:
                    continue

                yaml_content = parts[1].strip()
                try:
                    agent_meta = yaml.safe_load(yaml_content)
                except Exception as e:
                    print(f"解析 {config_file} 失败: {e}")
                    continue
                # 校验必填字段
                required_fields = ["name", "id", "description"]
                if not all(f in agent_meta for f in required_fields):
                    print(f"{agent_meta} 缺少必填字段")
                    continue

                agent_id = agent_meta["id"]
                agent_meta["markdown"] = parts[2].strip()
                agent_meta["baseDir"] = os.path.dirname(config_file)
                self.agents[agent_id] = self._create_agent_from_config(agent_meta)
                print(f"✅ 注册agent: {agent_id} - {agent_meta['name']}")


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

