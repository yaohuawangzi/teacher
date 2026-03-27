from core.router_dispatch.dispatcher_agent import DispatcherAgent
import os
import sys
from core.router_dispatch.plan import DispatcherSkill

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


if __name__ == "__main__":
    # 初始化 AgentManager 和 SkillManager
    DispatcherSkill().dispatch("1", "1", "我的学号123，想知道我们班有多少人")


