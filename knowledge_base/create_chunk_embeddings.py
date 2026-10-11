import os
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

CHUNKS_FILE = "knowledge_base/chunks.json"
OUTPUT_FILE = "knowledge_base/chunk_embeddings.json"


def create_chunk_embeddings():

    # Load chunks
    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    # Extract chunk text
    texts = [chunk["content"] for chunk in chunks]

    # Create embeddings
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )

    # Attach embedding to each chunk
    for chunk, embedding_data in zip(chunks, response.data):
        chunk["embedding"] = embedding_data.embedding

    # Save
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(chunks, file)

    print(f"Created embeddings for {len(chunks)} chunks.")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    create_chunk_embeddings()