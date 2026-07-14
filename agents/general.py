from services.llm_service import get_llm
from services.faq_service import search_faq
from prompts import GENERAL_PROMPT
from memory import get_chat_history, get_last_issue, save_message

llm = get_llm()


def general_agent(state):
    """
    Handles general customer support queries.
    """

    user_message = state["user_message"]
    session_id = state["session_id"]

    message = user_message.lower().strip()

    history = get_chat_history(
        session_id,
        limit=5
    )

    last_issue = get_last_issue(session_id)


    # =====================================
    # MEMORY QUESTIONS
    # =====================================

    memory_questions = [
        "what was my issue",
        "what was the issue",
        "what did i say",
        "continue",
        "remind me",
        "what was my previous issue"
    ]


    if message in memory_questions:

        if last_issue:
            response = f"Your previous issue was: {last_issue}"
        else:
            response = "I couldn't find any previous issue in this conversation."


        save_message(
            session_id=session_id,
            user_message=user_message,
            agent="General",
            bot_response=response
        )


        return {
            "user_message": user_message,
            "session_id": session_id,
            "agent": "General",
            "response": response
        }



    # =====================================
    # FAQ SEARCH FIRST
    # =====================================

    faq_response = search_faq(
        "general",
        user_message
    )


    if faq_response:

        save_message(
            session_id=session_id,
            user_message=user_message,
            agent="General",
            bot_response=faq_response
        )


        return {
            "user_message": user_message,
            "session_id": session_id,
            "agent": "General",
            "response": faq_response
        }



    # =====================================
    # LLM FALLBACK ONLY IF FAQ NOT FOUND
    # =====================================

    prompt = f"""
{GENERAL_PROMPT}

Previous conversation:
{history}

Current user question:
{user_message}

Instructions:
- You are a General Customer Support Agent.
- Answer the current question.
- Use previous messages only as context.
- Do not invent customer information.
- Keep responses short, clear, and professional.
"""


    response = llm.invoke(prompt).content


    save_message(
        session_id=session_id,
        user_message=user_message,
        agent="General",
        bot_response=response
    )


    return {
        "user_message": user_message,
        "session_id": session_id,
        "agent": "General",
        "response": response
    }