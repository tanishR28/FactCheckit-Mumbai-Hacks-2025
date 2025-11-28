from fastapi import APIRouter, HTTPException
from app.models import VerifyRequest, VerifyResponse
from app.agents.extractor_agent import extract_claim
from app.agents.verification_agent import verify_claim
from app.agents.verdict_agent import determine_verdict
from app.agents.explanation_agent import generate_explanation
import logging

router = APIRouter()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/verify", response_model=VerifyResponse)
async def verify_news_claim(request: VerifyRequest):
    """
    Main endpoint to verify a news claim or headline.
    
    Process:
    1. Extract clean factual claim from user input
    2. Verify claim using multiple sources
    3. Determine verdict
    4. Generate explanation and evidence
    """
    try:
        logger.info(f"Received claim: {request.claim[:100]}...")
        
        # Step 1: Extract clean factual claim
        extracted_claim = await extract_claim(request.claim)
        logger.info(f"Extracted claim: {extracted_claim}")
        
        # Step 2: Verify the claim using multiple tools
        verification_results = await verify_claim(extracted_claim)
        logger.info(f"Verification results obtained")
        
        # Step 3: Determine verdict based on verification results
        verdict_data = determine_verdict(verification_results)
        logger.info(f"Verdict: {verdict_data['verdict']}")
        
        # Step 4: Generate human-friendly explanation
        explanation_data = await generate_explanation(
            original_claim=request.claim,
            extracted_claim=extracted_claim,
            verification_results=verification_results,
            verdict_data=verdict_data
        )
        logger.info(f"Explanation generated")
        
        # Combine all results
        response = VerifyResponse(
            original_claim=request.claim,
            extracted_claim=extracted_claim,
            verdict=verdict_data["verdict"],
            confidence_score=verdict_data["confidence_score"],
            real_news_summary=explanation_data["real_news_summary"],
            detailed_explanation=explanation_data["detailed_explanation"],
            evidence_points=explanation_data["evidence_points"],
            sources=explanation_data["sources"],
            agent_reasoning=explanation_data.get("agent_reasoning")
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error in verify endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")
