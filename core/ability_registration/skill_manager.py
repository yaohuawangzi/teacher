import yaml
from pathlib import Path

class SkillConfig:
    def __init__(self, config):
        self.id = config['id']
        self.name = config['name']
        self.description = config['description']
        if 'parameters' in config:
            self.parameters = config['parameters']


class SkillManager:
    def __init__(self):
        self.skills = {}
        # 关键修复：基于当前文件的绝对路径拼接agents目录
        # 1. 获取当前文件（agent_manager.py）的绝对路径
        current_file_path = Path(__file__).absolute()
        # 2. 获取当前文件所在目录（core/）
        current_dir = current_file_path.parent
        # 3. 拼接上级目录的agents（core/../agents → project/agents）
        self.config_path = current_dir / "../../skills"
        # 4. 转换为绝对路径（消除../，避免路径歧义）
        self.config_path = self.config_path.resolve()
        self.load_skills()

    def load_skills(self):
        for skill_md in self.config_path.glob("**/skill.md"):
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
                    skill_meta = yaml.safe_load(yaml_content)
                except Exception as e:
                    print(f"解析 {skill_md} 失败: {e}")
                    continue

                # 校验必填字段
                required_fields = ["name", "id", "description", "parameters"]
                if not all(f in skill_meta for f in required_fields):
                    print(f"{skill_md} 缺少必填字段")
                    continue

                skill_id = skill_meta["id"]
                self.skills[skill_id] = {
                    "meta": skill_meta,
                    "markdown": parts[2].strip(),
                    "folder": skill_md
                }
                print(f"✅ 注册技能: {skill_id} - {skill_meta['name']}")

    def _create_skill_from_config(self, config):
        # 伪代码：实际会更复杂，包括加载 Skill, Tool, Knowledge Base 等
        agent_class = SkillConfig(config)
        return agent_class

    def get_skill(self, id):
        return self.skills.get(id)

    def get_skill_map(self):
        return self.skills

if __name__ == "__main__":
    skill_manager = SkillManager()
    assistant_agent = skill_manager.get_skill("智能助教")

