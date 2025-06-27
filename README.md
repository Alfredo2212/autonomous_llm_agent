Autonomous LLM Agent
--
This project is designed to develop a micro-agent that duplicates the core functionality of an LLM-powered AI Engine. It accepts user queries, retrieve relevant context from a knowledge base, and finally generate a well-structured source-cited response with an objective to minimize hallucination.

Core Functionalities 
--
1. Query Ingestion via FastAPI
2. Context Retrieval (RAG)
3. LLM Based Answer Generation
4. Structured JSON Response
5. Query and Logging

Tools
--
1. FastAPI
3. Transformers (Hugging Face)
4. ChromaDB
5. Redis
6. SQLite
7. Uvicorn

Run Walkthrough
--
1. Clone the Repository :
git clone https://github.com/Alfredo2212/autonomous_llm_agent.git
cd autonomous_llm_agent
2. It is urged to setup virtual environment
3. Make sure to have Python 3.8 or above installed
4. Install dependencies
pip install fastapi uvicorn transformers sentence-transformers chromadb redis 
5. Terminal input -> uvicorn main:app --reload
6. go to http://127.0.0.1:8000/docs

Output 
-- 
1. query_logs.db :
to open this file go terminal -> sqlite3 query_logs.db -> .tables -> SELECT * FROM logs;
