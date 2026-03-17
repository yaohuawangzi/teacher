import os
import json
import requests


class DoubaoClient:
    def __init__(self, api_key=None, model=None, base_url=None, timeout=60):
        self.api_key = api_key or os.getenv("DOUBAO_API_KEY") or os.getenv("ARK_API_KEY") or os.getenv("VOLC_API_KEY")
        if not self.api_key:
            raise ValueError("missing api key")
        self.model = model or os.getenv("DOUBAO_MODEL", "doubao-1-5-lite-32k-250115")
        self.base_url = (base_url or os.getenv("DOUBAO_BASE_URL") or "https://ark.cn-beijing.volces.com/api/v3").rstrip("/")
        self.timeout = timeout

    def _post_json(self, path, payload):
        url = f"{self.base_url}/{path.lstrip('/')}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response is not None else "unknown"
            detail = e.response.text if e.response is not None else str(e)
            raise RuntimeError(f"http {status}: {detail}") from e
        except requests.exceptions.RequestException as e:
            raise RuntimeError(str(e)) from e

    def chat(self, messages, temperature=0.7, top_p=None, stream=False, tools=None, tool_choice=None, extra_body=None):
        body = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": bool(stream),
        }
        if top_p is not None:
            body["top_p"] = top_p
        if tools:
            body["utils"] = tools
        if tool_choice:
            body["tool_choice"] = tool_choice
        if isinstance(extra_body, dict):
            body.update(extra_body)
        return self._post_json("chat/completions", body)

    def get_text(self, response):
        try:
            choices = response.get("choices") or []
            if not choices:
                return ""
            c = choices[0]
            msg = c.get("message") or {}
            if "content" in msg and msg["content"] is not None:
                return msg["content"]
            delta = c.get("delta") or {}
            return delta.get("content") or ""
        except Exception:
            return ""
