import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="gpt-5-mini",
    temperature=0,
)


def ask_llm(prompt: str) -> str:
    """Send a prompt to the LLM and return its response."""
    response = llm.invoke(prompt)
    return response.content