from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

def embed_documents(docs):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = [doc["content"] for doc in docs]
    embeddings = model.encode(texts)
    return embeddings

def store_in_chroma(docs, embeddings):
    client = chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=".chroma"
    ))

    collection = client.get_or_create_collection(name="reference_docs")

    ids = [doc["source"] for doc in docs]
    texts = [doc["content"] for doc in docs]

    collection.add(
        documents=texts,
        embeddings=embeddings.tolist(),
        ids=ids
    )

    return collection
