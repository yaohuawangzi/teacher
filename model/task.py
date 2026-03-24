from dataclasses import dataclass
from typing import List, Optional, Dict
from enum import Enum
import time


# 任务生命周期状态枚举
class TaskStatus(Enum):
    PENDING = "pending"  # 待执行
    RUNNING = "running"  # 执行中
    SUCCEEDED = "succeeded"  # 执行成功
    FAILED = "failed"  # 执行失败
    CANCELLED = "cancelled"  # 已取消
    DEPENDENCY_FAILED = "dependency_failed"  # 依赖任务失败


# 核心任务结构体
@dataclass
class Task:
    # 1. 唯一标识（必选）
    task_id: str  # 全局唯一任务ID（如 "task_123456"）
    agent_id: str  # 执行任务的Agent ID（如 "life_mentor"）

    # 2. 执行内容（必选）
    original_query: str  # 原始用户查询/任务指令
    session_id: Optional[str] = None  # 关联的Agent会话ID（可选）
    sub_session_id: Optional[str] = None  # 关联的子Agent会话ID（可选）
    params: Optional[Dict] = None  # 任务参数（如Agent配置、工具权限）

    # 3. 依赖关系（可选）
    dependencies: List[str] = None  # 依赖的任务ID列表（如 ["task_654321"]）

    # 4. 生命周期控制（自动维护）
    status: TaskStatus = TaskStatus.PENDING  # 初始状态为待执行
    create_time: float = time.time()  # 任务创建时间戳
    start_time: Optional[float] = None  # 执行开始时间戳
    end_time: Optional[float] = None  # 执行结束时间戳

    # 5. 结果存储（执行后填充）
    result: Optional[Dict] = None  # 任务执行结果（如Agent返回内容）
    error: Optional[str] = None  # 错误信息（失败时填充）
    retry_count: int = 0  # 重试次数
    max_retries: int = 3  # 最大重试次数