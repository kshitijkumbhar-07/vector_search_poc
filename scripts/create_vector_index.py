from google.cloud import aiplatform

from app.config import (
    GCP_PROJECT_ID,
    GOOGLE_CLOUD_LOCATION,
    VECTOR_SEARCH_BUCKET,
    VECTOR_SEARCH_GCS_PATH,
    EMBEDDING_DIMENSIONS,
)


def main() -> None:
    print("=" * 60)
    print("CREATING VECTOR SEARCH INDEX")
    print("=" * 60)

    aiplatform.init(
        project=GCP_PROJECT_ID,
        location=GOOGLE_CLOUD_LOCATION,
    )

    contents_delta_uri = (
        f"gs://{VECTOR_SEARCH_BUCKET}/{VECTOR_SEARCH_GCS_PATH}"
    )

    print(f"Project   : {GCP_PROJECT_ID}")
    print(f"Location  : {GOOGLE_CLOUD_LOCATION}")
    print(f"Vector URI: {contents_delta_uri}")

    index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
        display_name="adk-vector-poc-index-local",

        # IMPORTANT:
        # This is the DIRECTORY, not embeddings.jsonl
        contents_delta_uri=contents_delta_uri,

        dimensions=EMBEDDING_DIMENSIONS,
        approximate_neighbors_count=10,
        distance_measure_type="COSINE_DISTANCE",
        leaf_node_embedding_count=500,
        leaf_nodes_to_search_percent=10,

        description="Google ADK Vector Search POC",
        index_update_method="BATCH_UPDATE",
    )

    print("\n" + "=" * 60)
    print("VECTOR SEARCH INDEX CREATED")
    print("=" * 60)

    print(f"Index name: {index.resource_name}")


if __name__ == "__main__":
    main()