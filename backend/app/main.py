from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import verify
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="FactCheckit API",
    description="🇮🇳 AI-powered Crisis News & Claim Verification Tool - Built for Mumbai Hacks 2025",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(verify.router, prefix="/api", tags=["verification"])

@app.get("/")
async def root():
    """Root endpoint with API information"""
    gemini_configured = bool(os.getenv("GEMINI_API_KEY"))
    telegram_configured = bool(os.getenv("TELEGRAM_BOT_TOKEN"))
    
    return {
        "message": "FactCheckit API is running! 🚀",
        "version": "2.0.0",
        "status": "healthy",
        "features": {
            "indian_fact_checkers": ["PIB", "Alt News", "BOOM Live", "Factly", "Vishvas News"],
            "ai_powered": "Google Gemini 2.5 Flash",
            "web_scraping": "DuckDuckGo + NewsAPI",
            "telegram_bot": telegram_configured
        },
        "configuration": {
            "gemini_api": "✅ Configured" if gemini_configured else "❌ Not configured",
            "telegram_bot": "✅ Configured" if telegram_configured else "❌ Not configured"
        },
        "endpoints": {
            "verify": "/api/verify",
            "docs": "/docs",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "FactCheckit API",
        "version": "2.0.0"
    }
