import time
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    GEMINI_API_KEY = "AIzaSyAl3E4EHEluu4GPY8He_0NZdl7y9o69NYc"
    print("Warning: Using hardcoded API key. Consider using environment variables instead.")

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
HEADERS = {"Content-Type": "application/json"}

def call_gemini(prompt, retries=3, delay=2):
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    for attempt in range(retries):
        try:
            response = requests.post(GEMINI_URL, headers=HEADERS, json=payload, timeout=30)

            if response.status_code == 429:
                wait_time = delay * (2 ** attempt)
                print(f"Rate limit hit. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                continue

            response.raise_for_status()
            response_json = response.json()

            if "candidates" not in response_json or not response_json["candidates"]:
                return "I couldn't generate a recipe with those ingredients. Please try again."

            if "content" not in response_json["candidates"][0] or "parts" not in response_json["candidates"][0]["content"]:
                return "I couldn't process the recipe properly. Please try again."

            if not response_json["candidates"][0]["content"]["parts"]:
                return "I received an empty response. Please try again."

            return response_json["candidates"][0]["content"]["parts"][0]["text"]

        except requests.exceptions.RequestException as e:
            print(f"Request error: {str(e)}")
            time.sleep(delay)
        except (KeyError, ValueError, TypeError) as e:
            print(f"Parsing error: {str(e)}")
            time.sleep(delay)

    return "Sorry, I couldn't generate recipes after multiple attempts. Please try again later."

def generate_recipes(ingredients, meal_type, cuisine, prep_time):
    prompt = f"""
You are a smart recipe generator. Based on the inputs below, generate 3 creative recipes.

Ingredients: {', '.join(ingredients)}
Meal Type: {meal_type}
Cuisine Type: {', '.join(cuisine)}
Max Total Prep Time: {prep_time} minutes

For each recipe:
1. Start with "=== RECIPE START ==="
2. Include:
   - Title (formatted as a header)
   - Short description
   - List of ingredients with measurements
   - Full preparation instructions (numbered steps)
3. End with "=== RECIPE END ==="

Use markdown formatting. Return only the recipes.
"""
    return call_gemini(prompt)

def summarize_recipe(recipe_text):
    prompt = f"""
Summarize the following recipe in 2–3 short, engaging sentences for a recipe app:

{recipe_text}
"""
    return call_gemini(prompt)

def break_into_steps(recipe_text):
    prompt = f"""
You are a strict cooking assistant that ONLY outputs cooking instructions.

Your job is to extract a step-by-step numbered list of real, actionable cooking steps from the given recipe. Each step must be something the user physically does in the kitchen (e.g., chop onions, preheat oven, mix ingredients).

Do NOT include:
- Any introductions or explanations (e.g., "Here's how...")
- Any summaries or context
- Any non-cooking language

Start directly with the first step. Do not say anything else before the list.

Recipe Text:
{recipe_text}
"""
    output = call_gemini(prompt)
    steps = output.strip().split("\n")
    cleaned_steps = [step.lstrip("0123456789. ").strip() for step in steps if step.strip()]
    return [{"text": step} for step in cleaned_steps]
