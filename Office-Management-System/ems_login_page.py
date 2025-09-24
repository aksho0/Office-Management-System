from customtkinter import *
from PIL import Image, UnidentifiedImageError
from tkinter import messagebox
import database

#--------EMPLOYEE AUTHENTICATION------------
def fetch_emp_data(emp_id):
    conn = database.db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            if emp_id:
                query = 'SELECT name FROM ems_db WHERE id = %s'
                cursor.execute(query, (emp_id,))
                result = cursor.fetchone()
                if result:
                    return result[0]
                else:
                    messagebox.showinfo('Info', 'No employee found with this ID.')
                    return None
            else:
                messagebox.showerror('Error', 'Invalid employee ID provided.')
                return None
        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror('Error', f'An error occurred:\n{e}')
            return None
        finally:
            cursor.close()
            conn.close()
    else:
        messagebox.showerror('Error', 'Connection Error while fetching data')
        return None
        
#------------LOGIN AUTHENTICATION---------------
def login():
    username = username_entry.get()
    password = password_entry.get()
    
    if not username or not password:
        messagebox.showerror('Error', 'All fields are required')
    elif username == 'admin123' and password == '12345':
        root.destroy()
        import ems_admin_page
        # import admin_choice_page
    else:
        username1 = fetch_emp_data(password)

        if username == username1:
            database.log_employee_attendance(username) 
            root.destroy()
            import emplyoee_page
            return username
        else:
            messagebox.showerror('Error', 'Wrong credentials')

#-------------LOADING BACKGROUND--------------
def load_background_image():
    try:
        return CTkImage(Image.open('login_back_img.jpg'), size=(736, 417))
    except (FileNotFoundError, UnidentifiedImageError):
        messagebox.showerror("Error", "Background image not found.")
        return None

#------------GUI SETUP--------------
root = CTk()
root.geometry('736x417')
root.resizable(0, 0)
root.title('Login Page')

#--------BACKGROUND IMAGE------------
img = load_background_image()
if img:
    imageLabel = CTkLabel(root, image=img, text='')
    imageLabel.place(x=0, y=0)

#------------STYLING TWEAKS-----------
heading_font = ('Goudy Old Style', 28, 'bold')  # Larger heading font
label_font = ('Verdana', 14)  # Improved font size for labels
entry_width = 240
button_width = 100

#-------------HEADING-------------------
heading = CTkLabel(root, text="Office Management System", 
                   font=heading_font, text_color='#553e74', bg_color="#FFFFFF")
heading.place(x=200, y=50)

#-------------USERNAME ENTRY--------------
username_label = CTkLabel(root, text="Username:", font=label_font, text_color="#333333", bg_color="#FFFFFF")
username_label.place(x=200, y=120)

username_entry = CTkEntry(root, placeholder_text='Enter Your Username',
                          width=entry_width, corner_radius=10, fg_color="#ffffff", text_color="#333333", bg_color="#FFFFFF")
username_entry.place(x=200, y=150)

#----------PASSWORD ENTRY----------------
password_label = CTkLabel(root, text="Password:", font=label_font, text_color="#333333", bg_color="#FFFFFF")
password_label.place(x=200, y=200)

password_entry = CTkEntry(root, placeholder_text='Enter Your Password',
                          width=entry_width, corner_radius=10, fg_color="#ffffff", text_color="#333333", show='*', bg_color="#FFFFFF")
password_entry.place(x=200, y=230)

#--------LOGIN BUTTON-------------------
login_button = CTkButton(root, text='Login', cursor='hand2', command=login, 
                         width=button_width, corner_radius=10, fg_color="#553e74", hover_color="#6e4b8b", bg_color="#FFFFFF")
login_button.place(x=270, y=280)

#--------RUNNING APP----------
root.mainloop()
