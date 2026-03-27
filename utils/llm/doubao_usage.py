import os
import sys

import configs.llm
import utils.llm
import os
import json
import requests
from dotenv import load_dotenv
from typing import Any, List, Optional, Dict, AsyncIterator
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ChatMessage
from langchain_core.outputs import ChatResult, ChatGeneration, Generation
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.pydantic_v1 import Field

# 加载环境变量（存放豆包API密钥）
load_dotenv()

try:
    from .doubao_client import DoubaoClient
except Exception:
    from utils.llm.doubao_client import DoubaoClient


def SendDouBaoMessage(user_input: str):
    api_key = configs.llm.API_KEY
    if not api_key:
        print("missing api key", file=sys.stderr)
        sys.exit(1)
    model = os.getenv("DOUBAO_MODEL", "doubao-1-5-lite-32k-250115")
    base_url = os.getenv("DOUBAO_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
    client = DoubaoClient(api_key=api_key, model=model, base_url=base_url)
    messages = [
        {"role": "user", "content": user_input},
    ]
    res = client.chat(messages)
    return res

def DouBaoLLm(messages: List[dict]):
    api_key = configs.llm.API_KEY
    if not api_key:
        print("missing api key", file=sys.stderr)
        sys.exit(1)
    model = os.getenv("DOUBAO_MODEL", "doubao-1-5-lite-32k-250115")
    base_url = os.getenv("DOUBAO_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
    client = DoubaoClient(api_key=api_key, model=model, base_url=base_url)
    res = client.chat(messages)
    if res is not None:
        if 'choices' in res:
            choices = res['choices']
            if len(choices) > 0:
                choice = choices[0]
                if 'message' in choice:
                    message = choice['message']
                    if 'content' in message:
                        content = message['content']
                        role = message['role']
                        return role, content
    return None, None

# ===================== 核心：封装豆包大模型为LangChain ChatModel =====================
class DoubaoChatModel(BaseChatModel):
    """
    适配LangChain的豆包大模型ChatModel类，实现统一的invoke/stream接口
    """
    # 豆包API配置（可通过参数传入或环境变量读取）
    api_key: str = Field(default= configs.llm.API_KEY)
    base_url: str = Field(default="https://ark.cn-beijing.volces.com/api/v3")
    model: str = Field(default="doubao-1-5-lite-32k-250115")
    temperature: float = Field(default=0.0)  # 温度系数，0表示输出稳定

    def _convert_messages(self, messages: List[BaseMessage]) -> List[Dict]:
        """
        将LangChain的Message格式转换为豆包API要求的格式
        LangChain: HumanMessage/AIMessage → 豆包：role=user/assistant
        """
        converted = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                converted.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                converted.append({"role": "assistant", "content": msg.content})
            elif isinstance(msg, ChatMessage):
                converted.append({"role": msg.role, "content": msg.content})
        return converted

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        try:
            client = DoubaoClient(api_key=self.api_key, model=self.model, base_url=self.base_url)
            resp = client.chat(self._convert_messages(messages))
            ai_msg = AIMessage(content=resp["choices"][0]["message"]["content"])
            return ChatResult(generations=[ChatGeneration(message=ai_msg)])

        except Exception as e:
            raise ValueError(f"调用豆包API失败：{str(e)}") from e

    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,** kwargs: Any,
    ) -> ChatResult:
        """异步调用（可选，适配异步场景）"""
        # 简单实现：同步转异步（生产环境可改用aiohttp）
        return self._generate(messages, stop, run_manager, **kwargs)

    @property
    def _llm_type(self) -> str:
        """标识LLM类型，LangChain内部使用"""
        return "doubao-chat-model"



if __name__ == "__main__":
    SendDouBaoMessage("请用一句话介绍你自己")

