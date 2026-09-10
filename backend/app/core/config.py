from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    embedding_model: str = "all-MiniLM-L6-v2"
    vector_store_path: str = "data/vector_store"
    collection_name: str = "cs_learning_documents"
    llm_model: str = "llama3.2:3b"
    frontend_origin: str = "http://localhost:8501"

    class Config:
        env_file = ".env"


settings = Settings()