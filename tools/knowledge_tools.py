import json
import numpy as np

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

EMBEDDINGS_FILE = "knowledge_base/chunk_embeddings.json"


def cosine_similarity(vector_a, vector_b):

    vector_a = np.array(vector_a)
    vector_b = np.array(vector_b)

    return np.dot(vector_a, vector_b) / (
        np.linalg.norm(vector_a) *
        np.linalg.norm(vector_b)
    )


def search_knowledge_base(query):

    # Load chunk embeddings
    with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    # Convert user's question into an embedding
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )

    query_embedding = response.data[0].embedding

    results = []

    # Compare query with every chunk
    for chunk in chunks:

        similarity = cosine_similarity(
            query_embedding,
            chunk["embedding"]
        )

        results.append({
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"],
            "content": chunk["content"],
            "similarity": float(similarity)
        })

    # Highest similarity first
    results.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    # Return top 2 relevant chunks
    return results[:2]