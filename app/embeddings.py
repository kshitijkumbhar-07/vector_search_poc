from google import genai
from google.genai import types

from app.config import EMBEDDING_DIMENSIONS, EMBEDDING_MODEL


client = genai.Client()


def generate_embedding(text: str) -> list[float]:
    """
    Generate a 768-dimensional Gemini embedding.
    """

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            output_dimensionality=EMBEDDING_DIMENSIONS,
        ),
    )

    if not response.embeddings:
        raise RuntimeError("Embedding API returned no embeddings.")

    vector = response.embeddings[0].values

    if vector is None:
        raise RuntimeError("Embedding API returned an empty vector.")

    if len(vector) != EMBEDDING_DIMENSIONS:
        raise RuntimeError(
            f"Expected {EMBEDDING_DIMENSIONS} dimensions, "
            f"got {len(vector)}."
        )

    return list(vector)