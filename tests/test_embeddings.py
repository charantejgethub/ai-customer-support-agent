import json

with open("knowledge_base/embeddings.json", "r", encoding="utf-8") as file:
    documents = json.load(file)

for document in documents:
    print(document["source"])