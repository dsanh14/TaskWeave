"""Structured logging utilities."""
import json
import logging
from datetime import datetime
from typing import Any, Optional

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)

logger = logging.getLogger("taskweave")


def log_json(
    level: str,
    message: str,
    trace_id: Optional[str] = None,
    **kwargs: Any
) -> None:
    """Log a structured JSON message.
    
    Args:
        level: Log level (INFO, WARNING, ERROR, etc.)
        message: Log message
        trace_id: Optional trace ID for request tracking
        **kwargs: Additional fields to include in the log
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "message": message,
        "trace_id": trace_id,
        **kwargs
    }
    
    # Remove None values
    log_entry = {k: v for k, v in log_entry.items() if v is not None}
    
    log_method = getattr(logger, level.lower(), logger.info)
    log_method(json.dumps(log_entry))


def log_info(message: str, trace_id: Optional[str] = None, **kwargs: Any) -> None:
    """Log an info message."""
    log_json("INFO", message, trace_id, **kwargs)


def log_warning(message: str, trace_id: Optional[str] = None, **kwargs: Any) -> None:
    """Log a warning message."""
    log_json("WARNING", message, trace_id, **kwargs)


def log_error(message: str, trace_id: Optional[str] = None, **kwargs: Any) -> None:
    """Log an error message."""
    log_json("ERROR", message, trace_id, **kwargs)

