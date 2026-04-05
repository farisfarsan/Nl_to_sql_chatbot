# NL to SQL Chatbot

A conversational chatbot that converts natural language questions into SQL queries and runs them on a PostgreSQL database. Built with Streamlit, FastAPI, LangChain, and OpenAI.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.37.1-red?logo=streamlit)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688?logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-316192?logo=postgresql)
![LangChain](https://img.shields.io/badge/LangChain-0.2.16-green)

---

## Features

- **Natural Language to SQL** — Ask questions in plain English, get SQL-powered answers
- **Auto Schema Detection** — LangChain automatically reads your database schema
- **Result Tables** — Query results displayed as interactive dataframes
- **SQL Transparency** — See the exact SQL query generated for every question
- **Chat History** — Conversation is preserved during the session
- **REST API** — FastAPI backend with Swagger docs at `/docs`
- **Single Container** — Frontend and backend run together via Supervisord

---

## How It Works

```
User types a question in Streamlit
        |
Streamlit sends request to FastAPI (/query)
        |
FastAPI passes question to LangChain
        |
LangChain fetches DB schema from PostgreSQL
        |
OpenAI GPT generates SQL from question + schema
        |
FastAPI runs the SQL on PostgreSQL
        |
Results returned and displayed as a table in Streamlit
```

---

## Tech Stack

| Layer           | Technology               |
|-----------------|--------------------------|
| Frontend        | Streamlit                |
| Backend         | FastAPI                  |
| LLM             | OpenAI GPT-3.5-turbo     |
| RAG Framework   | LangChain                |
| Database        | PostgreSQL 15            |
| ORM             | SQLAlchemy               |
| Process Manager | Supervisord              |
| Containerization| Docker + Docker Compose  |

---

## Project Structure

```
nl-to-sql-chatbot/
├── backend/
│   ├── main.py          # FastAPI app and API routes
│   ├── chain.py         # LangChain NL to SQL chain
│   └── database.py      # PostgreSQL connection and query runner
├── frontend/
│   └── app.py           # Streamlit UI
├── init-db/
│   └── init.sql         # Sample database schema and data
├── supervisord/
│   └── app.conf         # Supervisord config to run both services
├── Dockerfile           # Single image for frontend + backend
├── docker-compose.yml   # Orchestrates app + PostgreSQL
├── requirements.txt     # All Python dependencies
├── .env                 # API keys and DB credentials (git-ignored)

```

---

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- An [OpenAI API key](https://platform.openai.com/api-keys)

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/nl-to-sql-chatbot.git
cd nl-to-sql-chatbot
```

### 2. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here

POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=chatbot
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin123
```

### 3. Run with Docker

```bash
docker-compose up --build
```

### 4. Open in browser

| Service      | URL                        |
|--------------|----------------------------|
| Streamlit UI | http://localhost:8501      |
| FastAPI Docs | http://localhost:8000/docs |

### 5. Stop the app

```bash
docker-compose down
```

---

## Sample Questions

**Users**
- Show me all users
- How many users are there?
- Which cities do our users come from?

**Products**
- What are the top 3 most expensive products?
- Show me all electronics products
- Which products are low in stock?

**Orders**
- How many orders does each user have?
- What is the total revenue from all orders?
- Which product has been ordered the most?

**Combined**
- Show total revenue per product category
- Which city has the most users?
- Which user has spent the most money?

---

## API Endpoints

| Method | Endpoint | Description                         |
|--------|----------|-------------------------------------|
| GET    | /        | Health check                        |
| GET    | /health  | Service status                      |
| GET    | /schema  | Returns the current database schema |
| POST   | /query   | Accepts a question, returns SQL + results |

### Example request

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Show me all users"}'
```

### Example response

```json
{
  "question": "Show me all users",
  "sql": "SELECT * FROM users LIMIT 100;",
  "results": [
    {"id": 1, "name": "Alice Johnson", "email": "alice@example.com", "city": "New York"}
  ],
  "row_count": 5
}
```

---

## Environment Variables

| Variable            | Description                   | Required |
|---------------------|-------------------------------|----------|
| `OPENAI_API_KEY`    | Your OpenAI API key           | Yes      |
| `POSTGRES_HOST`     | PostgreSQL host               | Yes      |
| `POSTGRES_PORT`     | PostgreSQL port (default 5432)| Yes      |
| `POSTGRES_DB`       | Database name                 | Yes      |
| `POSTGRES_USER`     | Database user                 | Yes      |
| `POSTGRES_PASSWORD` | Database password             | Yes      |

---

## Running Without Docker

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Terminal 1 - Backend
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
streamlit run app.py
