last_agent = {}


def set_last_agent(session_id, agent):
    last_agent[session_id] = agent


def get_last_agent(session_id):
    return last_agent.get(session_id)