import streamlit as st

if "non_dairy_count" not in st.session_state:
    st.session_state.non_dairy_count = 1
if "dairy_count" not in st.session_state:
    st.session_state.dairy_count = 1

recipeName = st.text_input('Recipe Name')
recipeCourse = st.selectbox('Course', ('Appetizer', 'Main', 'Dessert'))
recipeCuisine = st.text_input('Cuisine').capitalize()

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
