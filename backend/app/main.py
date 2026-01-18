"""
Main FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router


app = FastAPI(
    title="Pikachu Kawaii API",
    description="Backend API for Pikachu Kawaii game - DSA Project",
    version="1.0.0"
)

# CORS middleware for React frontend
# Allow localhost for development and Render domains for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://pokekawaii-frontend.onrender.com",  # Update with your Render frontend URL
        "*"  # Allow all origins (remove this in production for better security)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api", tags=["game"])


@app.get("/")
async def root():
    return {
        "message": "Pikachu Kawaii API - DSA Project",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
