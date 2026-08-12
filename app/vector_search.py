from google.cloud import aiplatform

from app.config import (
    GCP_PROJECT_ID,
    GOOGLE_CLOUD_LOCATION,
    VECTOR_SEARCH_INDEX_ENDPOINT_ID,
    DEPLOYED_INDEX_ID,
    TOP_K,
)


# ---------------------------------------------------------
# Vertex AI initialization
# ---------------------------------------------------------

aiplatform.init(
    project=GCP_PROJECT_ID,
    location=GOOGLE_CLOUD_LOCATION,
)


# ---------------------------------------------------------
# Vector Search Endpoint
# ---------------------------------------------------------

INDEX_ENDPOINT_NAME = (
    f"projects/{GCP_PROJECT_ID}/locations/"
    f"{GOOGLE_CLOUD_LOCATION}/indexEndpoints/"
    f"{VECTOR_SEARCH_INDEX_ENDPOINT_ID}"
)


index_endpoint = aiplatform.MatchingEngineIndexEndpoint(
    index_endpoint_name=INDEX_ENDPOINT_NAME
)


# ---------------------------------------------------------
# Vector Search
# ---------------------------------------------------------

def search_vector(
    query_embedding: list[float],
    top_k: int | None = None,
):
    """
    Search Vertex AI Vector Search using a query embedding.

    Parameters:
        query_embedding:
            768-dimensional embedding vector.

        top_k:
            Number of nearest documents to return.
            Uses TOP_K from configuration if not provided.

    Returns:
        List of Vector Search nearest-neighbor results.
    """

    # Validate embedding dimension
    if len(query_embedding) != 768:
        raise ValueError(
            f"Expected 768-dimensional vector, "
            f"got {len(query_embedding)}"
        )

    # Number of results
    num_neighbors = top_k or TOP_K

    print(
        f"Searching Vector Search "
        f"(top_k={num_neighbors})..."
    )

    # Query deployed Vector Search index
    neighbors = index_endpoint.find_neighbors(
        deployed_index_id=DEPLOYED_INDEX_ID,
        queries=[query_embedding],
        num_neighbors=num_neighbors,
    )

    if not neighbors:
        return []

    return neighbors[0]