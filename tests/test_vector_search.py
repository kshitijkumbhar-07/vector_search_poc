from app.embeddings import generate_embedding
from app.vector_search import search_vector


def main() -> None:
    query = "What is a Kubernetes Pod?"

    print("=" * 60)
    print("VECTOR SEARCH TEST")
    print("=" * 60)

    print(f"\nQuery: {query}")

    print("\nGenerating query embedding...")
    embedding = generate_embedding(query)

    print(f"Embedding dimensions: {len(embedding)}")

    print("\nSearching Vector Search...")
    results = search_vector(embedding, top_k=3)

    print(f"\nFound {len(results)} results\n")

    for i, result in enumerate(results, start=1):
        print(f"Result {i}")
        print(f"ID: {result.id}")
        print(f"Distance: {result.distance}")
        print("-" * 40)


if __name__ == "__main__":
    main()