import streamlit as st
from app_ui import show_ui

# Page config (must be here, only once)
st.set_page_config(page_title="Resume Builder", page_icon="📄", layout="wide")

# Call UI
show_ui()