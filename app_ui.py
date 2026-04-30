import streamlit as st
import base64
import tempfile
import os
from playwright.sync_api import sync_playwright

# ---------------- TEMPLATE LOADER ----------------
def load_template(template_name):
    with open(f"templates/{template_name}.html", "r", encoding="utf-8") as file:
        return file.read()

# ---------------- IMAGE CONVERTER ----------------
def get_image_base64(file):
    if file is not None:
        return base64.b64encode(file.read()).decode()
    return ""

# ---------------- HTML TO PDF CONVERTER ----------------
def convert_html_to_pdf(html_content):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8") as f:
        f.write(html_content)
        html_path = f.name

    pdf_path = html_path.replace(".html", ".pdf")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            args=["--no-sandbox"]
        )

        page = browser.new_page()
        page.goto(f"file:///{html_path}", wait_until="networkidle")

        page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True
        )

        browser.close()

    with open(pdf_path, "rb") as pdf_file:
        return pdf_file.read()

# ---------------- MAIN UI ----------------
def show_ui():

    # ---------------- SESSION STATE ----------------
    if "selected_template" not in st.session_state:
        st.session_state.selected_template = None

    # ---------------- TEMPLATE GALLERY PAGE ----------------
    if st.session_state.selected_template is None:

        st.title("🎨 Choose Resume Template")
        st.markdown("Select a template design to continue")
        st.markdown("---")

        templates = sorted(
            [file.replace(".html", "") for file in os.listdir("templates") if file.endswith(".html")]
        )

        cols = st.columns(3)

        for i, template in enumerate(templates):
            with cols[i % 3]:

                image_path = f"images/{template}.png"

                if os.path.exists(image_path):
                    st.image(image_path, use_container_width=True)
                else:
                    st.warning(f"Image missing: {template}.png")

                if st.button("Use Template", key=template):
                    st.session_state.selected_template = template
                    st.rerun()

        return

    # ---------------- FORM PAGE ----------------
    st.title("📄 Resume Builder")
    st.markdown(f"Selected Template: **{st.session_state.selected_template}**")

    if st.button("⬅️ Change Template"):
        st.session_state.selected_template = None
        st.rerun()

    st.markdown("---")

    # ---------------- INPUT UI ----------------
    st.subheader("👤 Personal Information")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Full Name")

    with col2:
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        linkedin = st.text_input("LinkedIn URL")
        github = st.text_input("GitHub URL")

    photo = st.file_uploader("Upload Profile Photo", type=["jpg", "png", "jpeg"])

    st.markdown("---")

    summary = st.text_area("Summary")

    st.subheader("🎓 Education")
    education = st.text_area("Enter your education (one per line)")

    st.subheader("💻 Technical Skills")
    skills = st.text_area("Enter your skills (one per line)")

    st.subheader("💼 Experience")
    experience = st.text_area("Enter your experience")

    st.subheader("🚀 Projects")
    projects = st.text_area("Enter project details")

    st.subheader("📜 Certifications")
    certifications = st.text_area("Enter certifications")

    st.subheader("🧠 Soft Skills")
    soft_skills = st.text_area("Enter soft skills")

    st.markdown("---")

    # ---------------- BUTTON ----------------
    if st.button("🚀 Generate Resume"):

        if not name:
            st.error("Please enter your name")
            return

        photo_base64 = get_image_base64(photo)

        if photo_base64:
            photo_data = f"data:image/png;base64,{photo_base64}"
        else:
            photo_data = ""

        # Use selected template from gallery
        template = st.session_state.selected_template
        html = load_template(template)

        html = html.replace("{{photo}}", photo_data)
        html = html.replace("{{name}}", name)
        html = html.replace("{{role}}", "")
        html = html.replace("{{phone}}", phone)
        html = html.replace("{{email}}", email)
        html = html.replace("{{linkedin}}", linkedin)
        html = html.replace("{{github}}", github)
        html = html.replace("{{summary}}", summary)
        html = html.replace("{{education}}", education)
        html = html.replace("{{skills}}", skills)
        html = html.replace("{{experience}}", experience)
        html = html.replace("{{project_desc}}", projects)
        html = html.replace("{{certifications}}", certifications)
        html = html.replace("{{soft_skills}}", soft_skills)

        st.subheader("📄 Resume Preview")
        st.components.v1.html(html, height=800, scrolling=True)

        with st.spinner("Generating your resume... Please wait"):
            pdf_file = convert_html_to_pdf(html)

        st.download_button(
            label="📥 Download Resume",
            data=pdf_file,
            file_name="Resume.pdf",
            mime="application/pdf"
        )

        st.success("✅ Resume Generated Successfully!")