from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import verify

app = FastAPI(
    title="FactCheckit API",
    description="AI-powered Crisis News & Claim Verification Tool",
    version="1.0.0"
)

# CORS configuration for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(verify.router, prefix="/api", tags=["verification"])

@app.get("/")
async def root():
    return {
        "message": "FactCheckit API is running",
        "version": "1.0.0",
        "endpoints": {
            "verify": "/api/verify"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
