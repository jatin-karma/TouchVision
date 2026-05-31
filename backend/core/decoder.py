"""
Braille Decoder — Maps 6-bit dot patterns to English characters.
Standard Braille alphabet encoding.
"""

from typing import Tuple, List

# Standard Braille alphabet mapping
# Each pattern is a 6-tuple: (dot1, dot2, dot3, dot4, dot5, dot6)
# Dot positions:
#   1 4
#   2 5
#   3 6

BRAILLE_MAP = {
    (1,0,0,0,0,0): 'a',
    (1,1,0,0,0,0): 'b',
    (1,0,0,1,0,0): 'c',
    (1,0,0,1,1,0): 'd',
    (1,0,0,0,1,0): 'e',
    (1,1,0,1,0,0): 'f',
    (1,1,0,1,1,0): 'g',
    (1,1,0,0,1,0): 'h',
    (0,1,0,1,0,0): 'i',
    (0,1,0,1,1,0): 'j',
    (1,0,1,0,0,0): 'k',
    (1,1,1,0,0,0): 'l',
    (1,0,1,1,0,0): 'm',
    (1,0,1,1,1,0): 'n',
    (1,0,1,0,1,0): 'o',
    (1,1,1,1,0,0): 'p',
    (1,1,1,1,1,0): 'q',
    (1,1,1,0,1,0): 'r',
    (0,1,1,1,0,0): 's',
    (0,1,1,1,1,0): 't',
    (1,0,1,0,0,1): 'u',
    (1,1,1,0,0,1): 'v',
    (0,1,0,1,1,1): 'w',
    (1,0,1,1,0,1): 'x',
    (1,0,1,1,1,1): 'y',
    (1,0,1,0,1,1): 'z',
    (0,0,0,0,0,0): ' ',  # empty cell = space
}

# Common Braille contractions and punctuation
BRAILLE_CONTRACTIONS = {
    (0,1,1,1,1,1): '.',
    (0,0,1,0,0,1): ',',
    (0,0,1,0,1,1): '!',
    (0,0,1,1,0,1): '?',
    (0,0,0,1,0,1): "'",
    (0,0,1,1,1,1): '"',
    (0,0,0,1,1,0): '-',
}


def decode_pattern(pattern: Tuple[int, ...]) -> str:
    """
    Decode a single 6-dot Braille pattern to a character.
    
    Args:
        pattern: Tuple of 6 binary values (dot1-dot6)
    
    Returns:
        Character corresponding to the pattern, or '?' if unknown
    """
    # Ensure pattern is a tuple of length 6
    if not isinstance(pattern, tuple):
        pattern = tuple(pattern)
    
    if len(pattern) != 6:
        return '?'
    
    # Try to match in contractions first, then regular alphabet
    char = BRAILLE_CONTRACTIONS.get(pattern)
    if char is not None:
        return char
    
    char = BRAILLE_MAP.get(pattern)
    if char is not None:
        return char
    
    return '?'


def decode_cells(cells: List[Tuple[int, ...]]) -> str:
    """
    Decode a list of Braille cells into English text.
    
    Args:
        cells: List of 6-tuples representing Braille cells
    
    Returns:
        Decoded English string
    """
    if not cells:
        return ""
    
    text = ""
    for cell in cells:
        char = decode_pattern(cell)
        text += char
    
    return text


def decode_with_confidence(cells: List[Tuple[int, ...]], 
                          confidence_scores: List[float] = None) -> Tuple[str, float]:
    """
    Decode cells with overall confidence score.
    
    Args:
        cells: List of Braille cell patterns
        confidence_scores: Optional confidence scores for each cell
    
    Returns:
        (decoded_text, overall_confidence)
    """
    text = decode_cells(cells)
    
    if confidence_scores and len(confidence_scores) > 0:
        avg_confidence = sum(confidence_scores) / len(confidence_scores)
    else:
        avg_confidence = 0.0
    
    return text, avg_confidence


def get_braille_info() -> dict:
    """
    Return information about Braille character mappings.
    """
    return {
        "alphabet_count": len(BRAILLE_MAP),
        "contraction_count": len(BRAILLE_CONTRACTIONS),
        "total_patterns": len(BRAILLE_MAP) + len(BRAILLE_CONTRACTIONS),
    }
