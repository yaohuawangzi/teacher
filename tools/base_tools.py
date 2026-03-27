from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Optional, Any
import json

@dataclass
class ToolResult:
    """
    所有 BaseTool 子类 execute 必须返回这个格式
    强制统一输出结构，避免格式混乱
    """
    success: bool = True                 # 执行是否成功（必选）
    data: Optional[Any] = None     # 执行结果数据（成功时返回）
    message: str = ""              # 提示信息（成功/失败描述）
    error: Optional[str] = None   # 错误信息（失败时返回）

    def to_json(self, ensure_ascii=False, indent=2) -> str:
        """
        把 ToolResult 转为标准 JSON 字符串
        ensure_ascii=False：支持中文正常显示
        indent=2：格式化输出，方便阅读
        """
        return json.dumps(asdict(self), ensure_ascii=ensure_ascii, indent=indent)


class BaseTool(ABC):
    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        """技能执行入口（必须实现）"""
        raise NotImplementedError("子类必须重写 execute 方法")

