from fastapi import FastAPI, HTTPException
from retriever import retrieve_documents, embed_documents, store_in_chroma, semantic_search
from llm_agent import generate_answer
from pydantic import BaseModel
import os 

app = FastAPI()

class QueryInput(BaseModel):
    query: str

docs = retrieve_documents()
embeddings = embed_documents(docs)
collection = store_in_chroma(docs, embeddings)

@app.post("/query")
def query_agent(query: QueryInput):
    try:
        print("Query received:", query.query)
        reference_docs = semantic_search(collection, query.query)
        print("Retrieved docs:", reference_docs)
    except Exception as e:
        print("Error occured:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "answer": generate_answer(query.query, reference_docs["documents"]),
        "sources": reference_docs["sources"]
    }
