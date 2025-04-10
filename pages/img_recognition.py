import streamlit as st
from recoUtils import getCuisines, topKRecipes, scoreRecipes

# ------------------------------- Ingredient Options -------------------------------
non_dairy_options = ["onion", "capsicum", "green chilli", "garlic", "carrot", "eggs", "flour"]
dairy_options = ["milk", "cheese"]
dairy_dict = {}
non_dairy_dict = {}
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


import requests, urllib.parse

st.subheader("🧠 Detect Ingredients from Image")

img_source = st.radio("Select image source:", ["Upload", "URL"])
api_key = "u7WezrPPtxKRBHLcB4oZ"

if img_source == "Upload":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        img_bytes = uploaded_file.getvalue()
        files = {"image": img_bytes}

        # For uploads, use detect.roboflow.com (not serverless)
        response = requests.post(
            "https://detect.roboflow.com/project2-exvgy/1",
            params={"api_key": api_key},
            files=files
        )


elif img_source == "URL":
    img_url = st.text_input("Paste image URL:")
    if img_url:
        encoded_url = urllib.parse.quote_plus(img_url)

        full_url = f"https://serverless.roboflow.com/project2-exvgy/1?api_key={api_key}&image={encoded_url}"
        response = requests.post(full_url)

# Parse and display detections
detected_ingredients = []

if 'response' not in locals():
    st.warning("❗ API call not made yet. Upload an image or enter a URL.")
elif response.status_code != 200:
    st.error(f"❌ Roboflow API error: {response.status_code}")
    st.text(response.text)
else:
    try:
        data = response.json()
        predictions = data.get("predictions", [])
        detected_ingredients = list({pred["class"] for pred in predictions})
        if detected_ingredients:
            st.success("✅ Ingredients detected:")
            st.write(detected_ingredients)
        else:
            st.info("⚠️ No ingredients detected. You can add them manually below.")
    except Exception as e:
        st.error(f"Error parsing response: {e}")
        st.write(response.text)

for i in detected_ingredients:
    if i in dairy_options:
        dairy_dict[i] = detected_ingredients.count(i)
    else:
        non_dairy_dict[i] = detected_ingredients.count(i)
#st.write(non_dairy_dict)
#st.write(dairy_dict)

# -------------------------------------------------------------------------
st.subheader("Non-Dairy Ingredients")

# First, display all detected non-dairy ingredients with their counts
for i, (ingredient, count) in enumerate(non_dairy_dict.items()):
    cols = st.columns([2, 1])
    cols[0].text(f"Detected: {ingredient}")
    count_value = cols[1].number_input(
        "Qty", min_value=1, max_value=10, value=count, key=f"non_dairy_detected_{ingredient}"
    )
    # Update the count in the dictionary
    non_dairy_dict[ingredient] = count_value

# Then add form for additional ingredients
remaining_slots = st.session_state.non_dairy_count
for i in range(remaining_slots):
    cols = st.columns([2, 1])
    new_ingredient = cols[0].selectbox(
        f"Additional Ingredient {i + 1}", 
        [None] + [opt for opt in non_dairy_options if opt not in non_dairy_dict], 
        key=f"non_dairy_new_{i}"
    )
    qty = cols[1].number_input(
        "Qty", min_value=1, max_value=10, value=1, key=f"non_dairy_new_qty_{i}"
    )
    if new_ingredient and new_ingredient != "None":
        non_dairy_dict[new_ingredient] = qty

if st.button("➕ Add More Non-Dairy"):
    st.session_state.non_dairy_count += 1

st.subheader("Dairy Ingredients")

# First, display all detected dairy ingredients with their counts
for i, (ingredient, count) in enumerate(dairy_dict.items()):
    cols = st.columns([2, 1])
    cols[0].text(f"Detected: {ingredient}")
    count_value = cols[1].number_input(
        "Qty in cups", min_value=1, max_value=10, value=count, key=f"dairy_detected_{ingredient}"
    )
    # Update the count in the dictionary
    dairy_dict[ingredient] = count_value

# Then add form for additional ingredients
for i in range(st.session_state.dairy_count):
    cols = st.columns([2, 1])
    dairy_ing = cols[0].selectbox(
        f"Additional Dairy {i + 1}", 
        [opt for opt in dairy_options if opt not in dairy_dict], 
        key=f"dairy_new_{i}"
    )
    qty = cols[1].number_input(
        "Qty in cups", min_value=1, max_value=10, value=1, key=f"dairy_new_qty_{i}"
    )
    if dairy_ing:
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
    if not scoredRecipes:
        st.warning("No recipes match your criteria. Please adjust your inputs.")
    else:
        st.success(f"Found {len(scoredRecipes)} matching recipes!")
        st.write(scoredRecipes)
    topK = topKRecipes(5, scoredRecipes)
    st.write(topK)
