import csv
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

embedding_function = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(path="db")


FAQ_FILES = {
    "billing_faq": "knowledge/billing.csv",
    "technical_faq": "knowledge/technical.csv",
    "account_faq": "knowledge/account.csv",
    "general_faq": "knowledge/general.csv"
}


def build_collection(collection_name, csv_file):

    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_function
    )

    # Clear old data (optional)
    try:
        existing = collection.get()["ids"]
        if existing:
            collection.delete(ids=existing)
    except:
        pass

    with open(csv_file, "r", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for index, row in enumerate(reader):

            collection.add(
                ids=[str(index)],
                documents=[row["question"]],
                metadatas=[
                    {
                        "answer": row["answer"]
                    }
                ]
            )

    print(f"✅ {collection_name} created")


def build_database():

    for collection_name, csv_file in FAQ_FILES.items():
        build_collection(collection_name, csv_file)


if __name__ == "__main__":
    build_database()
    