from agents.general import general_agent
from agents.billing import billing_agent
from agents.technical import technical_agent
from agents.account import account_agent
from agents.escalation import escalation_agent
from agents.triage import classify_query

from session_memory import set_last_agent, get_last_agent


def route_query(user_message, session_id):
    """
    Routes the user query using the AI Triage Agent.
    """

    message = user_message.lower().strip()

    state = {
        "user_message": user_message,
        "session_id": session_id
    }


    # -----------------------------------
    # Follow-up Questions
    # -----------------------------------

    follow_up = [
        "what was my issue",
        "what was the issue",
        "what did i say",
        "continue",
        "remind me",
        "what was my previous issue"
    ]


    if message in follow_up:

        last = get_last_agent(session_id)


        if last == "Billing":
            result = billing_agent(state)

        elif last == "Technical":
            result = technical_agent(state)

        elif last == "Account":
            result = account_agent(state)

        elif last == "Escalation":
            result = escalation_agent(state)

        else:
            result = general_agent(state)


        return result["agent"], result["response"]



    # -----------------------------------
    # AI TRIAGE AGENT
    # -----------------------------------

    classification = classify_query(user_message)

    category = classification.get(
        "category",
        "General"
    )

    print(f"Selected Agent: {category}")


    if category == "Billing":

        result = billing_agent(state)


    elif category == "Technical":

        result = technical_agent(state)


    elif category == "Account":

        result = account_agent(state)


    elif category == "Escalation":

        result = escalation_agent(state)


    else:

        result = general_agent(state)



    # Remember agent
    set_last_agent(
        session_id,
        result["agent"]
    )


    return result["agent"], result["response"]