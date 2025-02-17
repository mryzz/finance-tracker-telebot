import re

def format_input(message):
    """Formats the user input to extract amount, purpose, and remarks."""
    
    # Convert text to lowercase for case insensitivity
    text = message.text.lower().strip()
    
    # Allow both "10 food" and "10, food" formats
    parts = re.split(r'[, ]+', text, maxsplit=2)  # Split by comma or space
    
    # Ensure at least amount and purpose are provided
    if len(parts) < 2:
        return False

    amount, purpose = parts[:2]  # Extract amount and purpose
    remarks = parts[2] if len(parts) == 3 else ""  # Extract remarks if exists

    # Ensure amount is a valid number (integer or float)
    if not re.match(r'^\d+(\.\d+)?$', amount):
        return False
    
    if float(amount) <= 0:
        return False

    # Map single-letter shortcuts to full categories
    category_map = {
        'f': 'food',
        'b': 'bills',
        't': 'transport',
        'o': 'others',
        'e': 'entertainment',
        's': 'shopping',
        'h': 'healthcare',
        'l': 'learning'
    }

    # Replace shortcut if applicable
    purpose = category_map.get(purpose, purpose)  

    # Default to 'others' if purpose is empty
    if not purpose:
        purpose = 'others'

    # Remarks should not be empty, use a space instead
    if not remarks:
        remarks = ' '

    return amount, purpose, remarks
