import json

from services.llm_service import get_llm

llm = get_llm()


def classify_query(user_message):
    """
    Classifies the customer query into one category.
    Returns a Python dictionary.
    """

    prompt = f"""
You are an AI Triage Agent.

Your task is to classify the customer's message into exactly ONE category.

Categories:
- Billing
- Technical
- Account
- General
- Escalation

Return ONLY valid JSON in this format:

{{
    "category": "Billing"
}}

Customer Message:
{user_message}
"""

    response = llm.invoke(prompt).content.strip()

    try:
        result = json.loads(response)

        valid = [
            "Billing",
            "Technical",
            "Account",
            "General",
            "Escalation"
        ]

        if result["category"] not in valid:
            result["category"] = "General"

        return result

    except Exception:
        return {
            "category": "General"
        }