from core.ability_registration.register_agent_skill_tools import AgentRegister
from model.context import MessageContext, UserInfo
from core.context.context_manager import ContextManager


from model.task import Task
class DispatcherSkill:
    def __init__(self):
        pass
    def dispatch(self, agent_id, sub_session_id: str, user_id, user_input: str):
        # 存储对话
        context_manager = ContextManager()
        user =  UserInfo(user_id=user_id)
        session_id = context_manager.get_session_id_by_session(sub_session_id)
        message_context = MessageContext(sub_session_id=sub_session_id, session_id = session_id,user=user)

        if context_manager.get_sub_session_context(sub_session_id) is not None:
            message_context = context_manager.get_sub_session_context(sub_session_id)

        message_context.add_message("user", user_input, None, None)
        context_manager.save_sub_session_context(message_context)

        # 组装执行
        agent_register = AgentRegister()



    def generate_prompt(self, agent_id, agent_register: AgentRegister, message_context: MessageContext):

        agent_info = agent_register.agent_map[agent_id]
        dispatch_prompt = f"你是一个{agent_info.description} \n 核心职能为 {agent_info.core_competency}\n"
        skill_list_info = "你有以下能力:\n"
        i=1
        for skill_id in agent_register.agent_skill_map[agent_id]:
            skill = agent_register.skill_map[skill_id]
            skill_list_info = skill_list_info + f"技能{i}, id: {skill_id}, 名称: {skill.name}, 描述:{skill.description} \n"
            i=i+1

        tool_list_info = "你有以下可以使用的工具：\n"
        i=1
        for tool in agent_register.tool_map.values():
            tool_list_info = tool_list_info + f"工具{i}, id: {tool.id}, 名称: {tool.name}, 描述:{tool.description}, 入参样式：{tool.parameters} \n"
            i=i+1


        disspatch_prompt = f"{disspatch_prompt} 当前用户输入: {message_context.messages[-1].content} \n"
        disspatch_prompt = f"{disspatch_prompt} 请根据用户输入，选择合适的智能体，给出结果"
        return disspatch_prompt