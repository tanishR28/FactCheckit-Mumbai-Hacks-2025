import re

def clean_text(text: str) -> str:
    """
    Cleans and normalizes text for processing.
    
    Args:
        text: Raw text to clean
    
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s.,!?;:\-\'\"()]', '', text)
    
    # Trim whitespace
    text = text.strip()
    
    return text

def normalize_text(text: str) -> str:
    """
    Normalizes text for similarity comparison.
    
    Args:
        text: Text to normalize
    
    Returns:
        Normalized lowercase text
    """
    text = clean_text(text)
    text = text.lower()
    
    # Remove punctuation for comparison
    text = re.sub(r'[^\w\s]', '', text)
    
    return text
