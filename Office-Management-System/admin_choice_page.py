import customtkinter as ctk
from tkinter import messagebox
from database import db_connection, add_notice  # ✅ Your own DB functions

# 🖥️ GUI Setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("600x400")
root.resizable(False, False)
root.title("Admin Dashboard")

ctk.CTkLabel(root, text="Admin Dashboard", font=("Goudy Old Style", 28, "bold")).pack(pady=30)

# 🔗 Open Admin Page
def open_admin_page():
    root.destroy()
    import ems_admin_page

# 📊 View Attendance Log (from MySQL)
def open_attendance_log():
    log_window = ctk.CTkToplevel()
    log_window.title("Attendance Log")
    log_window.geometry("600x400")
    log_window.configure(bg='#2b2b2b')

    text_box = ctk.CTkTextbox(log_window, width=560, height=300)
    text_box.pack(pady=20)

    conn = db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT emp_id, date, status FROM attendance")
        records = cursor.fetchall()
        if records:
            for rec in records:
                text_box.insert("end", f"Employee ID: {rec[0]}, Date: {rec[1]}, Status: {rec[2]}\n")
        else:
            text_box.insert("end", "No attendance records found.")
        conn.close()
    else:
        messagebox.showerror("Error", "Database connection failed")

# 📢 Update Notice
def update_notice_frame():
    notice_window = ctk.CTkToplevel()
    notice_window.title("Update Notice")
    notice_window.geometry("500x300")
    notice_window.configure(bg='#2b2b2b')

    label = ctk.CTkLabel(notice_window, text="Enter new notice:")
    label.pack(pady=10)

    notice_entry = ctk.CTkTextbox(notice_window, height=100, width=450)
    notice_entry.pack(pady=10)

    # Optional: Preload last notice
    conn = db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM notice ORDER BY id DESC LIMIT 1")
        last_notice = cursor.fetchone()
        if last_notice:
            notice_entry.insert("1.0", last_notice[0])
        conn.close()

    def save_notice():
        new_notice = notice_entry.get("1.0", "end").strip()
        if new_notice:
            try:
                add_notice((new_notice,))  # assuming your table has 1 column (content)
                label.configure(text="Notice updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save notice: {e}")

    ctk.CTkButton(notice_window, text="Save Notice", command=save_notice).pack(pady=10)

# 🎛️ Buttons
ctk.CTkButton(root, text="Manage Employee Data", width=250, height=40, command=open_admin_page).pack(pady=15)
ctk.CTkButton(root, text="View Attendance Log", width=250, height=40, command=open_attendance_log).pack(pady=15)
ctk.CTkButton(root, text="Update Notice", width=250, height=40, command=update_notice_frame).pack(pady=15)

# 🚀 Run App
root.mainloop()
