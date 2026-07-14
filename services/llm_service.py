from langchain_groq import ChatGroq
from config import Config


# Create one shared LLM instance
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=Config.GROQ_API_KEY,
    temperature=0
)


def get_llm():
    """
    Returns the shared Groq LLM.
    """
    return llm