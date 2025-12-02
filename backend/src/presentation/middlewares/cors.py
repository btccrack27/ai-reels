from fastapi.middleware.cors import CORSMiddleware


def setup_cors(app):
    """Configure CORS middleware for the FastAPI application"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://localhost:8000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
