from services.llm_service import get_llm
from prompts import ESCALATION_PROMPT
from memory import get_chat_history, get_last_issue, save_message

llm = get_llm()


def escalation_agent(state):
    """
    Handles escalation requests.
    """

    user_message = state["user_message"]
    session_id = state["session_id"]

    message = user_message.lower().strip()

    history = get_chat_history(session_id, limit=5)
    last_issue = get_last_issue(session_id)

    # =====================================
    # MEMORY QUESTIONS
    # =====================================

    if message in [
        "what was my issue",
        "what was the issue",
        "what did i say",
        "continue",
        "remind me",
        "what was my previous issue"
    ]:

        if last_issue:
            response = f"Your previous issue was: {last_issue}"
        else:
            response = "I couldn't find any previous issue in this conversation."

        save_message(
            session_id=session_id,
            user_message=user_message,
            agent="Escalation",
            bot_response=response
        )

        return {
            "user_message": user_message,
            "session_id": session_id,
            "agent": "Escalation",
            "response": response
        }

    # =====================================
    # LLM FALLBACK
    # =====================================

    prompt = f"""
{ESCALATION_PROMPT}

Previous Customer Messages:
{history}

Current Customer Message:
{user_message}

Instructions:

- You are an AI Escalation Support Agent.
- Use the previous customer messages only as context.
- Summarize the customer's issue briefly.
- If the issue is still unresolved, politely inform the customer that it needs human assistance.
- Ask the customer to visit the Contact Us page and submit the support form.
- Explain that submitting the Contact Us form will automatically create a support ticket.
- Inform the customer that a Ticket ID will be generated after the form is submitted.
- Do NOT ask the customer for a Ticket ID before they have created one.
- Ask for an email address or contact number only if it is needed.
- Do not promise refunds or solutions.
- Keep the response short, professional, and empathetic.

Example Response:

"I'm sorry that your issue is still not resolved.

Please visit the Contact Us page and submit your issue.

Once you submit the form, our system will automatically create a support ticket and provide you with a Ticket ID.

Our human support team will review your request and contact you as soon as possible."
"""

    response = llm.invoke(prompt).content

    save_message(
        session_id=session_id,
        user_message=user_message,
        agent="Escalation",
        bot_response=response
    )

    return {
        "user_message": user_message,
        "session_id": session_id,
        "agent": "Escalation",
        "response": response
    }