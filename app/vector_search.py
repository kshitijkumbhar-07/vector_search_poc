from google.cloud import aiplatform
from app.config import (
    GCP_PROJECT_ID,
    GOOGLE_CLOUD_LOCATION,
    VECTOR_SEARCH_INDEX_ENDPOINT_ID,
    DEPLOYED_INDEX_ID,
    TOP_K,
)

def create_endpoint() -> aiplatform.MatchingEngineIndexEndpoint:
    return aiplatform.MatchingEngineIndexEndpoint(
        index_endpoint_name=(
            f"projects/{GCP_PROJECT_ID}"
            f"/locations/{GOOGLE_CLOUD_LOCATION}"
            f"/indexEndpoints/"
            f"{VECTOR_SEARCH_INDEX_ENDPOINT_ID}"
        )
    )

def search_vector(
    query_embedding: list[float],
    top_k: int | None = None,
    category: str | None = None,
    subcategory: str | None = None,
    language: str | None = None,
):
    endpoint = create_endpoint()
    filters = []

    if category:
        filters.append(
            aiplatform.matching_engine.matching_engine_index_endpoint.Namespace(
                name="category",
                allow_tokens=[category],
            )
        )

    if subcategory:
        filters.append(
            aiplatform.matching_engine.matching_engine_index_endpoint.Namespace(
                name="subcategory",
                allow_tokens=[subcategory],
            )
        )

    if language:
        filters.append(
            aiplatform.matching_engine.matching_engine_index_endpoint.Namespace(
                name="language",
                allow_tokens=[language],
            )
        )

    print("\n--- [Vertex AI Vector Search Query] ---")
    if filters:
        print("Applied Metadata Filters:")
        for f in filters:
            print(f"  • {f.name}: {f.allow_tokens}")
    else:
        print("Applied Metadata Filters: None (Unfiltered Search)")

    response = endpoint.find_neighbors(
        deployed_index_id=DEPLOYED_INDEX_ID,
        queries=[query_embedding],
        num_neighbors=top_k or TOP_K,
        filter=filters or None,
    )
    

    results = response[0] if response else []
    print(f"Matches Found: {len(results)}\n----------------------------------------\n")
    

    # Print vector distance for every match
    for idx, neighbor in enumerate(results, start=1):
        print(f"  [{idx}] Match ID: {neighbor.id:<15} | Distance: {neighbor.distance:.4f}")

    print("----------------------------------------\n")
    
    return results