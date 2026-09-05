from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
    ToolMessage,
)

from ai_data_analyst.agents import llm_with_tools, SYSTEM_PROMPT
from ai_data_analyst.tools import execute_sql


messages = [
    SystemMessage(content=SYSTEM_PROMPT),
    HumanMessage(
        content="What are the number of customers?"
    ),
]


# Step 1: Ask the LLM
response = llm_with_tools.invoke(messages)

print("LLM RESPONSE:")
print(response)


# Step 2: Check whether the LLM requested a tool
if response.tool_calls:

    # Add the LLM response to the conversation
    messages.append(response)

    # Step 3: Execute each requested tool
    for tool_call in response.tool_calls:

        if tool_call["name"] == "execute_sql":

            result = execute_sql.invoke(
                tool_call["args"]
            )

            print("\nTOOL RESULT:")
            print(result)

            # Step 4: Send the tool result back to the LLM
            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"],
                )
            )


    # Step 5: Ask the LLM to produce the final answer
    # print(messages)
    final_response = llm_with_tools.invoke(messages)

    print("\nFINAL ANSWER:")
    print(final_response.content)

else:

    print("\nFINAL ANSWER:")
    print(response.content)