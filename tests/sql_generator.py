from ai_data_analyst.model import ask_llm
from ai_data_analyst.schema import DATABASE_SCHEMA
from langchain_core.prompts import ChatPromptTemplate
from ai_data_analyst.tools import execute_sql


sql_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a senior data analyst.

Your job is to convert the user's business question
into a PostgreSQL SQL query.

Database schema:
{database_schema}

Rules:
- Generate PostgreSQL-compatible SQL.
- Only generate SELECT queries.
- Do not INSERT, UPDATE, DELETE, DROP, or ALTER.
- Use the correct table relationships.
- Return ONLY the SQL query.
- Do not use markdown code fences.
"""
    ),
    (
        "human",
        "{question}"
    ),
])


def generate_sql(question: str) -> str:
    prompt = sql_prompt.invoke({
        "database_schema": DATABASE_SCHEMA,
        "question": question,
    })
    return ask_llm(prompt)


if __name__=="__main__":
    sql = generate_sql("What are the number of customers ?")
    result = execute_sql.invoke({"query": sql})
    print(result)