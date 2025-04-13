import streamlit as st

# ✅ MUST be first Streamlit command
st.set_page_config(page_title="PantryBuddy", page_icon="🍱")  # Updated name

from pages import main_page, recipe_list, recipe_about, recipe_steps, saved_recipes
from backend.utils.state_manager import init_session_state

init_session_state()

page = st.session_state.get("current_page", "main")

if page == "main":
    main_page.render()
elif page == "recipe_list":
    recipe_list.render()
elif page == "recipe_about":
    recipe_about.render()
elif page == "recipe_steps":
    recipe_steps.render()
elif page == "saved_recipes":
    saved_recipes.render()
else:
    st.error("Page not found")
