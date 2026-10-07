import re
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db, AsyncSessionLocal
from app.models.helpdesk import Document, DocumentChunk, Article, Category, DocStatus
from app.schemas.helpdesk import DocumentResponse, ArticleResponse
from app.services.pdf_processor import extract_text_from_pdf, chunk_text
from app.services.ai_service import get_embedding, generate_articles_from_text

router = APIRouter(prefix="/documents", tags=["Documents & RAG"])

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    return re.sub(r'[-\s]+', '-', text)

async def process_pdf_background(document_id: int, file_bytes: bytes, filename: str):
    """Tarea en segundo plano: Extrae texto, vectoriza en pgvector y redacta artículos."""
    async with AsyncSessionLocal() as db:
        try:
            doc = await db.get(Document, document_id)
            if not doc:
                return

            # 1. Extraer texto y fragmentar
            raw_text = extract_text_from_pdf(file_bytes)
            chunks = chunk_text(raw_text)

            # 2. Generar vectores y guardarlos en document_chunks
            for chunk_str in chunks:
                vector = await get_embedding(chunk_str)
                db.add(DocumentChunk(
                    document_id=doc.id,
                    content=chunk_str,
                    embedding=vector
                ))

            # 3. Generar artículos SEO con IA
            analysis = await generate_articles_from_text(raw_text, filename)

            for gen_art in analysis.articles:
                cat_slug = slugify(gen_art.category_name)
                res = await db.execute(select(Category).where(Category.slug == cat_slug))
                category = res.scalar_one_or_none()

                if not category:
                    category = Category(name=gen_art.category_name, slug=cat_slug)
                    db.add(category)
                    await db.flush()

                # Integrar FAQs al final del Markdown
                faq_md = "\n\n## Preguntas Frecuentes (FAQ)\n"
                for faq in gen_art.faqs:
                    faq_md += f"\n### {faq.question}\n{faq.answer}\n"

                db.add(Article(
                    title=gen_art.title,
                    slug=f"{slugify(gen_art.slug)}-{doc.id}",
                    summary_seo=gen_art.summary_seo[:300],
                    content_markdown=gen_art.content_markdown + faq_md,
                    is_published=True,
                    category_id=category.id,
                    source_document_id=doc.id
                ))

            doc.status = DocStatus.COMPLETED
            await db.commit()

        except Exception as e:
            await db.rollback()
            doc = await db.get(Document, document_id)
            if doc:
                doc.status = DocStatus.FAILED
                await db.commit()
            print(f"Error procesando PDF {document_id}: {e}")

@router.post("/upload", response_model=DocumentResponse, status_code=202)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF.")

    file_bytes = await file.read()

    new_doc = Document(filename=file.filename, status=DocStatus.PROCESSING)
    db.add(new_doc)
    await db.commit()
    await db.refresh(new_doc)

    # Dispara el procesamiento pesado sin bloquear al usuario
    background_tasks.add_task(process_pdf_background, new_doc.id, file_bytes, file.filename)
    return new_doc

@router.get("/", response_model=list[DocumentResponse])
async def list_documents(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Document).order_by(Document.uploaded_at.desc()))
    return result.scalars().all()

@router.get("/articles", response_model=list[ArticleResponse])
async def list_articles(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Article).options(selectinload(Article.category)).order_by(Article.created_at.desc())
    )
    return result.scalars().all()