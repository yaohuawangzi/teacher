import chromadb
from chromadb.utils import embedding_functions

ChromdbClient = None
def initCli():
    if ChromdbClient is None:
        # --------------------------
        # 1. 初始化 Chroma 客户端
        # --------------------------
        # 方式1：内存模式（数据仅在运行时存在，重启后丢失）
        ChromdbClient = chromadb.Client()

        # 方式2：持久化模式（数据保存到本地文件夹，重启后不丢失）
        # ChromdbClient = chromadb.PersistentClient(path="./chroma_db")


def addSkills(collection, skills):
    # --------------------------
    # 2. 创建/获取集合（Collection）
    # --------------------------
    # 集合是 Chroma 存储数据的基本单元，类似数据库的「表」
    # embedding_function：指定嵌入函数（将文本转为向量），这里用默认的 all-MiniLM-L6-v2
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    # 创建集合（如果已存在则获取）
    collection = ChromdbClient.get_or_create_collection(
        name="skills",  # 集合名称
        embedding_function=sentence_transformer_ef,  # 嵌入函数
        metadata={"hnsw:space": "cosine"}  # 可选：指定相似度计算方式（cosine/euclidean/dot）
    )

def getSkills(collection, query):
    # --------------------------
    # 2. 创建/获取集合（Collection）
    # --------------------------
    # 集合是 Chroma 存储数据的基本单元，类似数据库的「表」
    # embedding_function：指定嵌入函数（将文本转为向量），这里用默认的 all-MiniLM-L6-v2
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    # 创建集合（如果已存在则获取）
    collection = ChromdbClient.get_or_create_collection(
        name="skills",  # 集合名称
        embedding_function=sentence_transformer_ef,  # 嵌入函数
        metadata={"hnsw:space": "cosine"}  # 可选：指定相似度计算方式（cosine/euclidean/dot）
    )