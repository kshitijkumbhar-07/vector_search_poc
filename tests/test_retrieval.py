from app.tools import retrieve_documents


def main() -> None:
    query = "What is a Kubernetes Pod?"

    print("=" * 60)
    print("RETRIEVAL TEST")
    print("=" * 60)

    print(f"\nQuery: {query}\n")

    results = retrieve_documents(
        query,
        top_k=3,
    )

    print(f"Retrieved {len(results)} documents\n")

    for i, result in enumerate(results, start=1):
        print(f"Result {i}")
        print(f"ID: {result['id']}")
        print(f"Distance: {result['distance']}")
        print(f"Content: {result['content']}")
        print("-" * 60)


if __name__ == "__main__":
    main()