import aiohttp
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def search_google(claim: str) -> dict:
    """
    Searches Google Custom Search for fact-checking and verification information.
    
    Args:
        claim: The claim to search for
    
    Returns:
        Dictionary with search results
    """
    api_key = os.getenv("GOOGLE_SEARCH_API_KEY") or os.getenv("GEMINI_API_KEY")
    search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID", "")
    
    if not api_key:
        print("Warning: No Google Search API key found")
        return {"results": [], "error": "No API key configured"}
    
    try:
        # Add "fact check" to search query for better results
        search_query = f"{claim} fact check"
        
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": api_key,
            "cx": search_engine_id if search_engine_id else "017576662512468239146:omuauf_lfve",  # Example search engine
            "q": search_query,
            "num": 5  # Top 5 results
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    items = data.get("items", [])
                    
                    # Structure the results
                    structured_results = []
                    for item in items:
                        structured_results.append({
                            "title": item.get("title", ""),
                            "snippet": item.get("snippet", ""),
                            "url": item.get("link", ""),
                            "displayLink": item.get("displayLink", "")
                        })
                    
                    return {
                        "results": structured_results,
                        "total": len(structured_results),
                        "query": search_query
                    }
                else:
                    error_text = await response.text()
                    print(f"Google Search API error: {response.status} - {error_text}")
                    
                    # Fallback: return empty results instead of failing
                    return {"results": [], "error": f"API error: {response.status}"}
                    
    except asyncio.TimeoutError:
        print("Google Search API timeout")
        return {"results": [], "error": "Request timeout"}
    except Exception as e:
        print(f"Google Search exception: {str(e)}")
        return {"results": [], "error": str(e)}
