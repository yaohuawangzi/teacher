from typing import List
import math
import hashlib


class HashEmbeddings:
    def __init__(self, dim: int = 768):
        self.dim = dim

    def _hash(self, token: str) -> int:
        h = hashlib.sha256(token.encode("utf-8")).hexdigest()
        return int(h[:8], 16) % self.dim

    def embed(self, text: str) -> List[float]:
        buckets = [0.0] * self.dim
        for w in text.split():
            idx = self._hash(w.lower())
            buckets[idx] += 1.0
        norm = math.sqrt(sum(v * v for v in buckets)) or 1.0
        return [v / norm for v in buckets]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self.embed(t) for t in texts]
