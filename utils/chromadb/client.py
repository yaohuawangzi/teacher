import os
from typing import Optional
import chromadb
from chromadb import PersistentClient
from chromadb.config import Settings


class ChromaClient:
    def __init__(self, persist_directory: Optional[str] = None):
        base = persist_directory or os.path.join(os.getcwd(), ".chromadb")
        os.makedirs(base, exist_ok=True)
        settings = Settings(anonymized_telemetry=False)
        self.client: PersistentClient = chromadb.PersistentClient(path=base, settings=settings)

    def get_or_create_collection(self, name: str, metadata: Optional[dict] = None):
        return self.client.get_or_create_collection(name=name, metadata=metadata or {})

    def get_collection(self, name: str):
        return self.client.get_collection(name=name)

    def delete_collection(self, name: str):
        self.client.delete_collection(name)
