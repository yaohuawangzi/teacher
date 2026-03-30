from typing import Dict, Any, List
import os
from .base_tools import BaseTool, ToolResult
from core.ability_registration.knowledge_manager import KnowledgeManager


class KnowledgeQueryTool(BaseTool):
    def execute(params: Dict[str, Any]) -> ToolResult:
        result = ToolResult(success=False)
        if "query_text" not in params or not params["query_text"]:
            result.error = "参数错误：缺少必填项 query_text"
            return result
        query_text = params.get("query_text")
        top_k = params.get("top_k", 1)
        where = params.get("where", None)
        km = KnowledgeManager()
        if not os.path.isdir(km.knowledge_dir):
            alt = os.path.join(os.getcwd(), "knowledge")
            if os.path.isdir(alt):
                km.knowledge_dir = alt
        km.ingest_all()
        res = km.query(query_text, n_results=top_k, where=where)
        ids: List[str] = (res.get("ids") or [[]])[0]
        docs: List[str] = (res.get("documents") or [[]])[0]
        metas: List[Dict[str, Any]] = (res.get("metadatas") or [[]])[0]
        items: List[Dict[str, Any]] = []
        n = min(len(ids), top_k)
        for i in range(n):
            items.append({"id": ids[i], "document": docs[i], "metadata": metas[i]})
        result.success = True
        result.data = items
        result.message = "查询成功"
        return result
