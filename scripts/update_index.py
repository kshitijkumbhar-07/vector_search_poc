from google.cloud import aiplatform

from app.config import (
    GCP_PROJECT_ID,
    GOOGLE_CLOUD_LOCATION,
    VECTOR_SEARCH_INDEX_ID,
    VECTOR_SEARCH_BUCKET,
    VECTOR_SEARCH_GCS_PATH,
)


def main() -> None:

    gcs_uri = (
        f"gs://{VECTOR_SEARCH_BUCKET}/"
        f"{VECTOR_SEARCH_GCS_PATH}"
    )

    print("=" * 60)
    print("UPDATING VECTOR SEARCH INDEX")
    print("=" * 60)

    aiplatform.init(
        project=GCP_PROJECT_ID,
        location=GOOGLE_CLOUD_LOCATION,
    )

    index = aiplatform.MatchingEngineIndex(
        index_name=VECTOR_SEARCH_INDEX_ID
    )

    print(f"Index: {VECTOR_SEARCH_INDEX_ID}")
    print(f"GCS:   {gcs_uri}")

    operation = index.update_embeddings(
    contents_delta_uri=gcs_uri,
    is_complete_overwrite=True,
)

    print()
    operation = index.update_embeddings(
        contents_delta_uri=gcs_uri,
        is_complete_overwrite=True,
    )

    print()
    print("Successfully updated vector search index:")
    print(operation.resource_name)


if __name__ == "__main__":
    main()