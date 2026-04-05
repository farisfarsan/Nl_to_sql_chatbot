import streamlit as st
import requests
import pandas as pd
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

st.set_page_config(
    page_title="NL to SQL Chatbot",
    page_icon=None,
    layout="wide"
)

st.title("NL to SQL Chatbot")
st.caption("Ask questions about your database in plain English")

# Sidebar
with st.sidebar:
    st.header("About")
    st.markdown("""
    This chatbot converts your **natural language questions**
    into **SQL queries** and runs them on a PostgreSQL database.

    **How to use:**
    1. Type your question below
    2. The AI generates SQL
    3. Results are shown as a table
    """)

    st.divider()

    st.subheader("Database Schema")
    if st.button("Load Schema", use_container_width=True):
        try:
            res = requests.get(f"{BACKEND_URL}/schema")
            if res.status_code == 200:
                st.session_state.schema = res.json()["schema"]
            else:
                st.error("Failed to load schema")
        except Exception as e:
            st.error(f"Backend not reachable: {e}")

    if "schema" in st.session_state:
        st.code(st.session_state.schema, language="sql")

    st.divider()

    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome message
if len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        st.markdown("""
        Hello! I can query your database using plain English.

        **Try asking:**
        - *Show me all users*
        - *How many orders were placed last month?*
        - *What are the top 5 products by sales?*
        """)

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "sql" in msg:
            with st.expander("Generated SQL"):
                st.code(msg["sql"], language="sql")
        if "results" in msg and msg["results"]:
            with st.expander(f"Results ({msg['row_count']} rows)"):
                df = pd.DataFrame(msg["results"])
                st.dataframe(df, use_container_width=True)

# Handle input
if prompt := st.chat_input("Ask a question about your database..."):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Generating SQL and fetching results..."):
            try:
                res = requests.post(
                    f"{BACKEND_URL}/query",
                    json={"question": prompt}
                )

                if res.status_code == 200:
                    data = res.json()
                    sql = data["sql"]
                    results = data["results"]
                    row_count = data["row_count"]

                    st.markdown(f"Found **{row_count}** result(s).")

                    with st.expander("Generated SQL"):
                        st.code(sql, language="sql")

                    if results:
                        with st.expander(f"Results ({row_count} rows)", expanded=True):
                            df = pd.DataFrame(results)
                            st.dataframe(df, use_container_width=True)
                    else:
                        st.info("Query ran successfully but returned no results.")

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Found **{row_count}** result(s).",
                        "sql": sql,
                        "results": results,
                        "row_count": row_count
                    })

                else:
                    error = res.json().get("detail", "Unknown error")
                    st.error(f"Error: {error}")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Error: {error}"
                    })

            except Exception as e:
                st.error(f"Could not reach backend: {e}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Could not reach backend: {e}"
                })
