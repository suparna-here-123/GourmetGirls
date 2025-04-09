import streamlit as st
from recoUtils import getUsers

st.set_page_config(
    page_title="Welcome",
    page_icon="👋",
)

st.markdown(
    """
    ## Welcome to Gourmet Girlzzz
"""
)

curUser = st.selectbox('Username', getUsers())
st.session_state.currentUser = curUser