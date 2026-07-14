from langgraph.graph import StateGraph, END

from state import CustomerState
from router import route_query


def router_node(state: CustomerState):
    """
    Routes the user query to the correct AI agent.
    """

    agent, response = route_query(
        state["user_message"],
        state["session_id"]
    )

    return {
        "user_message": state["user_message"],
        "session_id": state["session_id"],
        "agent": agent,
        "response": response
    }


# Create the graph
workflow = StateGraph(CustomerState)

# Add the router node
workflow.add_node("router", router_node)

# Set the entry point
workflow.set_entry_point("router")

# End after the router finishes
workflow.add_edge("router", END)

# Compile the graph
graph = workflow.compile()