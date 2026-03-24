import yaml
from pathlib import Path

class ToolConfig:
    def __init__(self, config):
        self.id = config['id']
        self.name = config['name']
        self.description = config['description']
        if 'parameters' in config:
            self.parameters = config['parameters']

class ToolManage:
    def __init__(self):
        self.tools = {}
        # 关键修复：基于当前文件的绝对路径拼接agents目录
        # 1. 获取当前文件（agent_manager.py）的绝对路径
        current_file_path = Path(__file__).absolute()
        # 2. 获取当前文件所在目录（core/）
        current_dir = current_file_path.parent
        # 3. 拼接上级目录的agents（core/../agents → project/agents）
        self.config_path = current_dir / "../../tools"
        # 4. 转换为绝对路径（消除../，避免路径歧义）
        self.config_path = self.config_path.resolve()
        self.load_tools()
    def load_tools(self):
        for skill_md in self.config_path.glob("tools.md"):
            with open(skill_md, 'r', encoding='utf-8') as f:
                content = f.read()
                # 分割 YAML 头和 Markdown 正文
                if "---" not in content:
                    continue
                parts = content.split("---", 2)
                if len(parts) < 3:
                    continue

                yaml_content = parts[1].strip()
                try:
                    tool_metas = yaml.safe_load(yaml_content)
                except Exception as e:
                    print(f"解析 {skill_md} 失败: {e}")
                    continue

                # 校验必填字段
                required_fields = ["name", "id", "description", "parameters"]
                for tool_meta in tool_metas:
                    if not all(f in tool_meta for f in required_fields):
                        print(f"{skill_md} 缺少必填字段")
                        continue

                    tool_id = tool_meta["id"]
                    self.tools[tool_id] = tool_meta
                    print(f"✅ 注册tool: {tool_id} - {tool_meta['name']}")

    def _create_tool_from_config(self, config):
        # 伪代码：实际会更复杂，包括加载 Skill, Tool, Knowledge Base 等
        tool_class = ToolConfig(config)
        return tool_class

    def get_tool(self, id):
        return self.tools.get(id)

    def get_tool_map(self):
        return self.tools


if __name__ == "__main__":
    skill_manager = ToolManage()
    assistant_agent = skill_manager.get_tool("智能助教")