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
    2. Verify claim using multiple sources (Indian fact-checkers + AI)
    3. Determine verdict with confidence score
    4. Generate explanation with evidence and sources
    """
    try:
        logger.info(f"📥 Received claim: {request.claim[:100]}...")
        
        # Validate input
        if not request.claim or len(request.claim.strip()) < 10:
            raise HTTPException(
                status_code=422, 
                detail="Claim must be at least 10 characters long"
            )
        
        # Step 1: Extract clean factual claim
        logger.info("🔍 Step 1: Extracting claim...")
        extracted_claim = await extract_claim(request.claim)
        logger.info(f"✅ Extracted: {extracted_claim}")
        
        # Step 2: Verify the claim using multiple tools
        logger.info("🔍 Step 2: Verifying with Indian fact-checkers + AI...")
        verification_results = await verify_claim(extracted_claim)
        logger.info(f"✅ Verification complete (sources checked: {verification_results.get('verification_summary', {}).get('total_sources', 0)})")
        
        # Step 3: Determine verdict based on verification results
        logger.info("🔍 Step 3: Determining verdict...")
        verdict_data = determine_verdict(verification_results)
        logger.info(f"✅ Verdict: {verdict_data['verdict']} (Confidence: {verdict_data['confidence_score']:.2%})")
        
        # Step 4: Generate human-friendly explanation
        logger.info("🔍 Step 4: Generating explanation...")
        explanation_data = await generate_explanation(
            original_claim=request.claim,
            extracted_claim=extracted_claim,
            verification_results=verification_results,
            verdict_data=verdict_data
        )
        logger.info(f"✅ Explanation generated")
        
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
        
        logger.info(f"🎉 Verification complete for claim")
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"❌ Error in verify endpoint: {str(e)}")
        error_message = str(e)
        
        # Provide helpful error messages
        if "GEMINI_API_KEY" in error_message or "API key" in error_message:
            raise HTTPException(
                status_code=500, 
                detail="API key configuration error. Please check your GEMINI_API_KEY in .env file."
            )
        elif "timeout" in error_message.lower() or "timed out" in error_message.lower():
            raise HTTPException(
                status_code=504, 
                detail="Request timed out. The verification took too long. Please try again."
            )
        else:
            raise HTTPException(
                status_code=500, 
                detail=f"Verification failed: {error_message}"
            )
