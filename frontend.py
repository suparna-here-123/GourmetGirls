import streamlit as st
from recoUtils import getCuisines

# Ingredient options
non_dairy_options = ["onion", "capsicum", "green chilli", "garlic", "carrot", "eggs", "flour"]
dairy_options = ["milk"]

# Initialize session state
if "numAllergens" not in st.session_state:
    st.session_state.numAllergens = 1
if "non_dairy_count" not in st.session_state:
    st.session_state.non_dairy_count = 1
if "dairy_count" not in st.session_state:
    st.session_state.dairy_count = 1

numPpl = st.number_input("How many people are you cooking for?", step = 1)
userCuisine = st.selectbox('Which cuisine are you in the mood for?', getCuisines())
userCourse = st.selectbox('Which course are you making?', ('Appetizer', 'Main', 'Dessert', 'Any'))

# Function to add a new input box
def add_allergen():
    st.session_state.numAllergens += 1

# Render dynamic text boxes
for i in range(st.session_state.numAllergens):
    st.text_input(f"Allergen {i+1}", key=f"allergen_{i}")

# Add Button
st.button("+ Add another", on_click=add_allergen)

# ONLY FOR TESTING - manually add ingredients + count
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

# Add Dairy Ingredients Section
# st.subheader("Dairy Ingredients")
dairyIng = st.selectbox('Dairy ingredients', ('Milk', 'None'))

# Button to get final list
if st.button("Submit"):
    userAllergens = [st.session_state[f"input_{i}"] for i in range(st.session_state.num_inputs)]
    if dairyIng == 'None' :
        dairyIng = []