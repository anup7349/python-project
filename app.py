from fpdf import FPDF

print("===== Resume Builder =====")

name = input("Enter your name: ")
email = input("Enter your email: ")
phone = input("Enter your phone: ")
skills = input("Enter your skills (comma separated): ")
education = input("Enter your education: ")
experience = input("Enter your experience: ")

pdf = FPDF()
pdf.add_page()

# Title
pdf.set_font("Arial", "B", 16)
pdf.cell(200, 10, "RESUME", ln=True, align="C")

pdf.ln(10)

pdf.set_font("Arial", size=12)

pdf.cell(200, 10, f"Name: {name}", ln=True)
pdf.cell(200, 10, f"Email: {email}", ln=True)
pdf.cell(200, 10, f"Phone: {phone}", ln=True)

pdf.ln(5)

pdf.set_font("Arial", "B", 12)
pdf.cell(200, 10, "Skills:", ln=True)
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, skills)

pdf.set_font("Arial", "B", 12)
pdf.cell(200, 10, "Education:", ln=True)
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, education)

pdf.set_font("Arial", "B", 12)
pdf.cell(200, 10, "Experience:", ln=True)
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, experience)

pdf.output("resume.pdf")

print("✅ Resume generated successfully! Check your folder.")