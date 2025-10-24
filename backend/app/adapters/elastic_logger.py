"""Elasticsearch logger adapter (optional)."""
from typing import Any, Optional
from datetime import datetime
import httpx
from app.config import settings
from app.util.logging import log_warning


class ElasticLogger:
    """Optional Elasticsearch logger for centralized logging."""
    
    def __init__(self):
        self.url = settings.elastic_url
        self.index = settings.elastic_index
        self.enabled = bool(self.url)
        
    async def log_event(
        self,
        level: str,
        message: str,
        trace_id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """Send a log event to Elasticsearch.
        
        Args:
            level: Log level
            message: Log message
            trace_id: Request trace ID
            **kwargs: Additional fields
        """
        if not self.enabled:
            return
        
        try:
            doc = {
                "timestamp": datetime.utcnow().isoformat(),
                "level": level,
                "message": message,
                "trace_id": trace_id,
                **kwargs
            }
            
            async with httpx.AsyncClient() as client:
                await client.post(
                    f"{self.url}/{self.index}/_doc",
                    json=doc,
                    timeout=5.0
                )
                
        except Exception as e:
            # Fail silently - don't let logging errors break the app
            log_warning(f"Failed to log to Elasticsearch: {e}")


# Global logger instance
elastic_logger = ElasticLogger()

