from model.context import MessageContext, UserInfo
import uuid

SessionContextHistory = {}
SubSessionContextHistory = {}
SubSession2Session = {}
class ContextManager:
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
        if ContextManager._initialized:
            return

    def get_session_context(self, session_id: str):
        if session_id in SessionContextHistory:
            return SessionContextHistory[session_id]
        else:
            return None

    def save_session_context(self, message_context: MessageContext):
        if message_context.session_id is None:
            print("session_id is None")
            return
        SessionContextHistory[message_context.session_id] = message_context


    def get_sub_session_context(self, sub_session_id: str):
        if sub_session_id in SubSessionContextHistory:
            return SubSessionContextHistory[sub_session_id]
        else:
            return None

    def save_sub_session_context(self, message_context: MessageContext):
        if message_context.sub_session_id is None or message_context.session_id is None:
            print("sub_session_id is None")
            return
        SubSessionContextHistory[message_context.sub_session_id] = message_context
        message_context[message_context.sub_session_id] = message_context.session_id

    def generate_sub_session_id(self, session_id: str):
        sub_session_id = str(uuid.uuid4())
        SubSession2Session[sub_session_id] = session_id
        return sub_session_id

    def get_session_id_by_session(self, sub_session_id: str):
        if sub_session_id in SubSession2Session:
            return SubSession2Session[sub_session_id]
        else:
            return None