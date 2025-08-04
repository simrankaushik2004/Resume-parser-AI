import pymysql
from tkinter import messagebox

def connect_database():
    global conn, mycursor
    try:
        conn = pymysql.connect(host="localhost", user="root", password="shyam@8764")
        mycursor = conn.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS jj")
        mycursor.execute("USE jj")
        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS inoj(
                ID INT PRIMARY KEY,
                Name VARCHAR(50),
                Mobile_Number BIGINT,
                Email VARCHAR(100),
                Role VARCHAR(20),
                Gender VARCHAR(20),
                Salary DECIMAL(10,2)
            )
        """)
        messagebox.showinfo("Success", "Database connected successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Database connection failed:\n{e}")

# ✅ Accepts ID as parameter now (7 args total)
def insert(ID, Name, Mobile_Number, Email, Role, Gender, Salary):
    try:
        mycursor.execute("""
            INSERT INTO inoj (ID, Name, Mobile_Number, Email, Role, Gender, Salary)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (ID, Name, Mobile_Number, Email, Role, Gender, Salary))
        conn.commit()
    except pymysql.err.IntegrityError:
        messagebox.showerror("Error", f"Employee with ID {ID} already exists.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def insert_with_id(ID, Name, Mobile_Number, Email, Role, Gender, Salary):
    # Same as insert() since we always use ID
    insert(ID, Name, Mobile_Number, Email, Role, Gender, Salary)

def fetch_employees():
    mycursor.execute("SELECT * FROM inoj")
    return mycursor.fetchall()

def update(ID, Name, Mobile_Number, Email, Role, Gender, Salary):
    mycursor.execute("""
        UPDATE inoj SET
            Name = %s,
            Mobile_Number = %s,
            Email = %s,
            Role = %s,
            Gender = %s,
            Salary = %s
        WHERE ID = %s
    """, (Name, Mobile_Number, Email, Role, Gender, Salary, ID))
    conn.commit()

def delete(ID):
    mycursor.execute("DELETE FROM inoj WHERE ID = %s", (ID,))
    conn.commit()

def deleteall_records():
    mycursor.execute("TRUNCATE TABLE inoj")
    conn.commit()

def Search(option, value):
    field_map = {
        "ID": "ID",
        "Name": "Name",
        "Mobile Number": "Mobile_Number",
        "Email": "Email",
        "Role": "Role",
        "Gender": "Gender",
        "Salary": "Salary"
    }
    column = field_map.get(option)
    if column:
        mycursor.execute(f"SELECT * FROM inoj WHERE {column} = %s", (value,))
        return mycursor.fetchall()
    return []

def id_exists(ID):
    mycursor.execute("SELECT COUNT(*) FROM inoj WHERE ID = %s", (ID,))
    return mycursor.fetchone()[0] > 0

# ⚠️ Always call this on import to ensure DB is ready
connect_database()
