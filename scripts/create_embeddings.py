import json
import logging
from pathlib import Path
from typing import Any, Dict, List

from google import genai
from google.genai import types

from app.config import (
    EMBEDDING_DIMENSIONS,
    EMBEDDING_MODEL,
    GCP_PROJECT_ID,
    GOOGLE_CLOUD_LOCATION,
)

# File Paths
INPUT_FILE = Path("data/documents.json")
OUTPUT_FILE = Path("data/embeddings.json")


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

client = genai.Client(
    vertexai=True,
    project=GCP_PROJECT_ID,
    location=GOOGLE_CLOUD_LOCATION,
)


def generate_embedding(text: str) -> List[float]:
    """Generates a text embedding vector using the Google GenAI SDK.

    Args:
        text: Input string document content to embed.

    Returns:
        List[float]: Vector values as floating-point numbers.
    """
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            output_dimensionality=EMBEDDING_DIMENSIONS,
            task_type="RETRIEVAL_DOCUMENT",
        ),
    )

    vector = response.embeddings[0].values

    if len(vector) != EMBEDDING_DIMENSIONS:
        raise RuntimeError(
            f"Expected {EMBEDDING_DIMENSIONS} dimensions, got {len(vector)}."
        )

    return list(vector)


def build_vector_search_datapoint(doc: Dict[str, Any], embedding: List[float]) -> Dict[str, Any]:
    """Constructs a Vertex AI Vector Search compliant JSON datapoint schema."""
    document_id = doc["document_id"]

    return {
        "id": f"{document_id}",
        "embedding": embedding,

        "restricts": [
            {"namespace": "category", "allow": [doc["category"]]},
            {"namespace": "subcategory", "allow": [doc["subcategory"]]},
            {"namespace": "language", "allow": [doc["language"]]},
            {"namespace": "source", "allow": [doc["source"]]},
            {"namespace": "source_type", "allow": [doc["source_type"]]},
        ],

        
        "numeric_restricts": [
            {"namespace": "version", "value_int": doc["version"]},
            {"namespace": "page", "value_int": doc["page"]},
        ],

        "embedding_metadata": {
            "document_id": doc["document_id"],
            "title": doc["title"],
            "content": doc["content"],
            "category": doc["category"],
            "subcategory": doc["subcategory"],
            "language": doc["language"],
            "source": doc["source"],
            "source_type": doc["source_type"],
            "version": doc["version"],
            "page": doc["page"],
        },
    }


def main() -> None:
    """Main execution function."""
    print("=" * 60)
    print("GENERATING EMBEDDINGS (VERTEX AI)")
    print("=" * 60)
    print(f"Project ID : {GCP_PROJECT_ID}")
    print(f"Location   : {GOOGLE_CLOUD_LOCATION}")
    print(f"Model      : {EMBEDDING_MODEL}")
    print(f"Dimensions : {EMBEDDING_DIMENSIONS}")
    print(f"Input      : {INPUT_FILE}")
    print(f"Output     : {OUTPUT_FILE}")
    print("=" * 60)

    if not INPUT_FILE.exists():
        logger.error("Input file not found: %s", INPUT_FILE)
        return

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    documents: List[Dict[str, Any]] = json.loads(
        INPUT_FILE.read_text(encoding="utf-8")
    )

    print(f"Documents found: {len(documents)}\n")

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        for index, doc in enumerate(documents, start=1):
            document_id = doc["document_id"]

            print(
                f"[{index}/{len(documents)}] "
                f"Embedding {document_id}: "
                f"\"{doc['title']}\""
            )

        
            embedding = generate_embedding(doc["content"])

            
            datapoint = build_vector_search_datapoint(doc, embedding)

            
            f.write(json.dumps(datapoint) + "\n")

    print("\n" + "=" * 60)
    print("EMBEDDINGS CREATED SUCCESSFULLY")
    print("=" * 60)
    print(f"Output file: {OUTPUT_FILE}")
    print(f"Total datapoints: {len(documents)}")
    print("=" * 60)


if __name__ == "__main__":
    main()