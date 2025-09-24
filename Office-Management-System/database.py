import pymysql
from tkinter import messagebox
from mysql.connector import Error
import datetime

def db_connection():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='3012#Tae',
            database="python_workshop"
        )
        return conn
    except:
        messagebox.showerror('Error', 'Somthing went wrong. Please open mysql before running')
        return None

def insert(id_entry, name, phone, role, gender, salary):
    conn = db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO ems_db (id, name, phone, role, gender, salary) values(%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (id_entry, name, phone, role, gender, salary))
            conn.commit()
            conn.close()
        except Exception as e:
            if isinstance(e, Error) and e.errno == 1062:  # Check MySQL error 1062 for duplicate entry
                messagebox.showerror("Error", "Id already exist")
            else:
                messagebox.showerror("Database Error", f"Error: {e}")

def fetch_emp():
    conn = db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('select * from ems_db')
        data = cursor
        return data
    else:
        messagebox.showerror('Error', 'Connection Error while fectching data')
    
def update(id, new_name, new_phone, new_role, new_gender, new_salary):
    conn = db_connection()
    if conn:
        cursor = conn.cursor()
        query = 'UPDATE ems_db SET name=%s, phone=%s, role=%s, gender=%s, salary=%s WHERE id=%s'
        cursor.execute(query,(new_name, new_phone, new_role, new_gender, new_salary, id))
        conn.commit()
        conn.close()
    else:
        messagebox.showerror('Error', 'Connection Error while updating data')

def delete(id):
    conn = db_connection()
    if conn:
        cursor = conn.cursor()
        query = 'DELETE FROM ems_db WHERE id=%s'
        cursor.execute(query, id)
        conn.commit()
        conn.close()
    else:
        messagebox.showerror('Error', 'Connection Error while deleting data')


def search(option, val):
    conn = db_connection()
    if conn:
        cursor = conn.cursor()
        query = f'SELECT * FROM ems_db WHERE {option}=%s'
        cursor.execute(query, val)
        searched_data = cursor.fetchall()
        conn.commit()
        conn.close()
        return searched_data
    else:
        messagebox.showerror('Error', 'Connection Error while searching data')

def delete_all_records():
        conn = db_connection()
        if conn:
            cursor = conn.cursor()
            query = 'TRUNCATE TABLE ems_db'
            cursor.execute(query)
            conn.commit()
            conn.close()
        else:
            messagebox.showerror('Error', 'Connection Error while deleting all the records')

def add_notice(notice):
    conn = db_connection()
    if conn:
        cursor = conn.cursor()
        query = f'INSERT INTO notice VALUES {notice}'
        cursor.execute(query)
        conn.commit()
        conn.close()
    else:
        messagebox.showerror('Error', 'Notice did not get updated')

def log_employee_attendance(emp_name):
    conn = db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("INSERT INTO attendance_log (emp_name, time) VALUES (%s, %s)", (emp_name, now))
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to log attendance: {e}")
    else:
        messagebox.showerror("Error", "Database connection failed")
