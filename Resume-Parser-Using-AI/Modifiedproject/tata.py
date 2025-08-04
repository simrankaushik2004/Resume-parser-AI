

import pymysql
from tkinter import messagebox

def conn_database():
    global mycursor, conn
    try:
        conn = pymysql.connect(host="localhost", user="root", password="Anjumbano12@#$%1")
        mycursor = conn.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS employee_data")
        mycursor.execute("USE employee_data")
        # Add 'Email' field to the table
        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS data(
                Id INT PRIMARY KEY,
                Name VARCHAR(50),
                Phone BIGINT,
                Role VARCHAR(62),
                Gender VARCHAR(50),
                Salary DECIMAL(10,2),
                Email VARCHAR(100)
            )
        """)
        messagebox.showinfo("Success", "Your database is connected successfully")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong. Try again later: {e}")
        return

def insert(id, name, phone, role, gender, salary, email):
    mycursor.execute("INSERT INTO data VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                     (id, name, phone, role, gender, salary, email))
    conn.commit()

def id_exists(id):
    mycursor.execute("SELECT COUNT(*) FROM data WHERE Id=%s", id)
    result = mycursor.fetchone()
    return result[0] > 0

def fetch_employees():
    mycursor.execute("SELECT * FROM data")
    result = mycursor.fetchall()
    return result

def update(id, new_name, new_phone, new_role, new_gender, new_salary, new_email):
    mycursor.execute("""
        UPDATE data 
        SET Name=%s, Phone=%s, Role=%s, Gender=%s, Salary=%s, Email=%s 
        WHERE Id=%s
    """, (new_name, new_phone, new_role, new_gender, new_salary, new_email, id))
    conn.commit()

def delete(id):
    mycursor.execute("DELETE FROM data WHERE Id=%s", id)
    conn.commit()

def search(option, value):
    mycursor.execute(f"SELECT * FROM data WHERE {option}=%s", (value,))
    result = mycursor.fetchall()
    return result

def deleteall_records():
    mycursor.execute("TRUNCATE TABLE data")
    conn.commit()

conn_database()