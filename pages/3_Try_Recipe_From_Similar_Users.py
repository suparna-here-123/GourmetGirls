import streamlit as st
import pickle
from recoUtils import getUsers, getRecos

curUser = st.session_state.currentUser
recos = getRecos(curUser, 5)

st.title("Recommended Recipes")

for idx, (score, recipe) in enumerate(recos):
    with st.container():
        st.markdown("---")  # Section divider

        # Card styling using columns
        top_col1, top_col2 = st.columns([4, 1])

        with top_col1:
            st.markdown(f"### 🍽️ {recipe['Name']}")
            st.markdown(f"*Suggested by:* **{recipe['source']}**")
            st.markdown(f"💯 **You'll like it:** `{score}%`")

        with top_col2:
            st.markdown(" ")
            st.markdown(" ")
            st.button(
                "🧑‍🍳 Get Help",
                key=f"help_{idx}",
                use_container_width=True,
                on_click=lambda r=recipe: st.session_state.update(selected_recipe=r),
            )
            if st.session_state.get("selected_recipe") == recipe:
                st.switch_page("pages/4_Recipe_Chatbot.py")

        st.markdown(" ")

        # Info block
        st.markdown(f"**🗺️ Cuisine:** {recipe['Cuisine']}  |  **🍽️ Course:** {recipe['Course']}  |  ⏱️ **Prep Time:** {recipe['Prep time']}  |  🍴 **Servings:** {recipe['servings']}")

        st.markdown(" ")

        # Tags and allergens
        st.markdown(f"**🏷️ Tags:** {', '.join(recipe['tags']) if recipe['tags'] else 'None'}")
        st.markdown(f"**⚠️ Allergens:** {', '.join(recipe['allergens']) if recipe['allergens'] else 'None'}")

        st.markdown(" ")

        # Ingredients
        st.markdown("#### 🧾 Ingredients")

        if recipe["Non-dairy ingredients"]:
            st.markdown("**🌿 Non-Dairy:**")
            for ing, qty in recipe["Non-dairy ingredients"].items():
                st.markdown(f"- {ing}: {qty}")

        if recipe["dairy ingredients"]:
            st.markdown("**🥛 Dairy:**")
            for ing, qty in recipe["dairy ingredients"].items():
                st.markdown(f"- {ing}: {qty}")

        st.markdown(" ")

        # Instructions
        st.markdown("#### 👨‍🍳 Instructions")
        st.markdown(f"{recipe['recipe']}")

        st.markdown(" ")
        st.markdown("---")  # Card bottom divider
