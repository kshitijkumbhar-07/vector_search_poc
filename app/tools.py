import json
from pathlib import Path

from app.vector_search import search_vector
from app.embeddings import generate_embedding


ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS_FILE = ROOT / "data" / "documents.json"


def load_documents() -> dict[str, str]:
    """
    Load documents.json into:
        document_id -> document content
    """

    documents = {}

    with DOCUMENTS_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    for document in data:
        documents[document["id"]] = document["content"]

    return documents


def retrieve_documents(
    query: str,
    top_k: int = 3,
) -> list[dict]:
    """
    Convert the query into an embedding,
    search Vertex AI Vector Search,
    and return matching documents.
    """

    # 1. Generate query embedding
    query_embedding = generate_embedding(query)

    # 2. Search Vector Search
    results = search_vector(
        query_embedding,
        top_k=top_k,
    )

    # 3. Load original documents
    documents = load_documents()

    retrieved = []

    for result in results:

        document_id = result.id

        retrieved.append(
            {
                "id": document_id,
                "content": documents.get(
                    document_id,
                    "[Document content not found]",
                ),
                "distance": result.distance,
            }
        )

    return retrieved


def search_knowledge_base(
    query: str,
) -> str:
    """
    ADK tool used by the RAG agent.

    Searches the internal knowledge base and
    returns the retrieved documents as text.
    """

    try:
        results = retrieve_documents(
            query=query,
            top_k=3,
        )

        if not results:
            return (
                "No relevant documents were found "
                "in the knowledge base."
            )

        output = []

        for result in results:
            output.append(
                f"Document ID: {result['id']}\n"
                f"Distance: {result['distance']}\n"
                f"Content: {result['content']}"
            )

        return "\n\n".join(output)

    except Exception as exc:
        return (
            "Knowledge base search failed. "
            f"Error: {exc}"
        )