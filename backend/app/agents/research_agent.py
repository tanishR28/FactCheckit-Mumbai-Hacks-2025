import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

async def analyze_with_gemini(claim: str, search_results: list) -> dict:
    """
    Uses Gemini AI to analyze search results and make intelligent verdict.
    
    Args:
        claim: The claim to verify
        search_results: List of search results from Google
    
    Returns:
        Dictionary with AI analysis including verdict and evidence
    """
    try:
        # If no search results, use Gemini's knowledge directly
        if not search_results or len(search_results) == 0:
            print(f"No search results available. Using Gemini's built-in knowledge for: {claim}")
            
            # Fallback: Ask Gemini directly based on its training data
            fallback_prompt = f"""You are an expert fact-checker with access to your training data (up to your knowledge cutoff).

CLAIM TO VERIFY: "{claim}"

Since no web search results are available, use your training knowledge to analyze this claim.

Your task:
1. Based on your training data, determine if this claim is generally TRUE, FALSE, MISLEADING, or UNVERIFIED
2. Provide reasoning based on established facts you know
3. Be honest about limitations if the claim is too recent or obscure

Provide your analysis in this exact JSON format:
{{
    "verdict": "TRUE" or "FALSE" or "MISLEADING" or "UNVERIFIED",
    "confidence": 0.0 to 1.0,
    "reasoning": ["point 1", "point 2", "point 3"],
    "key_findings": ["finding 1", "finding 2"],
    "evidence_summary": "Brief summary based on your knowledge",
    "caveat": "Note that this is based on training data, not current web search"
}}

Guidelines:
- TRUE: You're confident this is accurate based on established facts (confidence > 0.6)
- FALSE: You're confident this is false based on established facts (confidence > 0.6)
- MISLEADING: Partially true or requires context (confidence 0.4-0.6)
- UNVERIFIED: Too recent, obscure, or you don't have reliable information (confidence < 0.4)

Return ONLY the JSON, no additional text."""

            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content(fallback_prompt)
                response_text = response.text.strip()
                
                # Remove markdown code blocks if present
                if response_text.startswith("```json"):
                    response_text = response_text[7:]
                if response_text.startswith("```"):
                    response_text = response_text[3:]
                if response_text.endswith("```"):
                    response_text = response_text[:-3]
                
                import json
                analysis = json.loads(response_text.strip())
                
                return {
                    "analysis": analysis.get("evidence_summary", "Based on AI knowledge"),
                    "verdict_suggestion": analysis.get("verdict", "UNVERIFIED"),
                    "confidence": float(analysis.get("confidence", 0.3)),
                    "reasoning": analysis.get("reasoning", []),
                    "key_findings": analysis.get("key_findings", []),
                    "sources_analyzed": 0,
                    "fallback_mode": True,
                    "caveat": "Analysis based on AI training data (no live web search)"
                }
            except Exception as fallback_error:
                print(f"Fallback analysis error: {str(fallback_error)}")
                return {
                    "analysis": "No search results available and fallback failed",
                    "verdict_suggestion": "UNVERIFIED",
                    "confidence": 0.0,
                    "reasoning": ["Unable to verify - no web search results available"],
                    "sources_analyzed": 0
                }
        
        # Prepare context from search results
        context_parts = []
        for idx, result in enumerate(search_results[:5], 1):
            context_parts.append(
                f"Source {idx}:\n"
                f"Title: {result.get('title', 'N/A')}\n"
                f"Snippet: {result.get('snippet', 'N/A')}\n"
                f"URL: {result.get('url', 'N/A')}\n"
            )
        
        context = "\n".join(context_parts)
        
        # Create prompt for Gemini
        prompt = f"""You are an expert fact-checker analyzing information to verify a claim.

CLAIM TO VERIFY: "{claim}"

SEARCH RESULTS FROM THE WEB:
{context}

Your task:
1. Carefully analyze all the search results above
2. Look for patterns of debunking, confirmation, or mixed evidence
3. Consider the credibility of sources (news sites, fact-checkers, scientific publications)
4. Determine if the claim is TRUE, FALSE, MISLEADING, or UNVERIFIED

Provide your analysis in this exact JSON format:
{{
    "verdict": "TRUE" or "FALSE" or "MISLEADING" or "UNVERIFIED",
    "confidence": 0.0 to 1.0,
    "reasoning": ["point 1", "point 2", "point 3"],
    "key_findings": ["finding 1", "finding 2"],
    "evidence_summary": "Brief summary of evidence"
}}

Guidelines:
- TRUE: Multiple reliable sources confirm the claim with strong evidence (confidence > 0.7)
- FALSE: Multiple reliable sources debunk the claim with clear evidence (confidence > 0.7)
- MISLEADING: Mixed evidence, partially true, taken out of context (confidence 0.4-0.7)
- UNVERIFIED: Insufficient evidence or conflicting sources (confidence < 0.4)

Be objective and evidence-based. Return ONLY the JSON, no additional text."""

        # Call Gemini
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        
        # Parse JSON response
        import json
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        analysis = json.loads(response_text.strip())
        
        return {
            "analysis": analysis.get("evidence_summary", ""),
            "verdict_suggestion": analysis.get("verdict", "UNVERIFIED"),
            "confidence": float(analysis.get("confidence", 0.0)),
            "reasoning": analysis.get("reasoning", []),
            "key_findings": analysis.get("key_findings", []),
            "sources_analyzed": len(search_results)
        }
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error in research agent: {str(e)}")
        print(f"Response was: {response_text if 'response_text' in locals() else 'N/A'}")
        return {
            "analysis": "Error parsing AI response",
            "verdict_suggestion": "UNVERIFIED",
            "confidence": 0.0,
            "reasoning": ["Unable to analyze results properly"],
            "key_findings": [],
            "sources_analyzed": len(search_results)
        }
    except Exception as e:
        print(f"Error in research agent: {str(e)}")
        return {
            "analysis": f"Error: {str(e)}",
            "verdict_suggestion": "UNVERIFIED",
            "confidence": 0.0,
            "reasoning": [f"Analysis error: {str(e)}"],
            "key_findings": [],
            "sources_analyzed": 0
        }
