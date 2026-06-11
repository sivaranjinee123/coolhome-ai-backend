"""
COOLHOME AI - MAIN BACKEND APPLICATION

This file starts the entire backend server.
It's the entry point - where everything begins.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes
from contextlib import asynccontextmanager




@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    This replaces the old on_event("startup") method
    Runs when server starts, then yields, then runs shutdown code
    """
    # STARTUP CODE (runs when server starts)
    print("=" * 70)
    print("🚀 COOLHOME AI BACKEND STARTING...")
    print("=" * 70)
    print("✅ FastAPI app initialized")
    print("✅ CORS enabled (frontend can call backend)")
    print("✅ Routes loaded (all 6 endpoints available)")
    print("=" * 70)
    print()
    print("📍 Server is running on: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print()
    print("=" * 70)
    print()
    
    yield  # Server is running now
    
    # SHUTDOWN CODE (runs when server stops)
    print()
    print("=" * 70)
    print("🛑 COOLHOME AI BACKEND SHUTTING DOWN...")
    print("=" * 70)

# ============================================================
# CREATE FASTAPI APP
# ============================================================

# Initialize FastAPI with the new lifespan parameter
app = FastAPI(
    title="CoolHome AI Backend",
    description="AI-Powered Passive Cooling Advisor for Heat-Resilient Homes",
    version="1.0.0",
    lifespan=lifespan  # Use new lifespan instead of on_event
)

# ============================================================
# CORS CONFIGURATION
# ============================================================

# CORS = Cross-Origin Resource Sharing
# What this means: Your frontend (Member 1) is on a different "origin" (port 3000)
# Your backend is on a different "origin" (port 8000)
# CORS lets them talk to each other

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from ALL origins
                          # In production, use specific URLs like ["http://localhost:3000"]
    allow_credentials=True,  # Allow sending credentials (cookies, etc.)
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# ============================================================
# INCLUDE ROUTES
# ============================================================

# Import all the routes (endpoints) from app/api/routes.py
# This makes all the endpoints available
app.include_router(routes.router)

# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def read_root():
    """
    When someone visits http://localhost:8000/
    They get this response
    """
    return {
        "message": "Welcome to CoolHome AI Backend",
        "status": "running ✅",
        "docs": "Visit http://localhost:8000/docs for API documentation",
        "health": "Call http://localhost:8000/api/health to check if backend is alive"
    }

# ============================================================
# RUN THE SERVER
# ============================================================

if __name__ == "__main__":
    """
    This code only runs if you execute: python main.py
    It doesn't run if this file is imported as a module
    """
    
    import uvicorn
    
    # Start the server
    # app = FastAPI app object
    # host="0.0.0.0" = Accept requests from any computer
    # port=8000 = Run on port 8000
    # reload=True = Restart server when you change code
    uvicorn.run(
        "main:app",  # Tell uvicorn where to find the app (fixes the warning!)
        host="0.0.0.0",
        port=8000,
        reload=True
    )
