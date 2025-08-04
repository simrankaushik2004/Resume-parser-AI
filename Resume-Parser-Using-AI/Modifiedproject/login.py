from tkinter import Tk, Label, Entry, Button, messagebox,Canvas
from PIL import Image, ImageTk
import subprocess


def login():
    if userentry.get() == '' or passwordentry.get() == "":
        messagebox.showerror("Error", "Can't Login because you did not fill any field.") 
    elif userentry.get() == "Simran" and passwordentry.get() =="9999":
        messagebox.showinfo("Success", "You logged in successfully, go ahead.")
        root.destroy()
        subprocess.Popen(["python", "intermediate.py"])
        # import main
        # main.open_main()
        
    else:
        messagebox.showerror("Error", "Wrong credentials")
def on_click(event, entry, placeholder_text):
    """Remove the placeholder text when the user clicks inside the entry field."""
    if entry.get() == placeholder_text:
        entry.delete(0, "end")

def on_focusout(event, entry, placeholder_text):
    """Restore the placeholder text when the user leaves the entry field."""
    if entry.get() == "":
        entry.insert(0, placeholder_text)     
root = Tk()
root.geometry('860x605')
root.resizable(0, 1)
root.title("HR Login Page")

logo = Image.open("img3.png")
logo = logo.resize((532, 322))  # Resize image to fit the label
logo = ImageTk.PhotoImage(logo)
logoLabel = Label(root, image=logo)
logoLabel.place(x=260, y=100)

heading_label = Label(
    root,
    text="Resume Portal -- Parse and Analyze Resumes!",
    font=("Arial", 25, 'bold'),
)
heading_label.place(relx=0.5, rely=0.1, anchor="center")  # Center the label horizontally

# Create the canvas for the line
canvas = Canvas(root, width=600, height=2, bg="white", bd=0, highlightthickness=0)
canvas.create_line(0, 1, 600, 1, fill="black", width=2)  # Horizontal line across the canvas
canvas.place(relx=0.5, rely=0.15, anchor="center")

placeholder_text = "Enter your Username"
placeholder_text1 = "Enter your Password"

# Create the username entry field
userentry = Entry(root, font=("Arial", 14), width=25)  # Use font to set text style
userentry.insert(0, placeholder_text)  # Insert placeholder text
userentry.place(x=50, y=150,width=250,height=30)

# Create the password entry field
passwordentry = Entry(root, font=("Arial", 14), width=25, show="*")  # show="*" to hide password
passwordentry.insert(0, placeholder_text1)  # Insert placeholder text
passwordentry.place(x=50, y=200,width=250,height=30)

# Bind events to handle focus behavior
userentry.bind("<FocusIn>", lambda event: on_click(event, userentry, placeholder_text))
userentry.bind("<FocusOut>", lambda event: on_focusout(event, userentry, placeholder_text))
passwordentry.bind("<FocusIn>", lambda event: on_click(event, passwordentry, placeholder_text1))
passwordentry.bind("<FocusOut>", lambda event: on_focusout(event, passwordentry, placeholder_text1))

root.bind("<Return>", lambda event: login())
# Create the login button
loginButton = Button(root, text="Login", font=("Arial", 14), cursor="hand2",fg="white", bg="black",command=login)
loginButton.place(x=100, y=260,width=150,height=40)
root.mainloop()




