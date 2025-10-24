"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.router import health, llm, agents, memory, tools, websocket
from app.util.logging import log_info


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    log_info("TaskWeave backend starting up")
    yield
    log_info("TaskWeave backend shutting down")


# Create FastAPI app
app = FastAPI(
    title="TaskWeave API",
    description="Multi-agent productivity assistant backend",
    version="0.1.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health.router, tags=["health"])
app.include_router(llm.router, tags=["planning"])
app.include_router(agents.router, tags=["agents"])
app.include_router(memory.router, tags=["memory"])
app.include_router(tools.router, tags=["tools"])
app.include_router(websocket.router, tags=["websocket"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "TaskWeave",
        "version": "0.1.0",
        "status": "running"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=True
    )

