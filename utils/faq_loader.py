import csv


def load_faq(csv_file):
    """
    Loads FAQs from a CSV file.
    """

    faqs = []

    with open(csv_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            faqs.append(row)

    return faqs


def search_faq(user_message, csv_file):
    """
    Searches the FAQ CSV.
    Returns the answer if found, otherwise None.
    """

    faqs = load_faq(csv_file)

    user_message = user_message.lower()

    for faq in faqs:

        question = faq["question"].lower()

        if question in user_message:
            return faq["answer"]

    return None