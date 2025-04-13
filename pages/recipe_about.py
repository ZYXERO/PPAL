import streamlit as st
from backend.gemini_ai import summarize_recipe
from backend.utils.recipe_storage import save_recipe

# Do NOT call st.set_page_config() here again — it's already in streamlit_app.py

st.markdown("""
    <style>
    .stButton > button {
        height: 3em;
        width: 100%;
        white-space: nowrap;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

def render():
    recipe_text = st.session_state.selected_recipe_text
    st.title("📋 About the Recipe")

    with st.spinner("Summarizing..."):
        summary = summarize_recipe(recipe_text)
        st.write(summary)

    st.markdown("---")
    st.code(recipe_text)

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        if st.button("👨‍🍳 Start Cooking"):
            st.session_state.current_page = "recipe_steps"
            st.rerun()

    with col2:
        if st.button("📄 Recipes List"):
            st.session_state.current_page = "recipe_list"
            st.rerun()

    with col3:
        if st.button("🏠 Home"):
            st.session_state.current_page = "main"
            st.rerun()

    with col4:
        if st.button("🔖 Save Recipe"):
            if save_recipe(recipe_text):
                st.success("Recipe saved!")
            else:
                st.info("This recipe is already saved.")