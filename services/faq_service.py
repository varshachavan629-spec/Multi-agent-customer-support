import pandas as pd
import os


def search_faq(agent, question):

    file_path = f"knowledge/{agent.lower()}.csv"

    if not os.path.exists(file_path):
        return None

    df = pd.read_csv(file_path)

    question = question.lower().strip()

    best_answer = None
    best_score = 0


    for _, row in df.iterrows():

        faq_question = str(row["question"]).lower().strip()

        score = 0


        # Exact phrase match (highest priority)
        if faq_question in question or question in faq_question:
            return row["answer"]


        # Word matching
        question_words = set(question.split())
        faq_words = set(faq_question.split())


        common_words = question_words.intersection(faq_words)


        # Ignore common words
        ignored_words = {
            "i",
            "my",
            "the",
            "a",
            "an",
            "is",
            "was",
            "for",
            "to",
            "of"
        }


        useful_words = [
            word for word in common_words
            if word not in ignored_words
        ]


        score = len(useful_words)


        if score > best_score:
            best_score = score
            best_answer = row["answer"]


    # Only return FAQ when confidence is good
    if best_score >= 2:
        return best_answer


    # No FAQ match -> LLM will handle
    return None