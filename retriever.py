from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import os

def retrieve_documents():
    docs = []
    for i in range(1,11):
        file_name = f"reference{str(i).zfill(2)}.txt"
        file_path = os.path.join("data", file_name)
        with open(file_path, "r") as f:
            content = f.read()
            docs.append({
                "source": file_name,
                "content": content
            })
    return docs

def embed_documents(docs):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = [doc["content"] for doc in docs]
    embeddings = model.encode(texts)
    return embeddings

def store_in_chroma(docs, embeddings):
    client = chromadb.Client()
    collection = client.get_or_create_collection(name="reference_docs")

    ids = [doc["source"] for doc in docs]
    texts = [doc["content"] for doc in docs]

    collection.add(
        documents=texts,
        embeddings=embeddings.tolist(),
        ids=ids
    )

    return collection

def semantic_search(collection, query: str, k=3):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.Client()
    collection = client.get_collection(name="reference_docs")

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    return {
        "documents": [
            {"source": id, "content": doc}
            for id, doc in zip(results["ids"][0], results["documents"][0])
        ],
        "sources": results['ids'][0]
    }


