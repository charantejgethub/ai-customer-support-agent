import json

with open("knowledge_base/chunks.json", "r", encoding="utf-8") as file:
    data = json.load(file)

print("Total chunks:", len(data))

for chunk in data:
    print("\nChunk:", chunk["chunk_id"])
    print("Source:", chunk["source"])
    print("Content:")
    print(chunk["content"])
    print("-" * 50)