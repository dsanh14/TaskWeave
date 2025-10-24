"""Configuration management using pydantic-settings."""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Server
    port: int = 8000
    allowed_origins: str = "http://localhost:5173"
    
    # External APIs (all optional - fallback to mocks)
    anthropic_api_key: Optional[str] = None
    
    fetch_api_key: Optional[str] = None
    fetch_agentverse_url: str = "https://api.fetch.ai/agentverse"
    fetch_asi_one_url: str = "https://api.fetch.ai/asi-one"
    
    letta_api_key: Optional[str] = None
    letta_base_url: str = "https://api.letta.ai"
    
    composio_api_key: Optional[str] = None
    composio_base_url: str = "https://api.composio.dev"
    
    # Observability
    elastic_url: Optional[str] = None
    elastic_index: str = "taskweave-logs"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    @property
    def cors_origins(self) -> list[str]:
        """Parse allowed origins into a list."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]


# Global settings instance
settings = Settings()

