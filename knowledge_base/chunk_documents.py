import os
import json

KNOWLEDGE_BASE_PATH = "knowledge_base"
OUTPUT_FILE = "knowledge_base/chunks.json"

CHUNK_SIZE = 60
CHUNK_OVERLAP = 10


def create_chunks(text, chunk_size=60, overlap=10):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk_words = words[start:end]

        chunk = " ".join(chunk_words)

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def load_and_chunk_documents():

    all_chunks = []

    for filename in os.listdir(KNOWLEDGE_BASE_PATH):

        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(
            KNOWLEDGE_BASE_PATH,
            filename
        )

        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        chunks = create_chunks(content)

        for index, chunk in enumerate(chunks):

            all_chunks.append({
                "source": filename,
                "chunk_id": index,
                "content": chunk
            })

    return all_chunks


def save_chunks():

    chunks = load_and_chunk_documents()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(chunks, file, indent=2)

    print(f"Created {len(chunks)} chunks.")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    save_chunks()