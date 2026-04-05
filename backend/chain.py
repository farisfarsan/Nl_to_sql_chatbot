import os
import re
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from database import get_schema

load_dotenv()

def get_sql_chain():
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    prompt = ChatPromptTemplate.from_template("""
You are an expert SQL developer. Based on the database schema below, write a
valid PostgreSQL query to answer the user's question.

Rules:
- Return ONLY a single raw SQL query, nothing else
- Do NOT include any explanation or markdown
- Do NOT wrap the query in backticks or code blocks
- Do NOT return multiple queries
- Always start the query with SELECT, INSERT, UPDATE, or DELETE
- Always use lowercase table and column names
- Limit results to 100 rows unless the user specifies otherwise

Database Schema:
{schema}

User Question:
{question}

SQL Query:
""")

    def clean_sql(raw: str) -> str:
        # Remove markdown code blocks
        raw = raw.strip()
        raw = re.sub(r"```sql", "", raw)
        raw = re.sub(r"```", "", raw)
        raw = raw.strip()

        # Take only the first SQL statement
        # Split on semicolon and take first non-empty part
        statements = [s.strip() for s in raw.split(";") if s.strip()]
        if statements:
            sql = statements[0] + ";"
        else:
            sql = raw

        # Ensure it starts with a valid SQL keyword
        if not re.match(r"^(SELECT|INSERT|UPDATE|DELETE|WITH)", sql, re.IGNORECASE):
            # Try to find SELECT in the string
            match = re.search(r"(SELECT|WITH)\s+", sql, re.IGNORECASE)
            if match:
                sql = sql[match.start():]

        return sql.strip()

    def generate_sql(question: str) -> str:
        schema = get_schema()
        chain = (
            prompt
            | llm
            | StrOutputParser()
        )
        raw_sql = chain.invoke({
            "schema": schema,
            "question": question
        })
        return clean_sql(raw_sql)

    return generate_sql
