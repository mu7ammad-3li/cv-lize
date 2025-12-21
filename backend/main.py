"""
CV Wizard - FastAPI Main Application
AI-powered CV optimization with security-first design
"""

import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Load environment variables
load_dotenv()

# Import database
# Import rate limiting
from slowapi.errors import RateLimitExceeded

from middleware.rate_limit import limiter, rate_limit_exceeded_handler
from models.database import Database
from routes.analyze import router as analyze_router
from routes.download import router as download_router

# Import routes
from routes.upload import router as upload_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    print("🚀 Starting CV Wizard API...")

    # Create upload and quarantine directories
    upload_dir = os.getenv("UPLOAD_DIR", "./uploads")
    quarantine_dir = os.getenv("QUARANTINE_DIR", "./quarantine")
    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(quarantine_dir, exist_ok=True)
    print(f"📁 Created directories: {upload_dir}, {quarantine_dir}")

    # Connect to database
    await Database.connect_db()

    print("✅ CV Wizard API is ready!")
    print(f"📊 Environment: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"🔒 Debug mode: {os.getenv('DEBUG', 'False')}")

    yield

    # Shutdown
    print("\n🛑 Shutting down CV Wizard API...")
    await Database.close_db()
    print("👋 Goodbye!")


# Create FastAPI app
app = FastAPI(
    title="CV Wizard API",
    description="AI-powered CV optimization with security-first design",
    version="1.0.0",
    lifespan=lifespan,
)

# Add rate limiting state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# CORS configuration
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000"
).split(",")

# Add wildcard for development if DEBUG is True
if os.getenv("DEBUG", "False") == "True":
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False if allowed_origins == ["*"] else True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(upload_router)
app.include_router(analyze_router)
app.include_router(download_router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "CV Wizard API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "upload": "POST /api/upload",
            "analyze": "POST /api/analyze",
            "download_markdown": "GET /api/download/{session_id}/markdown",
            "download_pdf": "GET /api/download/{session_id}/pdf",
            "get_session": "GET /api/session/{session_id}",
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected" if Database.db is not None else "disconnected",
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for unhandled errors
    """
    print(f"❌ Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc)
            if os.getenv("DEBUG", "False") == "True"
            else "An unexpected error occurred",
        },
    )


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    uvicorn.run(
        "main:app", host=host, port=port, reload=os.getenv("DEBUG", "False") == "True"
    )
