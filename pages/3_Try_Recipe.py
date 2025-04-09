import streamlit as st
import pickle
from recoUtils import getUsers, getRecos


curUser = st.selectbox('Username', getUsers())
recos = getRecos(curUser, 5)
recosMapped = 