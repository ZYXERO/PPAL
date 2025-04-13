import streamlit as st

def init_session_state():
    defaults = {
        "current_page": "main",
        "ingredients": [],
        "meal_type": "",
        "cuisine": [],
        "prep_time": 30,
        "generated_recipes": [],
        "selected_recipe_text": "",
        "step_index": 0
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
