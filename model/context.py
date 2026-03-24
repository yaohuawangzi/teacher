from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import time
import uuid
@dataclass
class Agent:
    id: str
    name: str

@dataclass
class SkillOutput:
    """技能输出结构体（标准格式）"""
    status: str  # success/failed
    data: Dict[str, Any] = field(default_factory=dict)
    message: str = ""
@dataclass
class MessageMetadata:
    """消息扩展信息结构体"""
    intent: Optional[str] = None
    confidence: float = 0.0
    skill_name: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    output: Optional[SkillOutput] = None
    status: Optional[str] = None  # 技能执行状态：pending/completed/failed
    source_skills: List[str] = field(default_factory=list)

@dataclass
class Message:
    message_id: str
    #user	用户输入	content（用户原话）、metadata.intent（意图）
    #system 系统提示content（Agent人设 / 规则）
    #skill 技能执行记录metadata.skill_name（技能名）、metadata.parameters（入参）、metadata.output（输出）
    #assistant  Agent回复 content（最终回复）、metadata.source_skills（关联技能）
    role: str
    agent: Agent
    content: str
    timestamp: int = field(default_factory=lambda: int(time.time()))
    metadata: MessageMetadata = field(default_factory=MessageMetadata)


@dataclass
class UserInfo:
    user_id: str

@dataclass
class MessageContext:
    # 对话唯一标识，用于关联多轮消息（如多轮对话）
    session_id: str
    # 子对话标识
    sub_session_id: str
    user: UserInfo  # 用户信息
    messages: List[Message] = field(default_factory=list)

    # 消息创建时间
    created_at: int = field(default_factory=lambda: int(time.time()))

    # 消息状态，active（进行中）/closed（已结束）/archived（已归档）
    status: str = "active"


    # 辅助方法：添加消息
    def add_message(self, role: str, content: str, metadata: Optional[MessageMetadata] = None, agent: Agent = None):
        """添加一条消息到对话"""
        self.messages.append(Message(
            message_id=str(uuid.uuid4()),
            role=role,
            content=content,
            metadata=metadata or MessageMetadata(),
            agent = agent
        ))
        self.updated_at = int(time.time())  # 更新时间戳

    # 辅助方法：添加技能执行记录
    def add_skill_execution(self, skill_name: str, params: Dict[str, Any], output: SkillOutput, agent: Agent):
        """添加技能执行记录（role=skill）"""
        metadata = MessageMetadata(
            skill_name=skill_name,
            parameters=params,
            output=output,
            status="completed"
        )
        self.add_message(
            role="skill",
            content="",
            agent=agent,
            metadata=metadata
        )
        # 将技能输出存入全局上下文
        self.context[f"{skill_name}_output"] = output.data

