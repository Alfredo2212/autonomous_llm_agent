from fastapi import FastAPI, HTTPException
from retriever import retrieve_documents, embed_documents, store_in_chroma
from pydantic import BaseModel
import os 

app = FastAPI()

class QueryInput(BaseModel):
    query: str

data_dir = "data/"
docs = []
for filename in os.listdir(data_dir):
    with open(os.path.join(data_dir, filename), "r") as f:
        docs.append({"source":filename, "content": f.read()})

embeddings = embed_documents(docs)
collection = store_in_chroma(docs, embeddings)

@app.post("/query")
def query_agent(query: QueryInput):
    try:
        reference_docs = retrieve_documents(query.query, collection)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "answer": "Placeholder answer based on retrieved docs",
        "sources": [doc["source"] for doc in reference_docs]
    }