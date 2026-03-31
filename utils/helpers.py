"""
Helpers - Common helper functions
"""

from datetime import datetime


def format_date(date_str: str, format_type: str = 'display') -> str:
    """Format date string for display"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        if format_type == 'display':
            return date_obj.strftime('%d %b %Y')
        else:
            return date_str
    except:
        return date_str


def get_date_difference(date_str: str) -> int:
    """Get number of days between date and today"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        now = datetime.now()
        diff = now - date_obj
        return diff.days
    except:
        return 0


def truncate_text(text: str, max_length: int = 50, suffix: str = '...') -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def format_number(num: int, suffix: str = '') -> str:
    """Format large numbers with K, M suffixes"""
    if num >= 1000000:
        return f"{num / 1000000:.1f}M {suffix}".strip()
    elif num >= 1000:
        return f"{num / 1000:.1f}K {suffix}".strip()
    else:
        return f"{num} {suffix}".strip()

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters
    
    Args:
        filename: Original filename
    
    Returns:
        Sanitized filename
    """
    # Remove or replace invalid characters
    invalid_chars = '<>:"|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    return filename

