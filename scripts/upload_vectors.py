from pathlib import Path

from google.cloud import storage

from app.config import (
    GCP_PROJECT_ID,
    VECTOR_SEARCH_BUCKET,
    VECTOR_SEARCH_GCS_PATH,
)


ROOT = Path(__file__).resolve().parents[1]

EMBEDDINGS_FILE = ROOT / "data" / "embeddings.json"


def main() -> None:

    if not EMBEDDINGS_FILE.exists():
        raise FileNotFoundError(
            f"Missing {EMBEDDINGS_FILE}. "
            "Run create_embeddings.py first."
        )

    client = storage.Client(project=GCP_PROJECT_ID)

    bucket = client.bucket(VECTOR_SEARCH_BUCKET)

    blob_name = (
        f"{VECTOR_SEARCH_GCS_PATH}/embeddings.json"
    )

    blob = bucket.blob(blob_name)

    blob.upload_from_filename(
        EMBEDDINGS_FILE,
        content_type="application/json",
    )

    gcs_uri = (
        f"gs://{VECTOR_SEARCH_BUCKET}/"
        f"{VECTOR_SEARCH_GCS_PATH}"
    )

    print("=" * 60)
    print("VECTOR DATA UPLOADED")
    print("=" * 60)
    print(f"GCS URI: {gcs_uri}")


if __name__ == "__main__":
    main()