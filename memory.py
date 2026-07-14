from datetime import datetime
from database import get_last_conversations, save_conversation


def get_chat_history(session_id, limit=5):
    """
    Returns previous user messages for the current session.
    """

    conversations = get_last_conversations(session_id, limit)

    history = ""

    for (user_message,) in conversations:
        history += f"- {user_message}\n"

    return history.strip()

def get_last_issue(session_id):
    """
    Returns the latest user issue from the current session.
    """

    conversations = get_last_conversations(session_id, limit=10)

    ignore = [
        "what was my issue",
        "what was the issue",
        "what did i say",
        "remind me",
        "what was my previous issue"
    ]

    for (message,) in reversed(conversations):

        message = message.strip()

        if message.lower() not in ignore:
            return message

    return None


def save_message(
    session_id,
    user_message,
    agent,
    bot_response,
    status="Completed"
):
    """
    Saves conversation into the database.
    """

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    save_conversation(
        session_id=session_id,
        user_message=user_message,
        agent=agent,
        bot_response=bot_response,
        status=status,
        timestamp=timestamp
    )