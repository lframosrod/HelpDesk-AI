from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.config import settings
from app.core.database import get_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend asíncrono para generación de Centros de Ayuda SEO y RAG",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/health", tags=["Health"])
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            text("SELECT extname FROM pg_extension WHERE extname = 'vector';")
        )
        vector_installed = result.scalar() is not None
        return {
            "status": "ok",
            "service": settings.PROJECT_NAME,
            "database": "connected",
            "pgvector_enabled": vector_installed,
        }
    except Exception as e:
        return {"status": "error", "detail": str(e)}
