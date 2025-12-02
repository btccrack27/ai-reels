from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

# Controllers
from .presentation.controllers.content_controller import router as content_router
from .presentation.controllers.auth_controller import router as auth_router
from .presentation.controllers.subscription_controller import router as subscription_router
from .presentation.controllers.export_controller import router as export_router

# Database
from .infrastructure.database.postgres.config import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - Startup & Shutdown"""
    # Startup: Create database tables
    async with engine.begin() as conn:
        # In production: Use Alembic migrations instead
        # await conn.run_sync(Base.metadata.create_all)
        pass

    yield

    # Shutdown: Close connections
    await engine.dispose()


app = FastAPI(
    title="AI Reels Generator API",
    description="Backend API for AI-powered Instagram Reels content generation",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)


# ============== CORS Setup ==============

# Frontend URLs (Vercel + localhost)
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
allowed_origins = [
    frontend_url,
    "http://localhost:3000",
    "https://frontend-christians-projects-3af5506a.vercel.app",
    "https://*.vercel.app"  # All Vercel preview deployments
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Include Routers ==============

app.include_router(content_router)      # /api/content/*
app.include_router(auth_router)         # /api/auth/*
app.include_router(subscription_router) # /api/subscription/*
app.include_router(export_router)       # /api/export/*


# ============== Root Endpoints ==============

@app.get("/")
async def root():
    """API Root"""
    return {
        "message": "AI Reels Generator API",
        "version": "2.0.0",
        "docs": "/docs",
        "endpoints": {
            "content": "/api/content",
            "auth": "/api/auth",
            "subscription": "/api/subscription",
            "export": "/api/export"
        }
    }


@app.get("/health")
async def health_check():
    """Health Check Endpoint"""
    return {
        "status": "healthy",
        "version": "2.0.0"
    }
