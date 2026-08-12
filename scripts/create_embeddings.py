import json
from pathlib import Path

from app.embeddings import generate_embedding


ROOT = Path(__file__).resolve().parents[1]

DOCUMENTS_FILE = ROOT / "data" / "documents.json"
OUTPUT_FILE = ROOT / "data" / "embeddings.json"


def main() -> None:
    print("=" * 60)
    print("CREATING EMBEDDINGS")
    print("=" * 60)

    if not DOCUMENTS_FILE.exists():
        raise FileNotFoundError(
            f"Missing documents file: {DOCUMENTS_FILE}"
        )

    # Load normal JSON array
    with DOCUMENTS_FILE.open("r", encoding="utf-8") as file:
        documents = json.load(file)

    if not isinstance(documents, list):
        raise ValueError(
            "documents.json must contain a JSON array."
        )

    embeddings = []

    for document in documents:

        document_id = document["id"]
        content = document["content"]

        print(
            f"Generating embedding for {document_id}..."
        )

        vector = generate_embedding(content)

        if len(vector) != 768:
            raise ValueError(
                f"{document_id}: expected 768 dimensions, "
                f"got {len(vector)}"
            )

        embeddings.append(
            {
                "id": document_id,
                "embedding": vector,
            }
        )

        print(
            f"{document_id} -> {len(vector)} dimensions"
        )

    # IMPORTANT:
    # Vertex AI Vector Search expects one JSON object
    # per line. The file extension can still be .json.
    with OUTPUT_FILE.open("w", encoding="utf-8") as file:

        for item in embeddings:
            json.dump(
                item,
                file,
                ensure_ascii=False,
                separators=(",", ":"),
            )

            file.write("\n")

    print()
    print("=" * 60)
    print("EMBEDDING GENERATION COMPLETE")
    print("=" * 60)
    print(f"Created: {OUTPUT_FILE}")
    print(f"Documents: {len(embeddings)}")
    print("Format: JSON objects, one per line")
    print("=" * 60)


if __name__ == "__main__":
    main()