# backend/utils/pexels_fetcher.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def fetch_stock_image(query):
    headers = {
        "Authorization": PEXELS_API_KEY
    }

    # Append 'food' to bias results toward cooking content
    query_with_bias = f"{query} food"

    url = f"https://api.pexels.com/v1/search?query={query_with_bias}&per_page=1"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data["photos"]:
            return data["photos"][0]["src"]["large"]
        else:
            return "https://via.placeholder.com/768x512.png?text=No+Image+Found"
    except Exception as e:
        print(f"Pexels error: {str(e)}")
        return "https://via.placeholder.com/768x512.png?text=Error"
