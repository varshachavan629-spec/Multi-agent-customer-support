from services.faq_service import search_faq
from services.llm_service import llm
from memory import get_chat_history, get_last_issue, save_message


def billing_agent(state):

    user_message = state["user_message"]
    session_id = state["session_id"]


    # -----------------------------------
    # MEMORY QUESTIONS
    # -----------------------------------

    message = user_message.lower().strip()

    if message in [
        "what was my issue",
        "what was the issue",
        "what did i say",
        "continue",
        "remind me",
        "what was my previous issue"
    ]:

        last_issue = get_last_issue(session_id)

        if last_issue:
            response = f"Your previous issue was: {last_issue}"
        else:
            response = "I couldn't find any previous issue in this conversation."


        save_message(
            session_id=session_id,
            user_message=user_message,
            agent="Billing",
            bot_response=response
        )


        return {
            "agent": "Billing",
            "response": response
        }


    # -----------------------------------
    # STEP 1: SEARCH FAQ
    # -----------------------------------

    faq_answer = search_faq(
        "billing",
        user_message
    )


    # -----------------------------------
    # STEP 2: FAQ FOUND
    # -----------------------------------

    if faq_answer:

        save_message(
            session_id=session_id,
            user_message=user_message,
            agent="Billing",
            bot_response=faq_answer
        )

        return {
            "agent": "Billing",
            "response": faq_answer
        }


    # -----------------------------------
    # STEP 3: FAQ NOT FOUND → LLM
    # -----------------------------------

    history = get_chat_history(
        session_id,
        limit=5
    )


    prompt = f"""
You are a professional Billing Support Agent.

Previous conversation:
{history}

Current customer question:
{user_message}

Rules:
- Give a short and clear answer.
- Help with payments, refunds, subscriptions, and invoices.
- Do not ask for passwords, OTPs, or bank details.
- Ask only for safe details like transaction ID, payment method, date, or error message if required.
"""


    response = llm.invoke(prompt).content


    save_message(
        session_id=session_id,
        user_message=user_message,
        agent="Billing",
        bot_response=response
    )


    return {
        "agent": "Billing",
        "response": response
    }