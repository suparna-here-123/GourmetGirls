import streamlit as st
from recoUtils import getUsers
from streamlit_extras.colored_header import colored_header
from streamlit_extras.let_it_rain import rain

st.set_page_config(page_title="Pantry Pal", page_icon="🥕", layout="centered")

st.title("👩‍🍳 Pantry Pal: Your AI Cooking Sidekick")
curUser = st.selectbox('Login', getUsers())
st.session_state.currentUser = curUser

colored_header("Smart. Savvy. A little saucy.", description="", color_name="orange-70")

st.markdown("### 🧊 Snap, Cook, Repeat")
st.markdown(
    "- 📸 **Take a photo of your fridge** – we'll suggest recipes based on what's inside.\n"
    "- 🥗 Make the most of what you already have!"
)

st.markdown("### 🌍 Grandma Knows Best")
st.markdown(
    "- 🧓 **Preserve indigenous and regional recipes**\n"
    "- 🌶️ Suggest lesser-known dishes loved by users with similar tastes"
)

st.markdown("### 💬 Chat & Cook Like a Pro")
st.markdown(
    "- 🤖 **Step-by-step cooking assistant**\n"
    "- 🧂 Handles kitchen mishaps with tips, tricks, and a pinch of humor!"
)

st.markdown("### 🎉 Why Pantry Pal?")
st.markdown(
    "- 🧠 Powered by AI\n"
    "- 💰 Saves money\n"
    "- 🌱 Reduces waste\n"
    "- ❤️ Celebrates culture"
)

rain(emoji="🍅", font_size=30, falling_speed=5, animation_length="infinite")

