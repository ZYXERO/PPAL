import streamlit as st

st.markdown("""
    <style>
    .stButton > button {
        width: 200px;
        height: 3em;
        font-size: 1.05em;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)


def render():
    # 🧠 Page Title
    st.markdown("""
    <div style='text-align: center;'>
        <h1>👨‍🍳 PantryBuddy AI</h1>
        <h4>Create meals using what you already have!</h4>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align: center; font-size: 0.85rem; color: gray;'>
        🧠 Powered by AI | 🍳 Built for busy kitchens | 📚 Recipes on demand
    </div>
    """, unsafe_allow_html=True)

    # 🧾 Input Form
    with st.form("ingredient_form", clear_on_submit=False):
        st.markdown("### 📝 Recipe Generator")

        ingredients = st.text_input(
            "Ingredients (space-separated):",
            placeholder="e.g. rice chicken onion"
        )

        meal_type = st.selectbox("Meal Type:", ["Breakfast", "Lunch", "Brunch", "Dinner", "Snack"])

        cuisine = st.multiselect("Cuisine Type:", ["American", "Indian", "Mediterranean", "Asian", "Mexican", "Other"])

        prep_time = st.slider("Max Total Prep Time (min):", 5, 120, 30)

        submitted = st.form_submit_button("🔍 Find Recipes")

    # Save inputs to session and reroute
    if submitted and ingredients:
        st.session_state.ingredients = ingredients.strip().split()
        st.session_state.meal_type = meal_type
        st.session_state.cuisine = cuisine
        st.session_state.prep_time = prep_time
        st.session_state.current_page = "recipe_list"
        st.rerun()

    # ⬇️ Move View Saved Recipes to bottom center
    st.markdown("---")
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    if st.button("📚 View Saved Recipes"):
        st.session_state.current_page = "saved_recipes"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
