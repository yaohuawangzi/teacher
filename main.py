from core.router_dispatch.dispatcher_agent import DispatcherAgent
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


if __name__ == "__main__":
    # 初始化 AgentManager 和 SkillManager
    DispatcherAgent().dispatch("1", "1", "我有一道题目不太会而且压力比较大")


