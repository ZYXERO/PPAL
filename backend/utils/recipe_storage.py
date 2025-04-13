# backend/utils/recipe_storage.py
import json
import os
from datetime import datetime

def load_saved_recipes():
    """Load saved recipes from JSON file"""
    try:
        if os.path.exists("saved_recipes.json") and os.path.getsize("saved_recipes.json") > 0:
            with open("saved_recipes.json", "r") as file:
                return json.load(file)
        return []
    except (json.JSONDecodeError, FileNotFoundError):
        # Return empty list if file doesn't exist or is invalid
        return []

def save_recipe(recipe_text):
    """Save a recipe to the JSON file"""
    recipes = load_saved_recipes()
    
    # Extract title from recipe text (first line or first few words)
    lines = recipe_text.strip().split('\n')
    title = lines[0].strip('# ') if lines else "Untitled Recipe"
    if not title or len(title) > 100:  # If no title or too long, use first few words
        title = ' '.join(recipe_text.split()[:5]) + "..."
    
    # Check if this recipe is already saved (avoid duplicates)
    for recipe in recipes:
        if recipe["text"] == recipe_text:
            return False  # Already saved
    
    # Add new recipe
    recipes.append({
        "id": len(recipes) + 1,
        "title": title,
        "text": recipe_text,
        "date_saved": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    # Save to file
    with open("saved_recipes.json", "w") as file:
        json.dump(recipes, file, indent=2)
    
    return True

def delete_saved_recipe(recipe_id):
    """Delete a saved recipe by ID"""
    recipes = load_saved_recipes()
    
    # Find and remove the recipe
    recipes = [recipe for recipe in recipes if recipe["id"] != recipe_id]
    
    # Update the IDs to maintain sequence
    for i, recipe in enumerate(recipes):
        recipe["id"] = i + 1
    
    # Save to file
    with open("saved_recipes.json", "w") as file:
        json.dump(recipes, file, indent=2)
    
    return True