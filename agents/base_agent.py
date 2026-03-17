from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgent(ABC):
    """所有Agent的基类，定义统一接口"""
    def __init__(self, agent_id: str, soul_config: dict):
        self.agent_id = agent_id
        self.soul_config = soul_config  # 从soul.md加载的配置
        self.context = {}  # 会话上下文

    @abstractmethod
    def run(self, user_input: str, context: Dict[str, Any]) -> Any:
        """核心执行方法，子类必须实现"""
        pass