from google.cloud import aiplatform

from app.config import (
    GCP_PROJECT_ID,
    GOOGLE_CLOUD_LOCATION,
    VECTOR_SEARCH_BUCKET,
    VECTOR_SEARCH_GCS_PATH,
    EMBEDDING_DIMENSIONS,
)


def main() -> None:
  
    aiplatform.init(
        project=GCP_PROJECT_ID,
        location=GOOGLE_CLOUD_LOCATION,
    )

    contents_delta_uri = (
        f"gs://{VECTOR_SEARCH_BUCKET}/{VECTOR_SEARCH_GCS_PATH}"
    )

    print("=" * 60)
    print("CREATING VERTEX AI VECTOR SEARCH INDEX")
    print("=" * 60)

    print(f"Project       : {GCP_PROJECT_ID}")
    print(f"Region        : {GOOGLE_CLOUD_LOCATION}")
    print(f"GCS directory : {contents_delta_uri}")
    print(f"Dimensions    : {EMBEDDING_DIMENSIONS}")
    print("Algorithm     : tree-AH")
    print("Distance      : COSINE_DISTANCE")
    print("Update method : BATCH_UPDATE")
    print("Shard size    : SHARD_SIZE_SMALL")
    print("=" * 60)

    index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
        display_name="adk-vector-poc-index-local",

        description="Google ADK Vector Search POC",


        contents_delta_uri=contents_delta_uri,
        dimensions=EMBEDDING_DIMENSIONS,

       
        
        # Number of approximate candidates considered before
       
        approximate_neighbors_count=3,

        # Number of embeddings stored in each leaf node.
        leaf_node_embedding_count=5,

        # Percentage of leaf nodes searched for each query.
       
        leaf_nodes_to_search_percent=10,

        
        distance_measure_type="COSINE_DISTANCE",
        index_update_method="BATCH_UPDATE",

        shard_size="SHARD_SIZE_SMALL",
    )

    print()
    print("=" * 60)
    print("VECTOR SEARCH INDEX CREATED")
    print("=" * 60)

    print(f"Display name : {index.display_name}")
    print(f"Resource name: {index.resource_name}")
    print(f"Index ID     : {index.name.split('/')[-1]}")
    print("=" * 60)


if __name__ == "__main__":
    main()