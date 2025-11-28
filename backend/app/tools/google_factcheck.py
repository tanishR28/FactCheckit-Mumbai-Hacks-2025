import aiohttp
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def search_fact_check_api(claim: str) -> dict:
    """
    Searches Google Fact Check Tools API for existing fact checks.
    
    Args:
        claim: The claim to search for
    
    Returns:
        Dictionary with fact check results
    """
    api_key = os.getenv("GOOGLE_FACT_CHECK_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("Warning: No Fact Check API key found")
        return {"claims": [], "error": "No API key configured"}
    
    try:
        url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
        params = {
            "query": claim,
            "key": api_key,
            "languageCode": "en"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    claims = data.get("claims", [])
                    
                    # Parse and structure the results
                    structured_claims = []
                    for claim_data in claims[:5]:  # Top 5 results
                        claim_review = claim_data.get("claimReview", [{}])[0]
                        
                        structured_claims.append({
                            "text": claim_data.get("text", ""),
                            "claimant": claim_data.get("claimant", "Unknown"),
                            "claimReview": claim_review.get("title", ""),
                            "rating": claim_review.get("textualRating", ""),
                            "publisher": claim_review.get("publisher", {}).get("name", "Unknown"),
                            "url": claim_review.get("url", ""),
                            "reviewDate": claim_review.get("reviewDate", "")
                        })
                    
                    return {
                        "claims": structured_claims,
                        "total": len(structured_claims)
                    }
                else:
                    error_text = await response.text()
                    print(f"Fact Check API error: {response.status} - {error_text}")
                    return {"claims": [], "error": f"API error: {response.status}"}
                    
    except asyncio.TimeoutError:
        print("Fact Check API timeout")
        return {"claims": [], "error": "Request timeout"}
    except Exception as e:
        print(f"Fact Check API exception: {str(e)}")
        return {"claims": [], "error": str(e)}
