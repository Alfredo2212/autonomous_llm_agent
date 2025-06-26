from fastapi import FastAPI, HTTPException
from retriever import retrieve_documents
from pydantic import BaseModel

app = FastAPI()

class QueryInput(BaseModel):
    query: str

@app.post("/query")
def query_agent(query: QueryInput):
    try:
        reference_docs = retrieve_documents(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "answer": "Placeholder answer based on retrieved docs",
        "sources": [doc["source"] for doc in reference_docs]
    }