from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import os
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

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


# Load model
model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
qa_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)
def generate_answer(query: str, reference_docs: list) -> str:
    context_text = "\n\n".join([doc["content"] for doc in reference_docs])

    prompt = (
        f"You are a helpful research assistant. Based only on the context below, "
        f"answer the following question concisely:\n\n"
        f"Context:\n{context_text}\n\n"
        f"Question: {query}\nAnswer:"
    )

    response = qa_pipeline(prompt, max_new_tokens=200, do_sample=True, temperature=0.7, return_full_text=False)
    return response[0]['generated_text'].split("Answer:")[-1].strip()