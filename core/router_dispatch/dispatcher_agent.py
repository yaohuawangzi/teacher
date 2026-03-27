import json
from datetime import time

import model.task
import utils.llm.doubao_usage
from core.ability_registration.register_agent_skill_tools import AgentRegister
from core.context.context_manager import ContextManager
from core.router_dispatch.plan import DispatcherSkill
from core.task.task_run import TaskManager
from model.context import MessageContext, UserInfo
import uuid
import asyncio
import time
from typing import List, Dict, Set

class DispatcherAgent:
    def __init__(self):
        pass


    def dispatch(self, session_id: str, user_id, user_input: str):
        agent_register = AgentRegister()
        user = UserInfo(user_id=user_id)
        message_context = MessageContext(session_id=session_id,user=user)
        context_manager = ContextManager()
        if context_manager.get_session_context(session_id) is not None:
            message_context = context_manager.get_session_context(session_id)

        message_context.add_message("user", user_input, None, None)
        # 存储主会话上下文
        context_manager.save_session_context(session_id, message_context)
        # llm判断调用哪个agent
        generate_prompt = self.generate_prompt(agent_register, message_context)
        res = utils.llm.doubao_usage.SendDouBaoMessage(generate_prompt)

        task_info = {}
        if res is not None:
            if 'choices' in res:
                choices = res['choices']
                if len(choices) > 0:
                    choice = choices[0]
                    if 'context' in choice:
                        message = choice['context']
                        if 'content' in message:
                            content = message['content']
                            role = message['role']
                            message_context.add_message(role, content, None, None)
                            # task_info = json.loads(content)
                            sub_session_id = context_manager.generate_sub_session_id(session_id),
                            # dispatch_skill = DispatcherSkill(sub_session_id, user_id,content)

        # # 生成任务并创建子
        # tasks= []
        # if task_info is not None:
        #     if 'tasks' in task_info:
        #         if len(task_info['tasks']) > 0:
        #             for task in task_info['tasks']:
        #                 agent_id = task.agent_id
        #                 tasks.append(task)
        #                 if agent_id not in agent_register.agent_map:
        #                     print(f"没有找到对应的智能体，将任务分配给子静态智能体")
        #                     break
        #                 one_task = model.task.Task(
        #                     task_id=task["task_id"],
        #                     agent_id=agent_id,
        #                     original_query=task["original_query"],
        #                     session_id= session_id,
        #                     sub_session_id=uuid.uuid4().hex,
        #                     dependencies=task["dependencies"],
        #                 )
        #                 tasks.append(one_task)
        #
        # if len(tasks) > 0:
        #     TaskManager().schedule_tasks(tasks)



    def generate_prompt(self, agent_register:AgentRegister,message_context:MessageContext):
        main_agent = agent_register.agent_map["main_agent"]
        agent_info=""
        i = 1
        for agent in agent_register.agent_map.values():
            if agent.id != "main_agent" and agent.id != "sub_react_agent":
                agent_info =agent_info + f"智能体 {i}: id: {agent.id}, 名称: {agent.name}, 描述: {agent.description}, 核心职能: {agent.core_competency}\n"
                i=i+1
        disspatch_prompt= f"你是一个{main_agent.description} \n 核心职能为 {main_agent.core_competency}\n 约束条件为 {main_agent.constraints}\n, 输入demo为{main_agent.request_schema}\n，输出格式为{main_agent.response_schema}\n"
        disspatch_prompt=f"{disspatch_prompt} 当前有以下智能体可以使用: \n{agent_info}\n"
        disspatch_prompt = f"{disspatch_prompt} 当前用户输入: {message_context.messages[-1].content} \n"
        disspatch_prompt = f"{disspatch_prompt} 请根据用户输入，选择合适的智能体，给出结果"
        return disspatch_prompt