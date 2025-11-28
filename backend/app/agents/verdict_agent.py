from app.models.response_model import VerdictType

def determine_verdict(verification_results: dict) -> dict:
    """
    Determines the verdict based on verification results, prioritizing AI analysis.
    
    Args:
        verification_results: Combined results from all verification tools
    
    Returns:
        Dictionary with verdict and confidence score
    """
    try:
        verdict = VerdictType.UNVERIFIED
        confidence_score = 0.0
        reasoning = []
        
        # Extract data
        fact_check_data = verification_results.get("fact_check_api", {})
        google_data = verification_results.get("google_search", {})
        ai_analysis = verification_results.get("ai_analysis", {})
        
        fact_check_claims = fact_check_data.get("claims", [])
        google_results = google_data.get("results", [])
        
        # Priority 1: AI Analysis (most intelligent)
        ai_verdict = ai_analysis.get("verdict_suggestion", "UNVERIFIED")
        ai_confidence = ai_analysis.get("confidence", 0.0)
        ai_reasoning = ai_analysis.get("reasoning", [])
        
        if ai_confidence > 0.0:
            # Map AI verdict to VerdictType
            verdict_map = {
                "TRUE": VerdictType.TRUE,
                "FALSE": VerdictType.FALSE,
                "MISLEADING": VerdictType.MISLEADING,
                "UNVERIFIED": VerdictType.UNVERIFIED
            }
            verdict = verdict_map.get(ai_verdict, VerdictType.UNVERIFIED)
            confidence_score = ai_confidence
            reasoning.extend([f"AI Analysis: {r}" for r in ai_reasoning])
        
        # Priority 2: Fact Check API (cross-reference)
        if fact_check_claims:
            for claim in fact_check_claims[:2]:  # Top 2 claims
                rating = claim.get("rating", "").lower()
                
                if any(word in rating for word in ["true", "correct", "accurate"]):
                    reasoning.append(f"✓ Fact-checker confirms: {claim.get('publisher', 'Unknown')}")
                    # Boost confidence if AI agrees
                    if verdict == VerdictType.TRUE:
                        confidence_score = min(0.95, confidence_score + 0.1)
                elif any(word in rating for word in ["false", "incorrect", "inaccurate"]):
                    reasoning.append(f"✗ Fact-checker debunks: {claim.get('publisher', 'Unknown')}")
                    if verdict == VerdictType.FALSE:
                        confidence_score = min(0.95, confidence_score + 0.1)
                elif any(word in rating for word in ["misleading", "mixture", "partially"]):
                    reasoning.append(f"⚠ Fact-checker: Partially true/misleading")
        
        # Priority 3: Google Search results analysis
        if google_results and len(google_results) > 0:
            reasoning.append(f"Analyzed {len(google_results)} web sources")
        
        # If still unverified but we have sources, adjust confidence
        if verdict == VerdictType.UNVERIFIED and len(google_results) > 0:
            confidence_score = max(0.2, confidence_score)
            reasoning.append("Insufficient evidence to make a definitive determination")
        
        # Ensure minimum confidence for non-unverified verdicts
        if verdict != VerdictType.UNVERIFIED and confidence_score < 0.3:
            confidence_score = 0.3
        
        return {
            "verdict": verdict,
            "confidence_score": round(confidence_score, 2),
            "reasoning": reasoning,
            "total_sources": len(fact_check_claims) + len(google_results),
            "ai_powered": True
        }
        
    except Exception as e:
        print(f"Error in verdict determination: {str(e)}")
        return {
            "verdict": VerdictType.UNVERIFIED,
            "confidence_score": 0.0,
            "reasoning": [f"Error: {str(e)}"],
            "total_sources": 0,
            "ai_powered": False
        }
