from tkinter import Tk, Label
from PIL import Image, ImageTk  # Import from Pillow
import time
import subprocess

def transition():  
    # Simulate loading time
    time.sleep(3)  # Wait for 3 seconds
    root.destroy()
    # Launch the main file
    subprocess.Popen(["python", "main.py"])

root = Tk()
root.title("Loading")

# Center the window on the screen
window_width = 600
window_height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.configure(bg="white")

# Add the image
image = Image.open(r"C:\Users\HP\Downloads\sasa1-31.jpg")  # Replace with the path to your JPEG image
image = image.resize((500, 400))  # Resize the image to fit the window
photo = ImageTk.PhotoImage(image)

image_label = Label(root, image=photo, bg="white")
image_label.pack(pady=(20, 10))  # Add padding to position the image

# Add the "Please Wait..." text
text_label = Label(root, text="Please Wait...", font=("Arial", 18), bg="white")
text_label.pack()

# Start the transition in a non-blocking way
root.after(100, transition)

root.mainloop()






