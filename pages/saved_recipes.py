# pages/saved_recipes.py
import streamlit as st
from backend.utils.recipe_storage import load_saved_recipes, delete_saved_recipe

def render():
    st.title("📚 My Saved Recipes")
    
    # Load saved recipes
    recipes = load_saved_recipes()
    
    # Back button
    if st.button("⬅️ Back to Recipe Generator"):
        st.session_state.current_page = "main"
        st.rerun()
    
    if not recipes:
        st.info("You haven't saved any recipes yet.")
        return
    
    st.write(f"You have {len(recipes)} saved recipes.")
    
    # Display each saved recipe
    for recipe in recipes:
        with st.expander(f"🧾 {recipe['title']} (Saved on {recipe['date_saved']})"):
            st.markdown(recipe["text"])
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"👨‍🍳 Cook This!", key=f"cook_{recipe['id']}"):
                    st.session_state.selected_recipe_text = recipe["text"]
                    st.session_state.current_page = "recipe_about"
                    st.rerun()
            with col2:
                if st.button(f"🗑️ Delete", key=f"delete_{recipe['id']}"):
                    delete_saved_recipe(recipe["id"])
                    st.success("Recipe deleted!")
                    st.rerun()