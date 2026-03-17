import os
import sys
try:
    from .doubao_client import DoubaoClient
except Exception:
    from utils.llm.doubao_client import DoubaoClient


def main():
    api_key = os.getenv("DOUBAO_API_KEY") or os.getenv("ARK_API_KEY") or os.getenv("VOLC_API_KEY")
    api_key = "51ca9fa0-db22-4c3d-928c-94ba21531837"
    if not api_key:
        print("missing api key", file=sys.stderr)
        sys.exit(1)
    model = os.getenv("DOUBAO_MODEL", "doubao-1-5-lite-32k-250115")
    base_url = os.getenv("DOUBAO_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
    client = DoubaoClient(api_key=api_key, model=model, base_url=base_url)
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "请用一句话介绍你自己"},
    ]
    res = client.chat(messages)
    print(client.get_text(res))


if __name__ == "__main__":
    main()

