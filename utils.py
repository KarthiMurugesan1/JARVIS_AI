import requests

def get_current_location():
    try:
        res = requests.get("https://ipinfo.io/json")
        data = res.json()
        return {
            "city": data.get("city", "Unknown"),
            "region": data.get("region", ""),
            "country": data.get("country", "")
        }
    except Exception as e:
        print("Location fetch error:", e)
        return None
