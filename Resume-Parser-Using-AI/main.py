import docx2txt
from tkinter import Tk, filedialog, Canvas, Button, PhotoImage, Label, StringVar,CENTER,LEFT
import spacy
from spacy.matcher import Matcher
import re
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import PhotoImage,Toplevel
from customtkinter import *
from PyPDF2 import PdfReader
import os
from PIL import Image, ImageTk
from customtkinter import CTk, CTkLabel, CTkImage
from tkinter import Toplevel, Label,messagebox
import subprocess



def open_ems(parent_window=None):
    """
    Function to open the ems system UI in a new Toplevel window.
    Ensures no conflicts with Tkinter's image context.
    """
    ems_window = Toplevel(parent_window) if parent_window else CTk()
    ems_window.geometry("800x600")
    ems_window.title("ems System")

    try:
        # Dynamically load the image
        logo = CTkImage(Image.open("HR Employee Management System.png"), size=(800, 200))
        logo_label = CTkLabel(ems_window, image=logo, text='')
        logo_label.image = logo  # Prevent garbage collection
        logo_label.pack(pady=20)
    except Exception as e:
        Label(ems_window, text=f"Error loading logo: {e}", font=("Arial", 14)).pack(pady=20)

    Label(ems_window, text="Welcome to the ems System", font=("Arial", 16)).pack(pady=20)



def open_main():
    window = Tk()
    window.resizable(0,0)
    window.geometry("1590x840+100+100")
    window.state('normal')
    window.title("Resume Parser Page")
# window.attributes('-fullscreen',True)
    window.configure(bg="#FFFFFF")
#load the English language model of SpaCy and initialize a matcher object.
nlp = spacy.load('en_core_web_sm')
matcher = Matcher(nlp.vocab)

import os
import docx2txt
from tkinter import filedialog, Tk
from PyPDF2 import PdfReader

def extract_text_from_doc():
    """
    Opens a file dialog for the user to select a file. Extracts text from DOCX, PDF, or TXT files.
    """
    root = Tk()
    root.withdraw()  # Hide the main Tkinter window
    file_path = filedialog.askopenfilename(filetypes=[
        ("All Supported Files", "*.docx *.pdf *.txt"),
        ("DOCX Files", "*.docx"),
        ("PDF Files", "*.pdf"),
        ("Text Files", "*.txt")
    ])
    
    if file_path:
        file_extension = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_extension == '.docx':
                # Handle DOCX files
                try:
                    temp = docx2txt.process(file_path)
                    text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
                    return ' '.join(text)
                except Exception as e:
                    print(f"Error processing DOCX file: {e}")
                    return None

            elif file_extension == '.pdf':
                # Handle PDF files
                try:
                    reader = PdfReader(file_path)
                    text = ""
                    for page in reader.pages:
                        extracted_text = page.extract_text()
                        if extracted_text:
                            text += extracted_text
                    if text.strip() == "":
                        print("No text extracted from the PDF file. It may be a scanned document or use a non-standard encoding.")
                    return text
                except Exception as e:
                    print(f"Error processing PDF file: {e}")
                    return None

            elif file_extension == '.txt':
                # Handle TXT files
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        text = file.read()
                    return text
                except Exception as e:
                    print(f"Error reading TXT file: {e}")
                    return None
            
            else:
                print(f"Unsupported file format: {file_extension}")
                return None

        except Exception as e:
            print(f"Error processing file: {e}")
            return None
    else:
        print("No file selected.")
        return None


# def extract_text_from_doc():
#     """
#     Opens a file dialog for the user to select a file. Extracts text from DOCX, PDF, or TXT files.
#     """
#     root = Tk()
#     root.withdraw()  # Hide the main Tkinter window
#     file_path = filedialog.askopenfilename(filetypes=[
#         ("All Supported Files", "*.docx *.pdf *.txt"),
#         ("DOCX Files", "*.docx"),
#         ("PDF Files", "*.pdf"),
#         ("Text Files", "*.txt")
#     ])
    
#     if file_path:
#         file_extension = os.path.splitext(file_path)[1].lower()
        
#         try:
#             if file_extension == '.docx':
#                 # Handle DOCX files
#                 temp = docx2txt.process(file_path)
#                 text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
#                 return ' '.join(text)

#             elif file_extension == '.pdf':
#                 # Handle PDF files
#                 reader = PdfReader(file_path)
#                 text = ""
#                 for page in reader.pages:
#                     text += page.extract_text()  # Extract text from each page
#                 return text

#             elif file_extension == '.txt':
#                 # Handle TXT files
#                 with open(file_path, 'r', encoding='utf-8') as file:
#                     text = file.read()
#                 return text
            
#             else:
#                 print(f"Unsupported file format: {file_extension}")
#                 return None

#         except Exception as e:
#             print(f"Error processing file: {e}")
#             return None
#     else:
#         print("No file selected.")
#         return None


#The pattern looks for two consecutive proper nouns (names).
# If a match is found, it returns the matched span as the name.
import spacy

nlp = spacy.load('en_core_web_sm')

def extract_name(resume_text):
    doc = nlp(resume_text)

    # First try: Use Named Entity Recognition (NER)
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            return ent.text

    # Fallback: Use proper noun pattern in first few lines only
    lines = resume_text.split('\n')[:5]  # Only first 5 lines
    for line in lines:
        doc_line = nlp(line)
        tokens = [token for token in doc_line if token.pos_ == 'PROPN']
        if len(tokens) >= 2:
            return ' '.join([token.text for token in tokens[:2]])

    return "Name not found"


# It uses a regular expression pattern to find phone numbers in various formats.
# If a match is found, it returns the formatted phone number.
# def extract_mobile_number(text):
#     phone = re.findall(re.compile(
#         r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'),
#                        text)
#     if phone:
#         number = ''.join(phone[0])
#         if len(number) >= 10:
#             return '+' + number
#         else:
#             return number
def extract_mobile_number(text):
    # Look for a 10-digit number possibly with country code (+91)
    pattern = re.compile(r'(?:\+91[\-\s]?)?[6-9]\d{9}')
    matches = pattern.findall(text)
    
    if matches:
        # Return the first match with +91 prefix if not already present
        number = matches[0]
        if not number.startswith('+91'):
            number = '+91' + number[-10:]
        return number
    return None

#It uses a regular expression pattern to find email addresses.
# If a match is found, it returns the email address.
def extract_email(email):
    email = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", email)

    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None


def extract_skills(resume_text):
    nlp_text = nlp(resume_text)
    tokens = [token.text for token in nlp_text if not token.is_stop]
    data = pd.read_csv(r'C:\Users\simra\Desktop\DSA starting\Resume-Parser-Using-AI\skills.csv')
    skills = list(data.columns.values)
    skillset = []
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)
    for token in nlp_text.noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)
    return [i.capitalize() for i in set([i.lower() for i in skillset])]




globalvariable="hello"
def upload_document():
    global globalvariable
    try:
        # Extract text from uploaded document
        resume_text = extract_text_from_doc()
        if not resume_text:
            raise ValueError("No text extracted from the document.")
        resume_text = resume_text.lower()

        # Extract details from resume
        name = extract_name(resume_text) or "Name not found"
        mobile_number = extract_mobile_number(resume_text) or "Mobile number not found"
        email = extract_email(resume_text) or "Email not found"
        skills_user = extract_skills(resume_text)

        # Load dataset for job matching
        try:
            skills_data = pd.read_csv(r'C:\Users\simra\Desktop\DSA starting\Resume-Parser-Using-AI\ParSight_Dataset_merged(Updated).csv')
            if 'SKILLS' not in skills_data.columns:
                raise ValueError("The dataset does not contain a 'SKILLS' column.")
        except FileNotFoundError:
            raise FileNotFoundError("The specified dataset file was not found.")
        
        # Calculate similarity scores
        skills_user_str = ' '.join(skills_user)
        vectorizer = TfidfVectorizer()
        skills_job_vectorized = vectorizer.fit_transform(skills_data['SKILLS'])
        skills_user_vectorized = vectorizer.transform([skills_user_str])
        similarities = cosine_similarity(skills_user_vectorized, skills_job_vectorized)[0]

        # Add similarity scores to the dataset
        skills_data['similarity'] = similarities * 100
        sorted_jobs = skills_data.sort_values('similarity', ascending=False)
        num_jobs = 5  # Number of top matching jobs to retrieve
        top_jobs = sorted_jobs.head(num_jobs)
        top_jobs['similarity'] = top_jobs['similarity'].apply(lambda x: f'{x:.2f}%')

        # Update GUI labels with extracted information
        name_label.config(text=f"Name: {name}")
        mobile_label.config(text=f"Mobile number: {mobile_number}")
        email_label.config(text=f"Email: {email}")
        skills_label.config(text=f"Skills: {', '.join(skills_user)}")
        top_jobs_table = top_jobs[['JOBS', 'similarity']].to_string(index=False, header=False)
        top_jobs_label.config(text=f"Top Matching Jobs:\n\n{top_jobs_table}")

        # Send email with top jobs (if email is valid)
        if email != "Email not found":
            send_email(email, top_jobs)
        else:
            print("No valid email address found. Email not sent.")

        print("Resume text processed successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

def candidate_selection():
    """
    Functionality for the Candidate Selection button.
    Uses a condition to load and display the ems system UI.
    """
    condition = True
    if condition:
        try:
            subprocess.Popen(["python","ems.py"])
        except ImportError:
            messagebox.showerror("Error", "ems module not found. Ensure ems.py is in the correct location.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")



  



window = Tk()
window.resizable(0,0)
window.geometry("1400x700")
window.state('zoomed')
window.title("Resume Parser Page")
# window.attributes('-fullscreen',True)
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#EAF3FA",
    height=1100,
    width=1590,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)


image = Image.open("resume.png")
image_resized = image.resize((1400, 200))
logo = ImageTk.PhotoImage(image_resized)

# Create and place the Label
logo_label = Label(window, image=logo)
logo_label.grid(row=0, column=0)



upload_button_image = PhotoImage(file=r"C:\Users\simra\Desktop\DSA starting\Resume-Parser-Using-AI\Modifiedproject\button_1.png")
upload_button = Button(
    image=upload_button_image,
    command=upload_document,
    relief="flat",
    highlightbackground="#EAF3FA",
    highlightcolor="#EAF3FA"

)

upload_button.place(x=23.0, y=700, width=194.0, height=47.0)


def send_email(email, top_jobs):
    quoted_mail = f'{email}'
    sender_email = 'anjum2022@acem.edu.in'
    receiver_email = quoted_mail
    subject = 'Top Job Matches for You'
    
    # Prepare the email message
    try:
        message = "The top jobs for you are:\n\n" + top_jobs[['JOBS', 'similarity']].to_string(index=False, header=False)
    except Exception as e:
        print(f"Error creating email content: {e}")
        message = "We encountered an issue generating job recommendations."

    # Create MIME message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # SMTP Server Details
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    username = sender_email
    password = '@crfd oodd zhqf xfje'  # Replace with the generated app password

    try:
        # Connect to the SMTP server and send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Start TLS encryption
            server.login(username, password)  # Login with app password
            server.sendmail(sender_email, receiver_email, msg.as_string())  # Send the email
        print('Email sent successfully!')
        email_sent_label.config(text="Email sent successfully!")  # Update GUI label with success message
    except smtplib.SMTPAuthenticationError as e:
        print(f"Authentication Error: {e}")
        email_sent_label.config(text="Authentication Error: Check credentials.")  # Update GUI label with error message
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")
        email_sent_label.config(text="Error sending email.")  # Update GUI label with error message
    except Exception as e:
        print(f"Unexpected error: {e}")
        email_sent_label.config(text="Unexpected error occurred.")  # Update GUI label with error message

    email_sent_label.place(x=70.0, y=650.0, width=400, height=20)

candidate_button = Button(
    window,
    text="Candidate Selection",
    font=("Arial", 15, "bold"),
    bg="black",
    fg="white",
    command=candidate_selection,  # Calls the candidate selection function
    relief="raised",
    cursor="hand2"
)

# Place the button at the bottom-right corner
candidate_button.place(x=1200, y=700, width=194, height=47)


name_label = Label(window, text="Name:", font=("Inter Regular", 12))
name_label.place(x=23.0,y=350.0,anchor="nw") 

mobile_label = Label(window, text="Mobile number:", font=("Inter Regular", 12))
mobile_label.place(x=23.0, y=380.0, anchor="nw")

email_label = Label(window, text="Email:", font=("Inter Regular", 12))
email_label.place(x=23.0, y=420.0, anchor="nw")

skills_label = Label(window, text="Skills:", font=("Inter Regular", 12))
skills_label.place(x=23.0, y=450.0, anchor="nw")

top_jobs_label = Label(window, text="Top Matching Jobs:", font=("Inter Regular", 12))
top_jobs_label.place(x=23.0, y=480.0, anchor="nw")

email_sent_label = Label(window, text="", font=("Inter Regular", 12), fg="green")
email_sent_label.place(x=23.0, y=630.0, anchor="nw")

send_email_button = Button(window, text="Email Status", font=("Arial", 12), bg="black", fg="white", command=send_email)
send_email_button.place(x=23.0,y=650,anchor="nw")

window.mainloop()

