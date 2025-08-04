from customtkinter import *
from PIL import Image
from tkinter import ttk, messagebox
import data 
import csv
from tkinter import filedialog


def upload_picture():
    file_path = filedialog.askopenfilename(filetypes=[("image files", "*.jpg *.png")])
    if file_path:
        profile_img = CTkImage(Image.open(file_path), size=(150, 150))
        profileImgLabel.configure(image=profile_img)
        profileImgLabel.image = profile_img


def export_to_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Mobile Number", "Email", "Role", "Gender", "Salary"])

        for row in tree.get_children():
            row_data = tree.item(row)["values"]
            writer.writerow(row_data)

    messagebox.showinfo("Export Successful", f"Data exported successfully to {file_path}")


def import_from_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            data.insert_with_id(*row)

        treeview_data()
        messagebox.showinfo("Import Successful", f"Data imported successfully from {file_path}")


def delete_all():
    result = messagebox.askyesno("Confirm", "Do you really want to delete all the records?")
    if result:
        data.deleteall_records()
        treeview_data()


def show_all():
    treeview_data()
    SearchEntry.delete(0, END)
    SearchBox.set("Search By")


def search_employee():
    if SearchEntry.get() == "":
        messagebox.showerror("Error", "Enter value to search")
    elif SearchBox.get() == "Search By":
        messagebox.showerror("Error", "Please select an option")
    else:
        search_data = data.Search(SearchBox.get(), SearchEntry.get())
        tree.delete(*tree.get_children())
        for employee in search_data:
            tree.insert("", END, values=employee)


def delete_employee():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Select data to delete")
    else:
        data.delete(IDEntry.get())
        treeview_data()
        clear()
        messagebox.showinfo("Success", "Data deleted")


def update_employee():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Select data to update")
    else:
        data.update(
            IDEntry.get(),
            nameEntry.get(),
            MobileNumberEntry.get(),
            EmailEntry.get(),
            RoleBox.get(),
            GenderBox.get(),
            SalaryEntry.get()
        )
        treeview_data()
        clear()
        messagebox.showinfo("Success", "Data updated")


def selection(event):
    selected_item = tree.selection()
    if selected_item:
        clear()
        row = tree.item(selected_item)["values"]
        IDEntry.insert(0, row[0])
        nameEntry.insert(0, row[1])
        MobileNumberEntry.insert(0, row[2])
        EmailEntry.insert(0, row[3])
        RoleBox.set(row[4])
        GenderBox.set(row[5])
        SalaryEntry.insert(0, row[6])


def treeview_data():
    employees = data.fetch_employees()
    tree.delete(*tree.get_children())
    for employee in employees:
        tree.insert("", END, values=employee)


def clear(value=False):
    if value:
        tree.selection_remove(tree.focus())
    IDEntry.delete(0, END)
    nameEntry.delete(0, END)
    MobileNumberEntry.delete(0, END)
    EmailEntry.delete(0, END)
    RoleBox.set("Administrator")
    GenderBox.set("MALE")
    SalaryEntry.delete(0, END)


def add_Employee():
    if IDEntry.get()=="" or nameEntry.get() == "" or MobileNumberEntry.get() == "" or EmailEntry.get() == "" or SalaryEntry.get() == "":
        messagebox.showerror("Error", "All fields are required")
    else:
        data.insert(
            IDEntry.get(),
            nameEntry.get(),
            MobileNumberEntry.get(),
            EmailEntry.get(),
            RoleBox.get(),
            GenderBox.get(),
            SalaryEntry.get()
        )
        treeview_data()
        clear()
        messagebox.showinfo("Success", "Data successfully added")


window = CTk()
window.geometry('1500x650+100+100')
window.title("Employee Management System")
window.resizable(0, 0)

logo = CTkImage(Image.open("resume.png"), size=(1098, 200))
logoLabel = CTkLabel(window, image=logo, text='')
logoLabel.grid(row=0, column=0, columnspan=2)

leftFrame = CTkFrame(window)
leftFrame.grid(row=1, column=0)

RightFrame = CTkFrame(window)
RightFrame.grid(row=1, column=1)

IDLabel = CTkLabel(leftFrame, text="ID", font=("Arial", 18, "bold"), padx=20, pady=15)
IDLabel.grid(row=0, column=0, sticky="w")
IDEntry = CTkEntry(leftFrame, font=("arial", 15, "bold"), width=180)
IDEntry.grid(row=0, column=1)

NameLabel = CTkLabel(leftFrame, text="Name", font=("Arial", 18, "bold"), padx=20, pady=15)
NameLabel.grid(row=1, column=0, sticky="w")
nameEntry = CTkEntry(leftFrame, font=("arial", 15, "bold"), width=180)
nameEntry.grid(row=1, column=1)

MobileNumberLabel = CTkLabel(leftFrame, text="Mobile Number", font=("Arial", 18, "bold"), padx=20, pady=15)
MobileNumberLabel.grid(row=2, column=0, sticky="w")
MobileNumberEntry = CTkEntry(leftFrame, font=("arial", 15, "bold"), width=180)
MobileNumberEntry.grid(row=2, column=1)

EmailLabel = CTkLabel(leftFrame, text="Email", font=("Arial", 18, "bold"), padx=20, pady=15)
EmailLabel.grid(row=3, column=0, sticky="w")
EmailEntry = CTkEntry(leftFrame, font=("arial", 15, "bold"), width=180)
EmailEntry.grid(row=3, column=1)

RoleLabel = CTkLabel(leftFrame, text="Role", font=("Arial", 18, "bold"), padx=20, pady=15)
RoleLabel.grid(row=4, column=0, sticky="w")

role_options = ["Administrator", "HR Manager", "Team Leader", "Supervisor", "Recruiter"]
RoleBox = CTkComboBox(leftFrame, values=role_options, width=180, font=("Arial", 14, "bold"), state="readonly")
RoleBox.grid(row=4, column=1)
RoleBox.set(role_options[0])

GenderLabel = CTkLabel(leftFrame, text="Gender", font=("Arial", 18, "bold"), padx=20, pady=15)
GenderLabel.grid(row=5, column=0, sticky="w")

Gender_options = ["MALE", "FEMALE", "OTHERS"]
GenderBox = CTkComboBox(leftFrame, values=Gender_options, width=180, font=("Arial", 14, "bold"), state="readonly")
GenderBox.grid(row=5, column=1)
GenderBox.set(Gender_options[0])

SalaryLabel = CTkLabel(leftFrame, text="Salary", font=("Arial", 18, "bold"), padx=20, pady=15)
SalaryLabel.grid(row=6, column=0, sticky="w")

SalaryEntry = CTkEntry(leftFrame, font=("arial", 15, "bold"), width=180)
SalaryEntry.grid(row=6, column=1)

Search_options = ["ID", "Name", "Mobile Number", "Email", "Role", "Gender", "Salary"]
SearchBox = CTkComboBox(RightFrame, values=Search_options, state="readonly")
SearchBox.grid(row=0, column=0)
SearchBox.set("Search By")

SearchEntry = CTkEntry(RightFrame)
SearchEntry.grid(row=0, column=1)

SearchButton = CTkButton(RightFrame, text="Search", cursor="hand2", width=100, command=search_employee)
SearchButton.grid(row=0, column=2)

ShowAllButton = CTkButton(RightFrame, text="Show All", cursor="hand2", width=100, command=show_all)
ShowAllButton.grid(row=0, column=3)

tree = ttk.Treeview(RightFrame, height=16)
tree.grid(row=1, column=0, columnspan=4)

tree['columns'] = ("ID", "Name", "Mobile Number", "Email", "Role", "Gender", "Salary")
tree.column("ID", width=60)
tree.column("Name", width=150)
tree.column("Mobile Number", width=150)
tree.column("Email", width=150)
tree.column("Role", width=130)
tree.column("Gender", width=80)
tree.column("Salary", width=100)

tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Mobile Number", text="Mobile Number")
tree.heading("Email", text="Email")
tree.heading("Role", text="Role")
tree.heading("Gender", text="Gender")
tree.heading("Salary", text="Salary")
tree.config(show="headings")

style = ttk.Style()
style.configure('Treeview.Heading', font=("Arial", 15, "bold"))
style.configure("Treeview", font=("Arial", 12, "bold"), background="#161C30", foreground="white")

Scrollbar = ttk.Scrollbar(RightFrame, orient=VERTICAL)
Scrollbar.grid(row=1, column=4, sticky="ns")

ButtonFrame = CTkFrame(window, fg_color="#161C30")
ButtonFrame.grid(row=2, column=0, columnspan=2, pady=30)

newButton = CTkButton(ButtonFrame, text="NEW EMPLOYEE", cursor="hand2", font=("arial", 15, "bold"), width=160, corner_radius=12, command=lambda: clear(True))
newButton.grid(row=0, column=0, pady=5)

AddButton = CTkButton(ButtonFrame, text="Add EMPLOYEE", cursor="hand2", font=("arial", 15, "bold"), width=160, corner_radius=12, command=add_Employee)
AddButton.grid(row=0, column=1, pady=5, padx=5)

UpdateButton = CTkButton(ButtonFrame, text="Update EMPLOYEE", cursor="hand2", font=("arial", 15, "bold"), width=160, corner_radius=12, command=update_employee)
UpdateButton.grid(row=0, column=2, pady=5, padx=5)

DeleteButton = CTkButton(ButtonFrame, text="Delete EMPLOYEE", cursor="hand2", font=("arial", 15, "bold"), width=160, corner_radius=12, command=delete_employee)
DeleteButton.grid(row=0, column=3, pady=5, padx=5)

DeleteAllButton = CTkButton(ButtonFrame, text="DeleteAll EMPLOYEE", cursor="hand2", font=("arial", 15, "bold"), width=160, corner_radius=12, command=delete_all)
DeleteAllButton.grid(row=0, column=4, pady=5, padx=5)

ExportButton = CTkButton(ButtonFrame, text="Export to CSV", cursor="hand2", font=("arial", 15, "bold"), width=160, corner_radius=12, command=export_to_csv)
ExportButton.grid(row=0, column=5, pady=5, padx=5)

ImportButton = CTkButton(ButtonFrame, text="Import from CSV", cursor="hand2", font=("arial", 15, "bold"), width=160, corner_radius=12, command=import_from_csv)
ImportButton.grid(row=0, column=6, pady=5, padx=5)

tree.bind("<ButtonRelease-1>", selection)
treeview_data()
window.mainloop()
