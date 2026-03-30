from typing import List, Optional, Dict, Any
from .client import ChromaClient
from .embeddings import HashEmbeddings


class VectorStore:
    def __init__(self, collection_name: str = "knowledge", persist_directory: Optional[str] = None, dim: int = 768):
        self.collection = None
        self._memory = {"ids": [], "texts": [], "metadatas": [], "embeddings": []}
        try:
            self.client = ChromaClient(persist_directory=persist_directory)
            self.collection = self.client.get_or_create_collection(collection_name)
        except Exception:
            self.client = None
        self.embedder = HashEmbeddings(dim=dim)

    def add(self, ids: List[str], texts: List[str], metadatas: Optional[List[Dict[str, Any]]] = None, embeddings: Optional[List[List[float]]] = None):
        e = embeddings or self.embedder.embed_documents(texts)
        m = metadatas or [{} for _ in ids]
        if self.collection:
            self.collection.add(ids=ids, documents=texts, metadatas=m, embeddings=e)
        else:
            self._memory["ids"].extend(ids)
            self._memory["texts"].extend(texts)
            self._memory["metadatas"].extend(m)
            self._memory["embeddings"].extend(e)

    def query(self, text: str, n_results: int = 5, where: Optional[Dict[str, Any]] = None):
        q = self.embedder.embed(text)
        if self.collection:
            return self.collection.query(query_embeddings=[q], n_results=n_results, where=where)
        ids = self._memory["ids"]
        docs = self._memory["texts"]
        metas = self._memory["metadatas"]
        embs = self._memory["embeddings"]
        scores = []
        for i, e in enumerate(embs):
            s = sum(a * b for a, b in zip(e, q))
            scores.append((s, i))
        scores.sort(key=lambda x: x[0], reverse=True)
        top = scores[: n_results]
        result_ids = [ids[i] for _, i in top]
        result_docs = [docs[i] for _, i in top]
        result_metadatas = [metas[i] for _, i in top]
        return {"ids": [result_ids], "documents": [result_docs], "metadatas": [result_metadatas]}
