from graph import graph


def process_chat(user_message, session_id):
    """
    Process a customer message using the LangGraph workflow.
    """

    # Initial state passed to LangGraph
    state = {
        "user_message": user_message,
        "session_id": session_id
    }

    # Execute the graph
    result = graph.invoke(state)

    # Conversations are already saved by the agents via memory.save_message()
    # So we only return the result here.

    return {
        "agent": result["agent"],
        "response": result["response"]
    }