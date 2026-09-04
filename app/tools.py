import json
from pathlib import Path

from app.vector_search import search_vector
from app.embeddings import generate_embedding


ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS_FILE = ROOT / "data" / "documents.json"


def load_documents() -> dict[str, dict]:
    """
    Load documents.json.

    Returns:
        {
            "doc2": {
                "document_id": "doc2",
                "title": "Kubernetes Service",
                "content": "...",
                "category": "kubernetes",
                "subcategory": "networking",
                "language": "en",
                "source": "kubernetes_docs",
                "version": 1
            }
        }
    """

    documents: dict[str, dict] = {}

    with DOCUMENTS_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    for document in data:
        document_id = document["document_id"]

        documents[document_id] = document

    return documents


def retrieve_documents(
    query: str,
    top_k: int = 3,
    category: str | None = None,
    subcategory: str | None = None,
    language: str | None = None,
) -> list[dict]:
    """
    Convert the user's query into an embedding,
    search Vertex AI Vector Search, optionally using
    metadata filters, and return the matching documents.
    """

    print("\n" + "=" * 50)
    print(" [ADK TOOL] STARTING DOCUMENT RETRIEVAL")
    print("=" * 50)
    print(f" Query String : '{query}'")
    print(f" Top-K Limit  : {top_k}")

    # Visual breakdown of applied filters in terminal
    applied_filters = []

    if category:
        applied_filters.append(f"category='{category}'")

    if subcategory:
        applied_filters.append(f"subcategory='{subcategory}'")

    if language:
        applied_filters.append(f"language='{language}'")

    filter_str = (
        ", ".join(applied_filters)
        if applied_filters
        else "None (Unfiltered)"
    )

    print(f" Applied Filters: [{filter_str}]")
    print("-" * 50)

    print("Generating query embedding...")
    query_embedding = generate_embedding(query)

    print("Querying Vertex AI Vector Search...")

    
    results = search_vector(
        query_embedding=query_embedding,
        top_k=top_k,
        category=category,
        subcategory=subcategory,
        language=language,
    )

    documents = load_documents()

    retrieved: list[dict] = []

    print(
        f"Vector search returned {len(results)} candidate match(es). "
        "Mapping to local JSON metadata...\n"
    )

    for idx, result in enumerate(results, start=1):

        document_id = result.id

        # Transforms:
        # "doc2_chunk_001" -> "doc2"
        document_id = result.id.split("chunk")[0]

        document = documents.get(document_id)

        if document is None:

            print(
                f"  [{idx}] Match ID: {document_id} | "
                f"Distance: {result.distance:.4f} "
                "-> ⚠️ NOT FOUND IN documents.json"
            )

            retrieved.append(
                {
                    "id": document_id,
                    "title": "[Unknown document]",
                    "content": "[Document content not found]",
                    "category": None,
                    "subcategory": None,
                    "language": None,
                    "source": None,
                    "version": None,
                    "distance": result.distance,
                }
            )

            continue

        print(
            f"  [{idx}] Match ID: {document_id} | "
            f"Title: '{document.get('title')}' | "
            f"Category: "
            f"{document.get('category')}/"
            f"{document.get('subcategory')} | "
            f"Language: {document.get('language')} | "
            f"Distance: {result.distance:.4f}"
        )

        retrieved.append(
            {
                "id": document_id,
                "title": document.get("title"),
                "content": document.get("content"),
                "category": document.get("category"),
                "subcategory": document.get("subcategory"),
                "language": document.get("language"),
                "source": document.get("source"),
                "version": document.get("version"),
                "distance": result.distance,
            }
        )

    print("-" * 50)
    print(
        f" Total Documents Successfully Resolved: "
        f"{len(retrieved)}"
    )
    print("=" * 50 + "\n")

    return retrieved


def search_knowledge_base(
    query: str,
    category: str | None = None,
    subcategory: str | None = None,
    language: str | None = None,
) -> str:
    """
    ADK tool used by the RAG agent.

    Searches the internal knowledge base using semantic
    vector search with optional metadata filters.

    Args:
        query:
            Natural-language question.

        category:
            Optional category filter.

            Examples:
                "kubernetes"
                "gcp"

        subcategory:
            Optional subcategory filter.

            Examples:
                "networking"
                "compute"
                "storage"

        language:
            Optional language filter.

            Examples:
                "en"
                "hi"
                "fr"
    """

    
    print("\n" + "=" * 60)
    print(" [GEMINI → ADK TOOL CALL]")
    print("=" * 60)
    print(f" Query              : {query}")
    print(f" Category           : {category}")
    print(f" Subcategory        : {subcategory}")
    print(f" Language           : {language}")
    print("=" * 60 + "\n")

    try:

        results = retrieve_documents(
            query=query,
            top_k=3,
            category=category,
            subcategory=subcategory,
            language=language,
        )

        if not results:

            print(
                " [ADK TOOL OUTCOME] "
                "No documents found matching criteria."
            )

            return (
                "No relevant documents were found "
                "in the knowledge base."
            )

        output: list[str] = []

        for result in results:

            output.append(
                f"Document ID: {result['id']}\n"
                f"Title: {result['title']}\n"
                f"Category: {result['category'] or 'N/A'}\n"
                f"Subcategory: {result['subcategory'] or 'N/A'}\n"
                f"Language: {result['language'] or 'N/A'}\n"
                f"Source: {result['source'] or 'N/A'}\n"
                f"Version: {result['version'] or 'N/A'}\n"
                f"Distance: {result['distance']}\n"
                f"Content: {result['content']}"
            )

        formatted_payload = "\n\n".join(output)

        print("--- [PAYLOAD RETURNED TO AGENT] ---")
        print(formatted_payload)
        print("-----------------------------------\n")

        return formatted_payload

    except Exception as exc:

        error_message = (
            "Knowledge base search failed. "
            f"Error: {exc}"
        )

        print(
            f"  [ADK TOOL ERROR]: {error_message}"
        )

        return error_message