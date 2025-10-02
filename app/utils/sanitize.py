import re

def sanitize_name(name: str) -> str:
    """Sanitize a romancist and a book name by stripping leading/trailing whitespace, 
    converting to lowercase, and replacing multiple spaces with a single space.
    """
    lower_name = name.lower() # Convert to lowercase
    strip_name = lower_name.strip() # Remove leading/trailing whitespace
    sanitized_name = re.sub(r'\s+', ' ', strip_name) # Replace multiple spaces with a single space

    return sanitized_name

