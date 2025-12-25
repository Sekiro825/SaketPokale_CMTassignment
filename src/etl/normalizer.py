import re
from datetime import datetime
from typing import Optional

def normalize_name(name: Optional[str]) -> Optional[str]:
    """
    Title cases the name and strips whitespace.
    Returns None if name is empty or invalid.
    """
    if not name or not isinstance(name, str) or not name.strip():
        return None
    return name.strip().title()

def standardize_date(date_str: Optional[str]) -> Optional[str]:
    """
    Parses various date formats and returns ISO 8601 (YYYY-MM-DD).
    Returns None if invalid.
    Supported formats: YYYY-MM-DD, DD/MM/YYYY, MMM DD YYYY
    """
    if not date_str or not isinstance(date_str, str):
        return None
    
    date_str = date_str.strip()
    formats = [
        "%Y-%m-%d",       # 2023-01-15
        "%d/%m/%Y",       # 15/01/2023
        "%b %d %Y",       # Oct 12 2021
        "%d-%m-%Y",       # 15-01-2023
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
            
    return None
