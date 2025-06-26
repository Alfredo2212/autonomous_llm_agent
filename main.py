from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class QueryInput(BaseModel):
    query: str

@app.post("/query")
async def query_agent(input: QueryInput):
    return {"message": f"Received query: {input.query}"}