import os
from openai import AsyncOpenAI
from app.schemas.helpdesk import DocumentAnalysisResult, GeneratedArticle, GeneratedFAQ

# Cliente apuntando directamente a la red interna de Podman donde vive Ollama
client = AsyncOpenAI(base_url="http://helpdesk_ollama:11434/v1", api_key="local-mode")


async def get_embedding(text: str) -> list[float]:
    """Genera un vector de 768 dimensiones usando nomic-embed-text en Ollama."""
    response = await client.embeddings.create(input=text, model="nomic-embed-text")
    return response.data[0].embedding


async def generate_articles_from_text(
    text: str, filename: str
) -> DocumentAnalysisResult:
    """Analiza el manual técnico y devuelve artículos estructurados orientados a SEO."""
    completion = await client.beta.chat.completions.parse(
        model="qwen2.5:1.5b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres un arquitecto de soporte técnico B2B experto en SEO. "
                    "Analiza el siguiente manual y extrae artículos de base de conocimiento claros, "
                    "en formato Markdown, listos para un centro de ayuda público."
                ),
            },
            {"role": "user", "content": text[:15000]},
        ],
        response_format=DocumentAnalysisResult,
    )
    return completion.choices[0].message.parsed


async def generate_rag_answer(query: str, context_chunks: list[str]) -> str:
    """Genera una respuesta directa basada únicamente en los fragmentos recuperados por pgvector."""
    if not context_chunks:
        return "No se encontró información relevante en los manuales cargados."

    context_str = "\n\n---\n\n".join(context_chunks)

    response = await client.chat.completions.create(
        model="qwen2.5:1.5b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres un asistente de soporte técnico preciso. Responde la duda del usuario "
                    "usando ÚNICAMENTE el contexto proporcionado. Si la respuesta no está en el contexto, "
                    "indica que no tienes esa información."
                ),
            },
            {
                "role": "user",
                "content": f"Contexto:\n{context_str}\n\nPregunta: {query}",
            },
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content
