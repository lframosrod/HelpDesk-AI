from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List, Optional
from app.models.helpdesk import DocStatus


# --- CATEGORÍAS ---
class CategoryBase(BaseModel):
    name: str
    slug: str


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# --- DOCUMENTOS ---
class DocumentResponse(BaseModel):
    id: int
    filename: str
    status: DocStatus
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- ARTÍCULOS ---
class ArticleBase(BaseModel):
    title: str
    slug: str
    summary_seo: str
    content_markdown: str
    is_published: bool = False
    category_id: Optional[int] = None


class ArticleCreate(ArticleBase):
    source_document_id: int


class ArticleResponse(ArticleBase):
    id: int
    source_document_id: int
    created_at: datetime
    updated_at: datetime
    category: Optional[CategoryResponse] = None

    model_config = ConfigDict(from_attributes=True)


# --- AI STRUCTURED OUTPUTS (Para el RAG) ---
class GeneratedFAQ(BaseModel):
    question: str = Field(description="Pregunta frecuente detectada en el manual.")
    answer: str = Field(description="Respuesta corta y directa para el usuario.")


class GeneratedArticle(BaseModel):
    title: str = Field(
        description="Título claro y orientado a SEO (ej. 'Cómo configurar el sensor X')."
    )
    slug: str = Field(
        description="URL amigable en minúsculas, sin acentos y con guiones."
    )
    summary_seo: str = Field(
        description="Resumen ejecutivo del artículo, máximo 150 caracteres."
    )
    content_markdown: str = Field(
        description="El paso a paso extraído del documento, en formato Markdown."
    )
    category_name: str = Field(
        description="Nombre de la categoría sugerida para este artículo."
    )
    faqs: List[GeneratedFAQ] = Field(
        description="Lista de preguntas y respuestas útiles."
    )


class DocumentAnalysisResult(BaseModel):
    articles: List[GeneratedArticle] = Field(
        description="Lista de artículos extraídos lógicamente del documento."
    )
