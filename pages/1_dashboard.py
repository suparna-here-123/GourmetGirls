import streamlit as st
from recoUtils import getCuisines, topKRecipes, scoreRecipes

# Ingredient options
non_dairy_options = ["onion", "capsicum", "green chilli", "garlic", "carrot", "eggs", "flour"]
dairy_options = ["milk", "cheese"]

# Initialize session state
if "numAllergens" not in st.session_state:
    st.session_state.numAllergens = 0
if "non_dairy_count" not in st.session_state:
    st.session_state.non_dairy_count = 0
if "dairy_count" not in st.session_state:
    st.session_state.dairy_count = 0

#------------------------------------------ NUMBER OF PEOPLE ------------------------------------
numPpl = st.number_input("How many people are you cooking for?", step = 1)

#------------------------------------------ CUISINE ------------------------------------
userCuisine = st.selectbox('Which cuisine are you in the mood for?', getCuisines())

#------------------------------------------ COURSE ------------------------------------
userCourse = st.selectbox('Which course are you making?', ('Appetizer', 'Main', 'Dessert', 'Any'))

#------------------------------------------ MAX PREP TIME ------------------------------------
prepTime = st.slider('Max prep-time in minutes', min_value = 10, max_value = 60, step = 10)

#------------------------------------------ ALLERGENS ------------------------------------
# Function to add a new input box
def add_allergen():
    st.session_state.numAllergens += 1

# Render dynamic text boxes
for i in range(st.session_state.numAllergens):
    st.text_input(f"Allergen {i+1}", key=f"allergen_{i}")

# Add Button
st.button("+ Add another", on_click=add_allergen)

# ONLY FOR TESTING - manually add ingredients + count
#------------------------------------------NON-DAIRY INGREDIENTS ------------------------------------
# Add Non-Dairy Ingredients Section
st.subheader("Non-Dairy Ingredients")
non_dairy_dict = {}

for i in range(st.session_state.non_dairy_count):
    cols = st.columns([2, 1])
    ingredient = cols[0].selectbox(f"Ingredient {i+1}", non_dairy_options, key=f"non_dairy_{i}")
    qty = cols[1].number_input("Qty", min_value=1, max_value=10, value=1, key=f"non_dairy_qty_{i}")
    non_dairy_dict[ingredient] = qty

if st.button("➕ Add Non-Dairy Ingredient"):
    st.session_state.non_dairy_count += 1

#------------------------------------------ DAIRY INGREDIENTS ------------------------------------
# Add Dairy Ingredients Section
dairy_dict = {}
for i in range(st.session_state.dairy_count):
    cols = st.columns([2, 1])
    dairy_ing = cols[0].selectbox(f"Dairy Ingredient {i+1}", dairy_options, key=f"dairy_{i}")
    qty = cols[1].number_input("Qty in cups?", min_value=1, max_value=10, value=1, key=f"dairy_qty_{i}")
    dairy_dict[dairy_ing] = qty

if st.button("➕ Add Dairy Ingredient"):
    st.session_state.dairy_count += 1

#------------------------------------------ Get recipes ------------------------------------
# Button to get final list
if st.button("Suggest Recipes"):
    userAllergens = [st.session_state[f"allergen_{i}"] for i in range(st.session_state.numAllergens)]
    #st.write(numPpl, userCuisine, userCourse, userAllergens, prepTime, non_dairy_dict, dairy_dict)
    scoredRecipes = scoreRecipes(numPpl, userCuisine, userCourse, userAllergens, prepTime, non_dairy_dict, dairy_dict)

    #st.write(scoredRecipes)
    topK = topKRecipes(5, scoredRecipes)
    st.write(topK)