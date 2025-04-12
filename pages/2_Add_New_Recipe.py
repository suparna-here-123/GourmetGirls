import streamlit as st
from recoUtils import getDairy, getNonDairy, addRecipe
from shortuuid import uuid

if "non_dairy_count" not in st.session_state:
    st.session_state.non_dairy_count = 0

if "dairy_count" not in st.session_state:
    st.session_state.dairy_count = 0

non_dairy_options = getNonDairy()
dairy_options = getDairy()

st.title("Add a Recipe")

# --- Basic Info ---
name = st.text_input("Recipe Name")
cuisine = st.selectbox("Cuisine", ["Indian", "Asian", "Continental", "Fusion"])
course = st.selectbox("Course", ["Main", "Appetizer", "Dessert"])
prep_time = st.slider("Preparation Time in minutes (e.g., '20 minutes')", min_value = 10, max_value = 20, step = 5)
servings = st.number_input("Servings", min_value=1, max_value=10, value=2, step=1)

# --- Ingredients ---
st.subheader("Non-Dairy Ingredients")
non_dairy = {}

for i in range(st.session_state.non_dairy_count):
    cols = st.columns([2, 1])
    ingredient = cols[0].selectbox(
        f"Ingredient {i + 1}", non_dairy_options, key=f"non_dairy_{i}"
    )
    qty = cols[1].number_input(
        "Qty", min_value=1, max_value=10, value=1, key=f"non_dairy_qty_{i}"
    )
    non_dairy[ingredient] = qty

if st.button("➕ Add Non-Dairy Ingredient"):
    st.session_state.non_dairy_count += 1

# -------------------

st.subheader("Dairy Ingredients")
dairy = {}

for i in range(st.session_state.dairy_count):
    cols = st.columns([2, 1])
    dairy_ing = cols[0].selectbox(
        f"Dairy Ingredient {i + 1}", dairy_options, key=f"dairy_{i}"
    )
    qty = cols[1].number_input(
        "Quantity in cups", min_value=1, max_value=10, value=1, key=f"dairy_qty_{i}"
    )
    dairy[dairy_ing] = qty

if st.button("➕ Add Dairy Ingredient"):
    st.session_state.dairy_count += 1


# --- Tags ---
st.subheader("Tags")
tag_input = st.text_input("Enter tags (comma-separated)", placeholder="vegetarian, quick, gluten-free")
tags = [t.strip() for t in tag_input.split(",") if t.strip()]

# --- Recipe Steps ---
recipe_text = st.text_area("Recipe Instructions", height=150)

# --- Final Output ---
if st.button("Generate Recipe Dictionary"):
    recipeID = 'R_' + uuid()
    recipe_dict = { 
                    "Name": name,
                    "Cuisine": cuisine,
                    "Course": course,
                    "Non-dairy ingredients": non_dairy,
                    "dairy ingredients": dairy,
                    "Prep time": prep_time,
                    "tags": tags,
                    "recipe": recipe_text,
                    "servings": servings,
                    "allergens" : [],
                    "source" : st.session_state.currentUser
                  }
    addRecipe(recipeID, recipe_dict)
    st.subheader("📦 Recipe added!")
