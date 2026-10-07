import os
from openai import AsyncOpenAI
from app.schemas.helpdesk import DocumentAnalysisResult, GeneratedArticle, GeneratedFAQ

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
client = AsyncOpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY and not OPENAI_API_KEY.startswith("sk-proj-xxxx") else None

async def get_embedding(text: str) -> list[float]:
    """Genera un vector de 1536 dimensiones para el fragmento de texto."""
    if not client:
        # Vector determinista de prueba (1536 dimensiones) si no hay API Key configurada
        return [0.015] * 1536
    
    response = await client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

async def generate_articles_from_text(text: str, filename: str) -> DocumentAnalysisResult:
    """Analiza el manual técnico y devuelve artículos estructurados orientados a SEO."""
    if not client:
        # Respuesta estructurada de simulación para pruebas locales sin costo
        base_slug = filename.lower().replace(".pdf", "").replace(" ", "-")
        return DocumentAnalysisResult(
            articles=[
                GeneratedArticle(
                    title=f"Guía de configuración y uso: {filename}",
                    slug=f"guia-configuracion-{base_slug}",
                    summary_seo=f"Aprende paso a paso cómo configurar y resolver problemas comunes basados en {filename}.",
                    content_markdown=(
                        f"## Resumen del Manual\n\nEste artículo fue autogenerado a partir de **{filename}**.\n\n"
                        f"### Fragmento extraído\n> {text[:350]}...\n\n"
                        f"### Pasos recomendados\n1. Verificar los requisitos del sistema.\n2. Seguir el protocolo de instalación estándar."
                    ),
                    category_name="Guías Técnicas",
                    faqs=[
                        GeneratedFAQ(
                            question="¿Qué hacer si el sistema muestra error de conexión?",
                            answer="Verifique los parámetros de red y reinicie el servicio principal según la página 1 del manual."
                        )
                    ]
                )
            ]
        )

    completion = await client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres un arquitecto de soporte técnico B2B experto en SEO. "
                    "Analiza el siguiente manual y extrae artículos de base de conocimiento claros, "
                    "en formato Markdown, listos para un centro de ayuda público."
                )
            },
            {"role": "user", "content": text[:15000]}
        ],
        response_format=DocumentAnalysisResult,
    )
    return completion.choices[0].message.parsed