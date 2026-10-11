import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

KNOWLEDGE_BASE_PATH = "knowledge_base"
OUTPUT_FILE = "knowledge_base/embeddings.json"


def load_documents():
    documents = []

    for filename in os.listdir(KNOWLEDGE_BASE_PATH):

        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(KNOWLEDGE_BASE_PATH, filename)

        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        documents.append({
            "source": filename,
            "content": content
        })

    return documents


def create_embeddings():

    documents = load_documents()

    texts = [document["content"] for document in documents]

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )

    for document, embedding_data in zip(
        documents,
        response.data
    ):
        document["embedding"] = embedding_data.embedding

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(documents, file)

    print(f"Created embeddings for {len(documents)} documents.")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    create_embeddings()