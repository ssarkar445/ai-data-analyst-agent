import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

client = ChatOpenAI(model="gpt-5.4-mini", stream_usage=True,temperature=2)


def ask_llm(prompt: str) -> str:
    """Send a prompt to the LLM and return its response."""
    response = client.invoke(prompt)
    return response.content