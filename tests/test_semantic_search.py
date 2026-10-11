from tools.semantic_search import search_knowledge_base

questions = [
    "How many days do I have to return a product?",
    "How long does shipping take?",
    "What does the warranty cover?",
    "How long does a refund take?"
]

for question in questions:

    print("\nQuestion:", question)

    result = search_knowledge_base(question)

    print("Result:")
    print(result)