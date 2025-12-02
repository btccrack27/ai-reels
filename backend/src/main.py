from fastapi import FastAPI
from contextlib import asynccontextmanager
from .presentation.controllers.reel_controller import router as reel_router
from .presentation.middlewares.cors import setup_cors
from .infrastructure.database.config import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    pass


app = FastAPI(
    title="AI Reels Generator API",
    description="Backend API for AI-powered video reel generation",
    version="1.0.0",
    lifespan=lifespan
)

# Setup CORS
setup_cors(app)

# Include routers
app.include_router(reel_router)


@app.get("/")
async def root():
    return {
        "message": "AI Reels Generator API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
