'''
Accepts user query via FastAPI
Add as a clean central router integrator :
- Context Retrieval (FAISS / Chroma)
- Answer Generation (LLM)
- Caching (Redis)
- Logging (SQLite)
'''
import os 
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Project modules (Function Lists)
from retriever import retrieve_documents, embed_documents, store_in_chroma, semantic_search
from llm_agent import generate_answer
from logger import log_query
from cache import check_cache, store_cache

app = FastAPI()

# Creates a data model, expects JSON with single key
class QueryInput(BaseModel):
    query: str

docs = retrieve_documents() # This loads referenceXX.txt
embeddings = embed_documents(docs) # Generate embeddings with Sentence Transformers
collection = store_in_chroma(docs, embeddings) # Store it in ChromaDB

# Mainpost endpoint where user sends queries
# Check each functions in another .py files
@app.post("/query")
def query_agent(query: QueryInput):
    # Added error handling for ease of debugging
    try:
        print("Query received:", query.query)

        cached_result = check_cache(query.query)
        if cached_result:
            print("Returning from cache")
            return cached_result

        reference_docs = semantic_search(collection, query.query)
        print("Retrieved docs:", reference_docs)

        answer = generate_answer(query.query, reference_docs["documents"])
        result = {
            "answer": answer,
            "sources": reference_docs["sources"]
        }

        store_cache(query.query, result)
        log_query(query.query, answer, reference_docs["sources"])
        return result

    except Exception as e:
        print("Error occured:", str(e))
        raise HTTPException(status_code=500, detail=str(e))