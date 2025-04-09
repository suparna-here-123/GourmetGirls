import streamlit as st
from recoUtils import getCuisines, topKRecipes, scoreRecipes, getDairy, getNonDairy

# ------------------------------- Ingredient Options -------------------------------
non_dairy_options = getNonDairy()
dairy_options = getDairy()

# ------------------------------- Initialize Session State -------------------------------
if "numAllergens" not in st.session_state:
    st.session_state.numAllergens = 0

if "non_dairy_count" not in st.session_state:
    st.session_state.non_dairy_count = 0

if "dairy_count" not in st.session_state:
    st.session_state.dairy_count = 0

# ------------------------------- Number of People -------------------------------
numPpl = st.number_input("How many people are you cooking for?", step=1)

# ------------------------------- Cuisine Selection -------------------------------
userCuisine = st.selectbox("Which cuisine are you in the mood for?", getCuisines())

# ------------------------------- Course Selection -------------------------------
userCourse = st.selectbox("Which course are you making?", ("Appetizer", "Main", "Dessert", "Any"))

# ------------------------------- Max Prep Time -------------------------------
prepTime = st.slider("Max prep-time in minutes", min_value=10, max_value=60, step=10)

# ------------------------------- Allergens -------------------------------
def add_allergen():
    st.session_state.numAllergens += 1

st.subheader("Allergens")
for i in range(st.session_state.numAllergens):
    st.text_input(f"Allergen {i + 1}", key=f"allergen_{i}")

st.button("+ Add another", on_click=add_allergen)

# ------------------------------- Non-Dairy Ingredients -------------------------------
st.subheader("Non-Dairy Ingredients")
non_dairy_dict = {}

for i in range(st.session_state.non_dairy_count):
    cols = st.columns([2, 1])
    ingredient = cols[0].selectbox(
        f"Ingredient {i + 1}", non_dairy_options, key=f"non_dairy_{i}"
    )
    qty = cols[1].number_input(
        "Qty", min_value=1, max_value=10, value=1, key=f"non_dairy_qty_{i}"
    )
    non_dairy_dict[ingredient] = qty

if st.button("➕ Add Non-Dairy Ingredient"):
    st.session_state.non_dairy_count += 1

# ------------------------------- Dairy Ingredients -------------------------------
st.subheader("Dairy Ingredients")
dairy_dict = {}

for i in range(st.session_state.dairy_count):
    cols = st.columns([2, 1])
    dairy_ing = cols[0].selectbox(
        f"Dairy Ingredient {i + 1}", dairy_options, key=f"dairy_{i}"
    )
    qty = cols[1].number_input(
        "Qty in cups?", min_value=1, max_value=10, value=1, key=f"dairy_qty_{i}"
    )
    dairy_dict[dairy_ing] = qty

if st.button("➕ Add Dairy Ingredient"):
    st.session_state.dairy_count += 1

# ------------------------------- Suggest Recipes -------------------------------
if st.button("Suggest Recipes"):
    userAllergens = [
        st.session_state[f"allergen_{i}"] for i in range(st.session_state.numAllergens)
    ]

    scoredRecipes = scoreRecipes(
        numPpl, userCuisine, userCourse, userAllergens, prepTime, non_dairy_dict, dairy_dict
    )

    topK = topKRecipes(5, scoredRecipes)
    if topK :
        for recipe in topK:
            with st.container():
                st.markdown("---")  # Section divider

                # Card styling using columns
                top_col1, top_col2 = st.columns([4, 1])

                with top_col1:
                    st.markdown(f"### 🍽️ {recipe['recipe']}")
                    st.markdown(f"*Total Match Score:* **{recipe['total_score']}**")
                    st.markdown(f"*Ingredient Match Score:* **{recipe['ingredient_match_score']}**")

                st.markdown(" ")

                # Info block
                st.markdown(f"**🗺️ Cuisine:** {recipe['cuisine']}  |  **🍽️ Course:** {recipe['course']}  |  ⏱️ **Prep Time:** {recipe['prep_time']}  |  🍴 **Servings:** {recipe['servings']}")

                st.markdown(" ")

                # Instructions
                st.markdown("#### 👨‍🍳 Instructions")
                st.markdown(f"{recipe['recipe']}")

                st.markdown(" ")
                st.markdown("---")  # Card bottom divider
    else :
        st.subheader("Couldn't find any recipes that matched :( Want to try recipes similar users tried?")
