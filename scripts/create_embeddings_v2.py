import json
from pathlib import Path

from google import genai
from google.genai import types

from app.config import (
    EMBEDDING_MODEL,
    EMBEDDING_DIMENSIONS,
)

INPUT_FILE = Path("data/documents.json")
OUTPUT_FILE = Path("data/embeddings.jsonl")


# Gemini Developer API client.
# It reads GEMINI_API_KEY from the environment.
client = genai.Client()


def generate_embedding(text: str) -> list[float]:
    """
    Generate a Gemini embedding using the Gemini API.
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
            f"Expected {EMBEDDING_DIMENSIONS} dimensions, "
            f"got {len(vector)}."
        )

    return list(vector)


def main() -> None:

    print("=" * 60)
    print("GENERATING GEMINI EMBEDDINGS")
    print("=" * 60)

    print(f"Model      : {EMBEDDING_MODEL}")
    print(f"Dimensions : {EMBEDDING_DIMENSIONS}")
    print(f"Input      : {INPUT_FILE}")
    print(f"Output     : {OUTPUT_FILE}")
    print("=" * 60)

    documents = json.loads(
        INPUT_FILE.read_text(encoding="utf-8")
    )

    print(f"Documents found: {len(documents)}")

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:

        for index, doc in enumerate(documents, start=1):

            document_id = doc["document_id"]

            print(
                f"[{index}/{len(documents)}] "
                f"Embedding {document_id}: "
                f"{doc['title']}"
            )

            # ------------------------------------------------
            # 1. Generate vector
            # ------------------------------------------------

            embedding = generate_embedding(
                doc["content"]
            )

            # ------------------------------------------------
            # 2. Create Vertex AI Vector Search datapoint
            # ------------------------------------------------

            datapoint = {
                "id": f"{document_id}_chunk_001",

                "embedding": embedding,

                # --------------------------------------------
                # Categorical metadata used for PRE-FILTERING
                # --------------------------------------------

                "restricts": [
                    {
                        "namespace": "category",
                        "allow": [doc["category"]],
                    },
                    {
                        "namespace": "subcategory",
                        "allow": [doc["subcategory"]],
                    },
                    {
                        "namespace": "language",
                        "allow": [doc["language"]],
                    },
                    {
                        "namespace": "source",
                        "allow": [doc["source"]],
                    },
                    {
                        "namespace": "source_type",
                        "allow": [doc["source_type"]],
                    },
                ],

                # --------------------------------------------
                # Numeric metadata
                # --------------------------------------------

                "numeric_restricts": [
                    {
                        "namespace": "version",
                        "value_int": doc["version"],
                    },
                    {
                        "namespace": "page",
                        "value_int": doc["page"],
                    },
                ],

                # --------------------------------------------
                # Application metadata
                # --------------------------------------------

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

            # Write one JSON object per line
            f.write(
                json.dumps(datapoint)
                + "\n"
            )

    print()
    print("=" * 60)
    print("EMBEDDINGS CREATED SUCCESSFULLY")
    print("=" * 60)
    print(f"Output file: {OUTPUT_FILE}")
    print(f"Total datapoints: {len(documents)}")
    print("=" * 60)


if __name__ == "__main__":
    main()