import streamlit as st
import base64
import tempfile
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
        browser = p.chromium.launch()
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

def show_ui():

    st.title("📄 Resume Builder")
    st.markdown("---")

    # ---------------- INPUT UI ----------------
    st.subheader("👤 Personal Information")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Full Name")
        email = st.text_input("Email")

    with col2:
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

    st.subheader("🏢 Internship Experience")
    internship = st.text_area("Enter internship details")

    st.subheader("🚀 Projects")
    projects = st.text_area("Enter project details")

    st.subheader("📜 Certifications")
    certifications = st.text_area("Enter certifications")

    st.subheader("🧠 Soft Skills")
    soft_skills = st.text_area("Enter soft skills")

    st.markdown("---")

    # ---------------- TEMPLATE SELECTION ----------------
    st.subheader("🎨 Choose Resume Template")

    template = st.selectbox(
        "Select Template",
        ["template1", "template2", "template3"]
    )

    # ---------------- BUTTON ----------------
    if st.button("🚀 Generate Resume"):

        if not name:
            st.error("Please enter your name")
            return

        # ---------------- PHOTO DATA ----------------
        photo_base64 = get_image_base64(photo)

        if photo_base64:
            photo_data = f"data:image/png;base64,{photo_base64}"
        else:
            photo_data = ""

        # ---------------- HTML PREVIEW ----------------
        html = load_template(template)

        html = html.replace("{{photo}}", photo_data)
        html = html.replace("{{name}}", name)
        html = html.replace("{{role}}", "")
        html = html.replace("{{phone}}", phone)
        html = html.replace("{{email}}", email)
        html = html.replace("{{location}}", linkedin)
        html = html.replace("{{linkedin}}", linkedin)
        html = html.replace("{{github}}", github)
        html = html.replace("{{summary}}", summary)

        html = html.replace("{{education}}", education)
        html = html.replace("{{skills}}", skills)
        html = html.replace("{{internship}}", internship)
        html = html.replace("{{project_desc}}", projects)
        html = html.replace("{{certifications}}", certifications)
        html = html.replace("{{soft_skills}}", soft_skills)

        st.subheader("📄 Resume Preview")
        st.components.v1.html(html, height=800, scrolling=True)

        # ---------------- HTML TO PDF DOWNLOAD ----------------
        pdf_file = convert_html_to_pdf(html)

        st.download_button(
            label="📥 Download Resume",
            data=pdf_file,
            file_name="Resume.pdf",
            mime="application/pdf"
        )

        st.success("✅ Resume Generated Successfully!")