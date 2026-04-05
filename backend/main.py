import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from chain import get_sql_chain
from database import run_query, get_schema

load_dotenv()

app = FastAPI(
    title="NL to SQL Chatbot API",
    description="Convert natural language questions to SQL queries using LangChain and OpenAI",
    version="1.0.0"
)

# Allow Streamlit frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load chain once at startup
generate_sql = get_sql_chain()


class QuestionRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    question: str
    sql: str
    results: list
    row_count: int


@app.get("/")
def root():
    return {"status": "NL to SQL API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/schema")
def schema():
    """Return the current database schema."""
    try:
        return {"schema": get_schema()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query", response_model=QueryResponse)
def query(request: QuestionRequest):
    """
    Accept a natural language question,
    generate SQL, run it, and return results.
    """
    try:
        # Step 1: Generate SQL from question
        sql = generate_sql(request.question)

        # Step 2: Run the SQL on PostgreSQL
        results = run_query(sql)

        return QueryResponse(
            question=request.question,
            sql=sql,
            results=results,
            row_count=len(results)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
