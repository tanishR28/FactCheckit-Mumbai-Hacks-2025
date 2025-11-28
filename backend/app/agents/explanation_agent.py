import google.generativeai as genai
import os
from dotenv import load_dotenv
from app.models.response_model import Source, EvidencePoint, VerdictType
import json

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

async def generate_explanation(
    original_claim: str,
    extracted_claim: str,
    verification_results: dict,
    verdict_data: dict
) -> dict:
    """
    Uses Gemini to generate a human-friendly explanation of the verdict.
    
    Args:
        original_claim: Original user input
        extracted_claim: Cleaned factual claim
        verification_results: Results from verification agent
        verdict_data: Verdict and confidence from verdict agent
    
    Returns:
        Dictionary with explanation, evidence, and sources
    """
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Prepare context from verification results
        fact_check_claims = verification_results.get("fact_check_api", {}).get("claims", [])
        google_results = verification_results.get("google_search", {}).get("results", [])
        ai_analysis = verification_results.get("ai_analysis", {})
        
        verdict = verdict_data.get("verdict")
        confidence = verdict_data.get("confidence_score")
        
        # Build context string
        context = f"""
CLAIM TO VERIFY: {extracted_claim}

VERDICT: {verdict}
CONFIDENCE: {confidence}

AI ANALYSIS:
{ai_analysis.get('analysis', 'N/A')}

KEY FINDINGS:
"""
        
        for finding in ai_analysis.get("key_findings", []):
            context += f"- {finding}\n"
        
        context += "\nVERIFICATION SOURCES:\n"
        
        if fact_check_claims:
            context += "\nFact Check API Results:\n"
            for i, claim in enumerate(fact_check_claims[:3], 1):
                context += f"{i}. {claim.get('claimReview', 'N/A')} - Rating: {claim.get('rating', 'N/A')}\n"
                context += f"   Publisher: {claim.get('publisher', 'N/A')}\n"
        
        if google_results:
            context += "\nGoogle Search Results:\n"
            for i, result in enumerate(google_results[:3], 1):
                context += f"{i}. {result.get('title', 'N/A')}\n"
                context += f"   {result.get('snippet', 'N/A')}\n"
        
        # Generate explanation based on verdict type
        if verdict == VerdictType.FALSE:
            prompt = f"""{context}

Task: Generate a comprehensive explanation for why this claim is FALSE.

Provide a JSON response with:
1. "real_news_summary": A short (2-3 sentences) explanation of what the ACTUAL truth is
2. "detailed_explanation": A detailed explanation (3-4 sentences) of why the claim is false
3. "evidence_points": List of 2-3 key evidence points (each as {{"point": "...", "source": "..."}})

Be clear, factual, and helpful. Focus on educating the user."""

        elif verdict == VerdictType.TRUE:
            prompt = f"""{context}

Task: Generate a comprehensive explanation for why this claim is TRUE.

Provide a JSON response with:
1. "real_news_summary": A short (2-3 sentences) summary confirming the claim and providing context
2. "detailed_explanation": A detailed explanation (3-4 sentences) with additional context
3. "evidence_points": List of 2-3 key evidence points (each as {{"point": "...", "source": "..."}})

Be clear, factual, and provide helpful context."""

        elif verdict == VerdictType.MISLEADING:
            prompt = f"""{context}

Task: Generate a comprehensive explanation for why this claim is MISLEADING.

Provide a JSON response with:
1. "real_news_summary": A short (2-3 sentences) explanation of what is true and what is exaggerated/false
2. "detailed_explanation": A detailed explanation (3-4 sentences) breaking down the misleading aspects
3. "evidence_points": List of 2-3 key evidence points (each as {{"point": "...", "source": "..."}})

Be clear about what's true vs. misleading."""

        else:  # UNVERIFIED
            prompt = f"""{context}

Task: Generate a response explaining that we couldn't verify this claim.

Provide a JSON response with:
1. "real_news_summary": A short explanation of why we couldn't verify this
2. "detailed_explanation": What the user should do (check credible sources, wait for more information)
3. "evidence_points": List of 1-2 suggestions (each as {{"point": "...", "source": "..."}})

Be helpful and guide the user."""
        
        prompt += """\n\nIMPORTANT: Return ONLY valid JSON, no markdown formatting, no code blocks. Format:
{
  "real_news_summary": "...",
  "detailed_explanation": "...",
  "evidence_points": [
    {"point": "...", "source": "..."},
    {"point": "...", "source": "..."}
  ]
}"""
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean up response (remove markdown code blocks if present)
        response_text = response_text.replace("```json", "").replace("```", "").strip()
        
        # Parse JSON response
        explanation_data = json.loads(response_text)
        
        # Extract sources from verification results
        sources = []
        
        # Add fact-check sources
        for claim in fact_check_claims[:3]:
            sources.append(Source(
                title=claim.get("claimReview", "Fact Check"),
                url=claim.get("url", ""),
                publisher=claim.get("publisher", "Unknown")
            ))
        
        # Add Google search sources
        for result in google_results[:3]:
            sources.append(Source(
                title=result.get("title", "Search Result"),
                url=result.get("url", ""),
                publisher=result.get("displayLink", "Unknown")
            ))
        
        # Convert evidence points to proper format
        evidence_points = [
            EvidencePoint(
                point=ep.get("point", ""),
                source=ep.get("source")
            )
            for ep in explanation_data.get("evidence_points", [])
        ]
        
        # Build agent reasoning
        reasoning_parts = verdict_data.get("reasoning", [])
        agent_reasoning = " | ".join(reasoning_parts) if reasoning_parts else "AI-powered verification with multiple sources"
        
        return {
            "real_news_summary": explanation_data.get("real_news_summary", "Unable to generate summary"),
            "detailed_explanation": explanation_data.get("detailed_explanation", "Unable to generate explanation"),
            "evidence_points": evidence_points,
            "sources": sources,
            "agent_reasoning": agent_reasoning
        }
        
    except Exception as e:
        print(f"Error in explanation generation: {str(e)}")
        
        # Fallback response
        return {
            "real_news_summary": f"Verification completed with {verdict_data.get('verdict')} verdict.",
            "detailed_explanation": f"Based on available sources, the claim appears to be {verdict_data.get('verdict').lower()}.",
            "evidence_points": [
                EvidencePoint(point="Multiple sources were consulted", source="Verification System")
            ],
            "sources": [],
            "agent_reasoning": "Automated AI verification"
        }
