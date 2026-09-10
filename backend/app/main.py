from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.query import router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Loading RAG system...")

    # Importing the retrieval service loads:
    # - embedding model
    # - Chroma vector store
    from app.services import retrieval

    print("Embedding model loaded.")
    print("Vector store loaded.")
    print("Collection:", retrieval.collection.name)
    print("Stored chunks:", retrieval.collection.count())

    yield

    print("Shutting down RAG system.")


app = FastAPI(
    title="AI & Computer Science Learning Assistant",
    description="RAG-based assistant for AI and Computer Science documents",
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(router)