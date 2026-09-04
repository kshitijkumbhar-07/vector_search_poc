from google.cloud import aiplatform

from app.config import (
    GCP_PROJECT_ID,
    GOOGLE_CLOUD_LOCATION,
    VECTOR_SEARCH_INDEX_ID,
    VECTOR_SEARCH_ENDPOINT_ID,
)



NEW_DEPLOYED_INDEX_ID = "adk_vector_poc"


def main() -> None:

    print("=" * 60)
    print("DEPLOYING VECTOR SEARCH INDEX")
    print("=" * 60)

    print(f"Project  : {GCP_PROJECT_ID}")
    print(f"Location : {GOOGLE_CLOUD_LOCATION}")
    print(f"Index    : {VECTOR_SEARCH_INDEX_ID}")
    print(f"Endpoint : {VECTOR_SEARCH_ENDPOINT_ID}")
    print(f"Deploy ID: {NEW_DEPLOYED_INDEX_ID}")

    aiplatform.init(
        project=GCP_PROJECT_ID,
        location=GOOGLE_CLOUD_LOCATION,
    )

    # Load the newly created Vector Search index
    index = aiplatform.MatchingEngineIndex(
        index_name=VECTOR_SEARCH_INDEX_ID
    )

    # Load the existing Vector Search endpoint
    endpoint = aiplatform.MatchingEngineIndexEndpoint(
        index_endpoint_name=VECTOR_SEARCH_ENDPOINT_ID
    )

    print()
    print("Deploying index to endpoint...")
    print("This may take some time.")

    endpoint.deploy_index(
        index=index,
        deployed_index_id=NEW_DEPLOYED_INDEX_ID,
        display_name="adk_vector_poc",
        min_replica_count=1,
        max_replica_count=1,
    )

    print()
    print("=" * 60)
    print("VECTOR SEARCH INDEX DEPLOYED")
    print("=" * 60)
    print(f"Endpoint : {VECTOR_SEARCH_ENDPOINT_ID}")
    print(f"Deploy ID: {NEW_DEPLOYED_INDEX_ID}")
    print()
    print("Verify with:")
    print(
        "gcloud ai index-endpoints list "
        f"--region={GOOGLE_CLOUD_LOCATION} "
        f"--project={GCP_PROJECT_ID}"
    )


if __name__ == "__main__":
    main()