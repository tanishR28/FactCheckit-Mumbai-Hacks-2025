from difflib import SequenceMatcher
import re

def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculates similarity between two texts using SequenceMatcher.
    
    Args:
        text1: First text
        text2: Second text
    
    Returns:
        Similarity score between 0 and 1
    """
    if not text1 or not text2:
        return 0.0
    
    # Normalize texts
    text1 = normalize_for_similarity(text1)
    text2 = normalize_for_similarity(text2)
    
    # Calculate similarity
    similarity = SequenceMatcher(None, text1, text2).ratio()
    
    return similarity

def normalize_for_similarity(text: str) -> str:
    """
    Normalizes text for similarity calculation.
    
    Args:
        text: Text to normalize
    
    Returns:
        Normalized text
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    
    # Trim
    text = text.strip()
    
    return text

def jaccard_similarity(text1: str, text2: str) -> float:
    """
    Calculates Jaccard similarity (word-level) between two texts.
    
    Args:
        text1: First text
        text2: Second text
    
    Returns:
        Jaccard similarity score between 0 and 1
    """
    if not text1 or not text2:
        return 0.0
    
    # Normalize and split into words
    words1 = set(normalize_for_similarity(text1).split())
    words2 = set(normalize_for_similarity(text2).split())
    
    if not words1 or not words2:
        return 0.0
    
    # Calculate Jaccard similarity
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union) if union else 0.0

def hybrid_similarity(text1: str, text2: str) -> float:
    """
    Combines sequence and Jaccard similarity for better matching.
    
    Args:
        text1: First text
        text2: Second text
    
    Returns:
        Combined similarity score between 0 and 1
    """
    seq_sim = calculate_similarity(text1, text2)
    jaccard_sim = jaccard_similarity(text1, text2)
    
    # Weighted average (70% sequence, 30% Jaccard)
    return (seq_sim * 0.7) + (jaccard_sim * 0.3)
