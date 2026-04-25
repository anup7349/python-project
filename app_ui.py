import streamlit as st
from fpdf import FPDF

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

    st.markdown("---")

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

    # ---------------- PDF CLASS ----------------
    class ResumePDF(FPDF):

        def header(self):
            self.set_font("Arial", "B", 18)
            self.cell(0, 10, self.name, ln=True, align="C")

            self.set_font("Arial", size=11)
            self.cell(0, 8, f"{self.phone} | {self.email} | {self.linkedin}", ln=True, align="C")

            self.ln(3)
            self.set_draw_color(100, 100, 100)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(6)

        def section_title(self, title):
            self.set_font("Arial", "B", 13)
            self.cell(0, 8, title, ln=True)

            self.set_draw_color(180, 180, 180)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(4)

        def section_body(self, text):
            self.set_font("Arial", size=11)
            lines = text.split("\n")

            for line in lines:
                if line.strip():
                    self.multi_cell(0, 6, f"- {line}")

            self.ln(2)

        def skills_two_column(self, skills_text):
            self.set_font("Arial", size=11)
            skills_list = skills_text.split("\n")

            for i in range(0, len(skills_list), 2):
                left = skills_list[i]
                right = skills_list[i+1] if i+1 < len(skills_list) else ""

                self.cell(90, 6, f"- {left}")
                self.cell(0, 6, f"- {right}", ln=True)

            self.ln(3)

    # ---------------- BUTTON ----------------
    if st.button("🚀 Generate Resume"):

        if not name:
            st.error("Please enter your name")
            return

        pdf = ResumePDF()

        pdf.name = name
        pdf.phone = phone
        pdf.email = email
        pdf.linkedin = linkedin

        pdf.add_page()

        pdf.section_title("EDUCATION")
        pdf.section_body(education)

        pdf.section_title("TECHNICAL SKILLS")
        pdf.skills_two_column(skills)

        pdf.section_title("INTERNSHIP EXPERIENCE")
        pdf.section_body(internship)

        pdf.section_title("PROJECTS")
        pdf.section_body(projects)

        pdf.section_title("CERTIFICATIONS")
        pdf.section_body(certifications)

        pdf.section_title("SOFT SKILLS")
        pdf.section_body(soft_skills)

        pdf.output("resume.pdf")

        with open("resume.pdf", "rb") as f:
            st.download_button(
                label="📥 Download Resume",
                data=f,
                file_name="Resume.pdf",
                mime="application/pdf"
            )

        st.success("✅ Resume Generated Successfully!")