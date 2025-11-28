import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

async def extract_claim(user_input: str) -> str:
    """
    Uses Gemini to extract a clean, factual claim from user input.
    
    Args:
        user_input: Raw text from user (headline, claim, or question)
    
    Returns:
        A clean, factual statement that can be verified
    """
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""You are a claim extraction expert. Your job is to convert user input into a clear, verifiable factual claim.

User Input: "{user_input}"

Task:
1. Extract the core factual claim from this input
2. Rewrite it as a clear, specific statement
3. Remove opinions, questions, or emotional language
4. Make it suitable for fact-checking

Rules:
- Keep it concise (1-2 sentences max)
- Make it specific and verifiable
- Remove any bias or loaded language
- If it's a question, convert it to a statement

Return ONLY the extracted claim, nothing else."""

        response = model.generate_content(prompt)
        extracted_claim = response.text.strip()
        
        # Clean up any quotes or extra formatting
        extracted_claim = extracted_claim.strip('"\'')
        
        return extracted_claim
        
    except Exception as e:
        # Fallback: return original input if extraction fails
        print(f"Error in claim extraction: {str(e)}")
        return user_input.strip()
