from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class VerdictType(str, Enum):
    TRUE = "TRUE"
    FALSE = "FALSE"
    MISLEADING = "MISLEADING"
    UNVERIFIED = "UNVERIFIED"

class Source(BaseModel):
    title: str
    url: str
    publisher: Optional[str] = None

class EvidencePoint(BaseModel):
    point: str
    source: Optional[str] = None

class VerifyResponse(BaseModel):
    original_claim: str
    extracted_claim: str
    verdict: VerdictType
    confidence_score: float
    real_news_summary: str
    detailed_explanation: str
    evidence_points: List[EvidencePoint]
    sources: List[Source]
    agent_reasoning: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "original_claim": "Scientists have discovered a cure for all types of cancer",
                "extracted_claim": "A complete cure for all types of cancer has been discovered by scientists in 2025",
                "verdict": "FALSE",
                "confidence_score": 0.92,
                "real_news_summary": "While there have been significant advances in cancer treatment, including immunotherapies and targeted treatments, no universal cure for all types of cancer has been discovered.",
                "detailed_explanation": "This claim is false. Cancer research continues to make progress, but cancer is not a single disease - it's hundreds of different diseases. Current advances focus on specific cancer types and personalized treatments.",
                "evidence_points": [
                    {"point": "No major scientific journal has published findings of a universal cancer cure", "source": "Nature Medicine"},
                    {"point": "Recent breakthroughs focus on specific cancer types, not all cancers", "source": "WHO"},
                    {"point": "Cancer researchers emphasize progress, not cure announcements", "source": "NIH"}
                ],
                "sources": [
                    {"title": "Cancer Research Progress 2025", "url": "https://example.com", "publisher": "WHO"}
                ],
                "agent_reasoning": "Verified through Google Fact Check API, Google Search, and cross-referenced with medical databases."
            }
        }
