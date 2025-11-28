from app.tools.google_factcheck import search_fact_check_api
from app.tools.google_search import search_google
from app.agents.research_agent import analyze_with_gemini
from app.utils.preprocess import clean_text
import asyncio

async def verify_claim(claim: str) -> dict:
    """
    Verifies a claim using multiple sources and AI analysis.
    
    Args:
        claim: The extracted factual claim to verify
    
    Returns:
        Dictionary containing verification results from all sources
    """
    try:
        # Clean the claim
        cleaned_claim = clean_text(claim)
        
        # Run verification tools in parallel
        fact_check_task = search_fact_check_api(cleaned_claim)
        google_search_task = search_google(cleaned_claim)
        
        # Wait for all results
        fact_check_results, google_results = await asyncio.gather(
            fact_check_task,
            google_search_task,
            return_exceptions=True
        )
        
        # Handle exceptions
        if isinstance(fact_check_results, Exception):
            print(f"Fact Check API error: {fact_check_results}")
            fact_check_results = {"claims": [], "error": str(fact_check_results)}
            
        if isinstance(google_results, Exception):
            print(f"Google Search error: {google_results}")
            google_results = {"results": [], "error": str(google_results)}
        
        # Use Gemini AI to analyze search results
        search_results = google_results.get("results", [])
        ai_analysis = await analyze_with_gemini(cleaned_claim, search_results)
        
        # Compile verification results
        verification_results = {
            "claim": claim,
            "cleaned_claim": cleaned_claim,
            "fact_check_api": fact_check_results,
            "google_search": google_results,
            "ai_analysis": ai_analysis,
            "verification_summary": {
                "fact_check_found": len(fact_check_results.get("claims", [])) > 0,
                "google_results_count": len(google_results.get("results", [])),
                "ai_confidence": ai_analysis.get("confidence", 0.0),
                "total_sources": (
                    len(fact_check_results.get("claims", [])) + 
                    len(google_results.get("results", []))
                )
            }
        }
        
        return verification_results
        
    except Exception as e:
        print(f"Error in verification agent: {str(e)}")
        return {
            "claim": claim,
            "error": str(e),
            "fact_check_api": {"claims": []},
            "google_search": {"results": []},
            "ai_analysis": {
                "verdict_suggestion": "UNVERIFIED",
                "confidence": 0.0,
                "reasoning": [f"Error: {str(e)}"]
            },
            "verification_summary": {
                "fact_check_found": False,
                "google_results_count": 0,
                "ai_confidence": 0.0,
                "total_sources": 0
            }
        }
