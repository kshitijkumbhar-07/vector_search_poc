import os
from pathlib import Path

from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]

load_dotenv(ROOT / ".env")


def required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")

    return value


GCP_PROJECT_ID = required_env("GCP_PROJECT_ID")
GOOGLE_CLOUD_LOCATION = required_env("GOOGLE_CLOUD_LOCATION")

EMBEDDING_MODEL = required_env("EMBEDDING_MODEL")
EMBEDDING_DIMENSIONS = int(required_env("EMBEDDING_DIMENSIONS"))

VECTOR_SEARCH_INDEX_ID = required_env("VECTOR_SEARCH_INDEX_ID")
VECTOR_SEARCH_INDEX_ENDPOINT_ID = required_env(
    "VECTOR_SEARCH_INDEX_ENDPOINT_ID"
)
DEPLOYED_INDEX_ID = required_env("DEPLOYED_INDEX_ID")

VECTOR_SEARCH_BUCKET = required_env("VECTOR_SEARCH_BUCKET")
VECTOR_SEARCH_GCS_PATH = required_env("VECTOR_SEARCH_GCS_PATH")

TOP_K = int(required_env("TOP_K"))

GEMINI_MODEL = required_env("GEMINI_MODEL")