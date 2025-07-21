# query_preprocessor.py

from utils import get_current_location

def preprocess_query(query: str) -> str:
    query_lower = query.lower()
    location_keywords = ["weather", "traffic", "air quality", "near me", "my location", "in my area"]

    if any(kw in query_lower for kw in location_keywords) and "in" not in query_lower:
        # Get location once
        location = get_current_location()
        if location:
            query += f" in {location}"

    return query
