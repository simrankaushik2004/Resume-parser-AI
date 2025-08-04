import PyPDF2
import tkinter as tk
from tkinter import filedialog

# List of keywords for ATS checking
required_keywords = ['Python', 'Machine Learning', 'Data Analysis', 
                     'AI', 'Communication', 'Problem Solving', 
                     'Teamwork', 'Leadership']

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        with open(pdf_file, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + " "
    except Exception as e:
        print("Error reading PDF:", e)
    return text

# Function to check ATS score
def ats_checker(resume_text):
    found_keywords = [word for word in required_keywords if word.lower() in resume_text.lower()]
    missing_keywords = [word for word in required_keywords if word.lower() not in resume_text.lower()]

    print("\n*** ATS Report ***")
    print("Found Keywords:", ", ".join(found_keywords))
    print("Missing Keywords:", ", ".join(missing_keywords))
    match_percentage = (len(found_keywords) / len(required_keywords)) * 100
    print(f"Match Percentage: {match_percentage:.2f}%")
    return match_percentage

# Main Function with File Dialog
def select_and_check_pdf():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    pdf_file = filedialog.askopenfilename(
        title="Select Resume PDF",
        filetypes=[("PDF Files", "*.pdf")]
    )

    if pdf_file:
        resume_text = extract_text_from_pdf(pdf_file)
        if resume_text.strip():
            ats_checker(resume_text)
        else:
            print("No text found in the PDF file.")
    else:
        print("No file selected.")

# Run the ATS Checker
select_and_check_pdf()
