from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
    ToolMessage,
)

from ai_data_analyst.model import llm
from ai_data_analyst.tools import execute_sql
from ai_data_analyst.schema import DATABASE_SCHEMA


SYSTEM_PROMPT = f"""
You are an expert Data Analyst.

Your job is to answer business questions using
the PostgreSQL analytics database.

Database schema:

{DATABASE_SCHEMA}

Rules:

- Use the execute_sql tool when database information is required.
- Only generate SELECT queries.
- Never modify the database.
- Never invent tables or columns.
- Use the correct table relationships.
- Revenue is calculated as:
  quantity * unit_price * (1 - discount)
- Give concise, business-friendly answers.
"""


llm_with_tools = llm.bind_tools(
    [execute_sql]
)


def run_agent(question: str) -> str:
    """Run the data analyst agent."""

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=question),
    ]

    # Ask the LLM
    response = llm_with_tools.invoke(messages)

    # If the LLM wants to use a tool
    if response.tool_calls:

        messages.append(response)

        for tool_call in response.tool_calls:

            if tool_call["name"] == "execute_sql":

                result = execute_sql.invoke(
                    tool_call["args"]
                )

                messages.append(
                    ToolMessage(
                        content=str(result),
                        tool_call_id=tool_call["id"],
                    )
                )

        # Ask the LLM to interpret the tool result
        final_response = llm_with_tools.invoke(messages)

        return final_response.content

    # No tool required
    return response.content