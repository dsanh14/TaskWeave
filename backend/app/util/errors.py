"""Custom exceptions for the application."""
from typing import Optional


class TaskWeaveError(Exception):
    """Base exception for TaskWeave errors."""
    
    def __init__(self, message: str, trace_id: Optional[str] = None):
        self.message = message
        self.trace_id = trace_id
        super().__init__(message)


class PlannerError(TaskWeaveError):
    """Error during planning phase."""
    pass


class OrchestratorError(TaskWeaveError):
    """Error during agent orchestration."""
    pass


class MemoryError(TaskWeaveError):
    """Error accessing or updating memory."""
    pass


class ToolError(TaskWeaveError):
    """Error executing a tool."""
    pass


class ValidationError(TaskWeaveError):
    """Input validation error."""
    pass

