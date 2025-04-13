import streamlit as st
from backend.gemini_ai import generate_recipes
from backend.utils.recipe_storage import save_recipe, load_saved_recipes

def render():
    st.title("🍽️ AI-Powered Recipe Suggestions")

    # Add button to view saved recipes
    if st.button("📚 View Saved Recipes"):
        st.session_state.current_page = "saved_recipes"
        st.rerun()

    if not st.session_state.get("generated_recipes"):
        with st.spinner("Generating delicious ideas..."):
            response_text = generate_recipes(
                st.session_state.ingredients,
                st.session_state.meal_type,
                st.session_state.cuisine,
                st.session_state.prep_time
            )
            
            # Better way to parse the response - don't rely on specific markers
            # First try to split by recipe markers if they exist
            if "=== RECIPE START ===" in response_text:
                recipes = response_text.split("=== RECIPE START ===")
                recipes = [r.split("=== RECIPE END ===")[0].strip() for r in recipes if "===" in r]
            else:
                # As a fallback, try to split by "Recipe" headings
                import re
                recipes = re.split(r'(?:\r?\n){2,}(?:#{1,3}\s*Recipe \d+|Recipe \d+:)', response_text)
                recipes = [r.strip() for r in recipes if r.strip()]
                
                # If we still don't have recipes, just use the entire response as one recipe
                if not recipes:
                    recipes = [response_text.strip()]
            
            st.session_state.generated_recipes = recipes

    if st.button("🔄 Regenerate"):
        with st.spinner("Regenerating..."):
            response_text = generate_recipes(
                st.session_state.ingredients,
                st.session_state.meal_type,
                st.session_state.cuisine,
                st.session_state.prep_time
            )
            
            # Same parsing logic as above
            if "=== RECIPE START ===" in response_text:
                recipes = response_text.split("=== RECIPE START ===")
                recipes = [r.split("=== RECIPE END ===")[0].strip() for r in recipes if "===" in r]
            else:
                import re
                recipes = re.split(r'(?:\r?\n){2,}(?:#{1,3}\s*Recipe \d+|Recipe \d+:)', response_text)
                recipes = [r.strip() for r in recipes if r.strip()]
                
                if not recipes:
                    recipes = [response_text.strip()]
            
            st.session_state.generated_recipes = recipes

    if st.session_state.get("generated_recipes"):
        for i, recipe in enumerate(st.session_state.generated_recipes):
            st.markdown(f"### 🧾 Recipe {i + 1}")
            st.markdown(recipe)
            
            # Create two columns for buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"👨‍🍳 Cook This!", key=f"select_{i}"):
                    st.session_state.selected_recipe_text = recipe
                    st.session_state.current_page = "recipe_about"
                    st.rerun()
            with col2:
                if st.button(f"🔖 Save Recipe", key=f"save_{i}"):
                    if save_recipe(recipe):
                        st.success("Recipe saved!")
                    else:
                        st.info("This recipe is already saved.")