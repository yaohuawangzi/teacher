from core.ability_registration.agent_manager import AgentManager
from core.ability_registration.skill_manager import SkillManager
from core.ability_registration.tool_manage import ToolManage



class AgentRegister:
    # 类变量：存储唯一实例
    _instance = None
    # 标记：是否已初始化（避免重复加载配置）
    _initialized = False

    # 核心：重写 __new__ 方法，控制实例创建
    def __new__(cls):
        # 如果实例不存在，创建新实例
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        # 始终返回同一个实例
        return cls._instance


    def __init__(self):
        # 防止重复初始化（__init__ 会在每次实例化时调用）
        if AgentRegister._initialized:
            return
        agent_manager = AgentManager()
        skill_manager = SkillManager()
        tool_manager = ToolManage()
        agent_map = agent_manager.get_agent_map()
        skill_map = skill_manager.get_skill_map()
        tool_map = tool_manager.get_tool_map()
        # agent_skill_map = {}
        # for agent_id, agent_config in agent_map.items():
        #     agent_skill_map[agent_id] = []
        #     if agent_config.skills is not None:
        #         for skill_id in agent_config.skills:
        #             if skill_id in skill_map:
        #                 agent_skill_map[agent_id].append(skill_id)
        self.agent_map = agent_map
        self.skill_map = skill_map
        self.tool_map = tool_map
        # self.agent_skill_map = agent_skill_map