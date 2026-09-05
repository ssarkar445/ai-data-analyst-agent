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
- After receiving a successful execute_sql result, determine whether
  the user's question has been answered.
- If the result is sufficient, do not call execute_sql again.
- Do not repeat the same SQL query unless there is a clear reason.
- Always provide a final answer when the available database results
  are sufficient.
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

    for _ in range(5):

        # Ask the LLM what to do
        response = llm_with_tools.invoke(messages)

        # Add LLM response to conversation history
        messages.append(response)

        # No tool call means we have the final answer
        if not response.tool_calls:
            return response.content

        # Execute requested tools
        for tool_call in response.tool_calls:

            if tool_call["name"] == "execute_sql":

                result = execute_sql.invoke(
                    tool_call["args"]
                )

                print("\nSQL RESULT:")
                print(result)

                messages.append(
                    ToolMessage(
                        content=str(result),
                        tool_call_id=tool_call["id"],
                    )
                )

    return "I was unable to complete the analysis within the allowed steps."