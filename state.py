from typing import TypedDict


class CustomerState(TypedDict):
    user_message: str
    session_id: str
    agent: str
    response: str