import utils.llm.doubao_usage
from core.ability_registration.register_agent_skill_tools import AgentRegister
from model.context import MessageContext, UserInfo
from core.context.context_manager import ContextManager
import json



from model.task import Task
class DispatcherSkill:
    def __init__(self):
        pass
    def dispatch(self,session_id:str,  user_id:str, user_input: str):
        # 存储对话
        context_manager = ContextManager()
        user =  UserInfo(user_id=user_id)
        message_context = MessageContext(session_id = session_id,user=user)

        if context_manager.get_session_context(session_id) is not None:
            message_context = context_manager.get_session_context(session_id)

        # 组装执行
        agent_register = AgentRegister()
        sys_prompt = self.generate_sys_prompt("main_agent", agent_register)
        query = user_input
        need_stop = False
        while need_stop is False:
            history = message_context.messages
            messages = self.build_message(history, query, sys_prompt)
            role, content = utils.llm.doubao_usage.DouBaoLLm(messages)
            message_context.add_message("user", query, None, None)
            if role is not None and content is not None:
                message_context.add_message(role, content, None, None)
                try:
                    data = json.loads(content)
                    if 'task_id' in data:
                        task_id = data['task_id']
                    if 'type' in data:
                        type = data['type']
                        if type == "plan" or type == "replan":
                            query = "Planing 阶段完成，请按照规划继续往下调度执行"
                        elif type == "action" or type == "knowledge_query":
                            if 'tool_call' in data:
                                tool_call = data['tool_call']
                                params = tool_call['parameters']
                                if 'tool_id' in tool_call:
                                    tool_id = tool_call['tool_id']
                                    tool = agent_register.tool_map[tool_id]
                                    task_run = tool.instance.execute(params)
                                    query= f"{task_id}这一步执行结果如下:" + task_run.to_json()
                                    # 执行func
                            # 执行func
                        elif type == "complete":
                            need_stop = True
                            break
                        elif type == "pause":
                            need_stop = True
                            break
                        else:
                            print("不支持的类型")
                            break
                    else:
                        print("不支持的类型")
                        break
                except Exception as e:
                    print(f"解析 {content} 失败: {e}")
                    break


    def generate_sys_prompt(self, agent_id, agent_register: AgentRegister):

        agent_info = agent_register.agent_map[agent_id]
        dispatch_prompt = f"agent_id: {agent_id}, 名称: {agent_info.name}, 描述: {agent_info.description}\n"
        disspatch_prompt = f"{dispatch_prompt} {agent_info.markDown}\n"
        skill_list_info = "# 你有以下能力:\n"
        i=1
        for skill in agent_register.skill_map.values():
            skill_list_info = skill_list_info + f"技能{i}, id: {skill.id}, 名称: {skill.name}, 描述:{skill.description},技能说明: {skill.filePath}， baseDir:{skill.baseDir} , 入参: {skill.parameters}\n"
            i=i+1
        disspatch_prompt = f"{disspatch_prompt} {skill_list_info}\n"
        tool_list_info = "# 你有以下可以使用的工具：\n"
        i=1
        for tool in agent_register.tool_map.values():
            tool_list_info = tool_list_info + f"工具{i}, id: {tool.id}, 名称: {tool.name}, 描述:{tool.description}, 入参样式：{tool.parameters} \n"
            i=i+1
        disspatch_prompt = f"{disspatch_prompt} {tool_list_info}\n"
        return disspatch_prompt

    def build_message(self, history: list, query: str, system_prompt: str = None):
        messages = []
        if system_prompt is not None:
            messages.append({"role": "system", "content": system_prompt})
        for message in history:
            messages.append({"role": message.role, "content": message.content})
        messages.append({"role": "user", "content": query})
        return messages