import streamlit as st
from backend.gemini_ai import break_into_steps
from backend.utils.image_generator import describe_image_for_step
from backend.utils.pexels_fetcher import fetch_stock_image
from backend.utils.recipe_storage import save_recipe
from backend.utils.step_utils import is_valid_step

def render():
    recipe_text = st.session_state.selected_recipe_text
    recipe_lines = recipe_text.strip().split('\n')
    recipe_title = recipe_lines[0].strip('# ') if recipe_lines else "Recipe"

    st.title(f"Cooking: {recipe_title}")

    # ⬇️ Parse steps if not cached
    if "recipe_steps" not in st.session_state:
        with st.spinner("Breaking recipe into steps..."):
            raw_steps = break_into_steps(recipe_text)
            filtered_steps = [step for step in raw_steps if is_valid_step(step["text"])]
            st.session_state.recipe_steps = filtered_steps if filtered_steps else raw_steps

    steps = st.session_state.recipe_steps
    if "step_index" not in st.session_state:
        st.session_state.step_index = 0

    # 🔄 Step Progress
    progress = (st.session_state.step_index + 1) / len(steps)
    st.progress(progress)

    # 📋 Current Step
    step = steps[st.session_state.step_index]
    st.subheader(f"Step {st.session_state.step_index + 1} of {len(steps)}")
    st.write(step["text"])

    # 🖼️ Image & Caption
    step_key = f"image_desc_{st.session_state.step_index}"
    image_key = f"image_url_{st.session_state.step_index}"

    if step_key not in st.session_state:
        with st.spinner("Describing image..."):
            desc = describe_image_for_step(step["text"])
            st.session_state[step_key] = desc
            st.session_state[image_key] = fetch_stock_image(desc)

    st.image(st.session_state[image_key], use_container_width=True)
    st.caption(f"🖼️ *{st.session_state[step_key]}*")

    # 👇 All controls on a single bottom row
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

    with col1:
        if st.button("🔖 Save"):
            if save_recipe(recipe_text):
                st.success("Recipe saved!")
            else:
                st.info("This recipe is already saved.")

    with col2:
        if st.button("📄 Recipes List"):
            st.session_state.step_index = 0
            for key in list(st.session_state.keys()):
                if key.startswith("image_desc_") or key.startswith("image_url_"):
                    del st.session_state[key]
            st.session_state.pop("recipe_steps", None)
            st.session_state.pop("recipe_intro", None)
            st.session_state.current_page = "recipe_list"
            st.rerun()

    with col3:
        if st.button("🏠 Home"):
            st.session_state.step_index = 0
            for key in list(st.session_state.keys()):
                if key.startswith("image_desc_") or key.startswith("image_url_"):
                    del st.session_state[key]
            st.session_state.pop("recipe_steps", None)
            st.session_state.pop("recipe_intro", None)
            st.session_state.current_page = "main"
            st.rerun()

    with col4:
        if st.session_state.step_index > 0 and st.button("⬅️ Previous"):
            st.session_state.step_index -= 1
            st.rerun()

    with col5:
        if st.session_state.step_index < len(steps) - 1 and st.button("➡️ Next"):
            st.session_state.step_index += 1
            st.rerun()
        elif st.session_state.step_index == len(steps) - 1 and st.button("🏁 Finish"):
            st.session_state.step_index = 0
            for key in list(st.session_state.keys()):
                if key.startswith("image_desc_") or key.startswith("image_url_"):
                    del st.session_state[key]
            st.session_state.pop("recipe_steps", None)
            st.session_state.pop("recipe_intro", None)
            st.session_state.current_page = "recipe_list"
            st.rerun()
