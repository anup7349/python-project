import base64
import os
import subprocess
import sys
import tempfile

import streamlit as st
from playwright.sync_api import sync_playwright


def load_template(template_name):
    with open(f"templates/{template_name}.html", "r", encoding="utf-8") as file:
        return file.read()


def get_image_base64(file):
    if file is not None:
        return base64.b64encode(file.read()).decode()
    return ""


@st.cache_resource(show_spinner=False)
def ensure_playwright_chromium():
    subprocess.run(
        [sys.executable, "-m", "playwright", "install", "chromium"],
        check=True,
    )


def convert_html_to_pdf(html_content):
    html_path = None
    pdf_path = None
    browser = None

    try:
        ensure_playwright_chromium()

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".html",
            mode="w",
            encoding="utf-8",
        ) as f:
            f.write(html_content)
            html_path = f.name

        pdf_path = html_path.replace(".html", ".pdf")

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                ],
            )

            page = browser.new_page()
            page.goto(f"file://{html_path}", wait_until="load")

            page.pdf(
                path=pdf_path,
                format="A4",
                print_background=True,
            )

            browser.close()
            browser = None

        with open(pdf_path, "rb") as pdf_file:
            return pdf_file.read()

    finally:
        if browser is not None:
            browser.close()

        if html_path and os.path.exists(html_path):
            os.remove(html_path)

        if pdf_path and os.path.exists(pdf_path):
            os.remove(pdf_path)


def show_ui():
    if "selected_template" not in st.session_state:
        st.session_state.selected_template = None

    if st.session_state.selected_template is None:
        st.title("Choose Resume Template")
        st.markdown("Select a template design to continue")
        st.markdown("---")

        templates = sorted(
            [
                file.replace(".html", "")
                for file in os.listdir("templates")
                if file.endswith(".html")
            ]
        )
