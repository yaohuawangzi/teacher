import os
from typing import List, Dict, Any, Tuple
from utils.chromadb.store import VectorStore


class KnowledgeManager:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, knowledge_dir: str = None, collection_name: str = "knowledge", persist_directory: str = None):
        if self._initialized:
            return
        knowledge_dir = "../../knowledge"
        base = knowledge_dir or os.path.join(os.getcwd(), "knowledge")
        self.knowledge_dir = base
        self.store = VectorStore(collection_name=collection_name, persist_directory=persist_directory)
        self._initialized = True

    def _parse_yaml_front_matter(self, content: str) -> Tuple[Dict[str, Any], str]:
        if not content.startswith("---"):
            return {}, content
        parts = content.split("\n")
        end = None
        for i in range(1, len(parts)):
            if parts[i].strip() == "---":
                end = i
                break
        if end is None:
            return {}, content
        header_lines = parts[1:end]
        body = "\n".join(parts[end + 1 :])
        data: Dict[str, Any] = {}
        key = None
        for line in header_lines:
            if ":" in line:
                k, v = line.split(":", 1)
                k = k.strip()
                v = v.strip()
                key = None
                if v:
                    data[k] = v.strip().strip("[]")
                else:
                    key = k
            else:
                s = line.strip().lstrip("-").strip()
                if key:
                    if key not in data or not isinstance(data[key], list):
                        data[key] = []
                    if s:
                        data[key].append(s)
        for k in list(data.keys()):
            v = data[k]
            if isinstance(v, str) and "," in v:
                data[k] = [x.strip() for x in v.split(",") if x.strip()]
            elif isinstance(v, str) and v:
                data[k] = [v]
        return data, body

    def _normalize_meta(self, meta: Dict[str, Any]) -> Dict[str, Any]:
        biz = None
        kws = None
        for k in ["biz", "business", "业务线"]:
            if k in meta:
                biz = meta[k]
                break
        for k in ["keywords", "key_words", "关键词"]:
            if k in meta:
                kws = meta[k]
                break
        biz = biz if isinstance(biz, list) else ([biz] if biz else [])
        kws = kws if isinstance(kws, list) else ([kws] if kws else [])
        return {"biz": biz, "keywords": kws}

    def _read_file(self, path: str) -> str:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def _split_markdown_sections(self, body: str) -> List[Dict[str, Any]]:
        lines = body.splitlines()
        n = len(lines)
        bounds = []
        for i in range(n):
            line = lines[i]
            prev_blank = i == 0 or lines[i - 1].strip() == ""
            next_blank = i + 1 >= n or lines[i + 1].strip() == ""
            is_heading = line.lstrip().startswith("#")
            is_blank_title = prev_blank and next_blank and line.strip() != ""
            if is_heading or is_blank_title:
                bounds.append(i)
        if not bounds:
            parts = [p.strip() for p in body.split("\n\n") if p.strip()]
            return [{"title": "", "text": p} for p in parts]
        chunks = []
        for idx, b in enumerate(bounds):
            e = bounds[idx + 1] if idx + 1 < len(bounds) else n
            segment = "\n".join(lines[b:e]).strip()
            title_line = lines[b].strip()
            if title_line.lstrip().startswith("#"):
                t = title_line.lstrip("#").strip()
            else:
                t = title_line
            if segment:
                chunks.append({"title": t, "text": segment})
        return chunks

    def ingest_all(self) -> List[str]:
        ids: List[str] = []
        files = []
        if os.path.isdir(self.knowledge_dir):
            for name in os.listdir(self.knowledge_dir):
                if name.lower().endswith(".md"):
                    files.append(os.path.join(self.knowledge_dir, name))
        texts: List[str] = []
        metadatas: List[Dict[str, Any]] = []
        for p in files:
            raw = self._read_file(p)
            meta_raw, body = self._parse_yaml_front_matter(raw)
            meta = self._normalize_meta(meta_raw)
            i = os.path.relpath(p, self.knowledge_dir)
            if not body.strip():
                kw_text = " ".join(meta.get("keywords", []))
                if kw_text.strip():
                    ids.append(i + "#kw")
                    texts.append(kw_text)
                    m = {"path": p, "section": "keywords"}
                    m.update(meta)
                    metadatas.append(m)
            else:
                chunks = self._split_markdown_sections(body)
                for c_idx, c in enumerate(chunks):
                    ids.append(f"{i}#s{c_idx+1}")
                    texts.append(c["text"])
                    m = {"path": p, "section": c.get("title", "")}
                    m.update(meta)
                    metadatas.append(m)
        if ids:
            self.store.add(ids=ids, texts=texts, metadatas=metadatas)
        return ids

    def query(self, text: str, n_results: int = 1, where: Dict[str, Any] = None):
        return self.store.query(text=text, n_results=n_results, where=where or {})

if __name__ == '__main__':
    km = KnowledgeManager()
    km.ingest_all()
    res = km.query("我们班多少人")
    print(km.query("如何查询订单"))
