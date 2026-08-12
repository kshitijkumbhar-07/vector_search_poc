from app.embeddings import generate_embedding


def test_embedding_dimension():
    vector = generate_embedding(
        "A Kubernetes Pod is the smallest deployable unit."
    )

    assert len(vector) == 768

    print("Embedding dimension test: PASSED")
    print(f"Embedding dimensions: {len(vector)}")