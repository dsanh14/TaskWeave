"""ID generation utilities."""
import uuid


def generate_id(prefix: str = "") -> str:
    """Generate a unique ID with optional prefix."""
    unique_id = str(uuid.uuid4())
    return f"{prefix}{unique_id}" if prefix else unique_id


def generate_trace_id() -> str:
    """Generate a trace ID for request tracing."""
    return f"trace_{uuid.uuid4().hex[:12]}"

