import sys
import asyncio

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import streamlit as st
from app_ui import show_ui

st.set_page_config(page_title="Resume Builder", page_icon="📄", layout="wide")

show_ui()