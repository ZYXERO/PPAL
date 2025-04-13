# backend/utils/step_utils.py

NON_INSTRUCTIONAL_PHRASES = [
    "here are", "we will", "let's", "introduction", "overview",
    "recipe for", "this recipe", "step-by-step", "instructions",
    "cooking instructions", "follow these steps", "you will need"
]

def is_valid_step(text):
    """Return True only if the text is a real cooking action."""
    lowered = text.strip().lower()
    
    if len(lowered.split()) <= 3:  # Skip very short/junk steps
        return False

    return not any(phrase in lowered for phrase in NON_INSTRUCTIONAL_PHRASES)
