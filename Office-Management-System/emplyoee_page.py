from customtkinter import *
from tkinter import messagebox, ttk
import datetime
import mysql.connector
import database

# GUI Application Setup
app = CTk()
app.geometry("600x450")
app.title("Office Management System")
set_appearance_mode("light")  # Use dark mode consistently

# Function to show frame
def show_frame(frame):
    frame.tkraise()

# Get logged-in employee name (simulate for now)
logged_in_user = "employee1"  # This should be passed from login

#--------------------FUNCTIONS---------------
def apply_leave():
    name = leave_name_entry.get()
    leave_reason = reason_entry.get("1.0", "end").strip()
    if not name or not leave_reason:
        messagebox.showerror("Error", "Please fill all the fields.")
        return
    messagebox.showinfo("Success", "Leave application submitted successfully.")
    leave_name_entry.delete(0, "end")
    reason_entry.delete("1.0", "end")

def show_notice():
    conn = database.db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM notice")
        notice = cursor.fetchone()
        if notice:
            messagebox.showinfo("Notice Board", f"📢 Today's Notice:\n\n{notice[0]}")
        else:
            messagebox.showinfo("Notice Board", "No notice available.")
        conn.close()

# Frames
app.rowconfigure(0, weight=1)
app.columnconfigure(0, weight=1)

home_frame = CTkFrame(app)
attendance_frame = CTkFrame(app)
leave_frame = CTkFrame(app)
notice_frame = CTkFrame(app)

for frame in (home_frame, attendance_frame, leave_frame, notice_frame):
    frame.grid(row=0, column=0, sticky="nsew")

# HOME FRAME
CTkLabel(home_frame, text="Employee Dashboard", font=("Arial", 24, "bold")).pack(pady=20)
CTkButton(home_frame, text="🕒 Attendance log", width=250, height=45, font=("Arial", 16), command=lambda: show_frame(attendance_frame)).pack(pady=10)
CTkButton(home_frame, text="📝 Apply for Leave", width=250, height=45, font=("Arial", 16), command=lambda: show_frame(leave_frame)).pack(pady=10)
CTkButton(home_frame, text="📢 View Notice", width=250, height=45, font=("Arial", 16), command=show_notice).pack(pady=10)

# ATTENDANCE FRAME
CTkLabel(attendance_frame, text="Your Attendance Log", font=("Arial", 24, "bold")).pack(pady=20)

# Attendance Summary Label
attendance_summary_label = CTkLabel(attendance_frame, text="", font=("Arial", 16))
attendance_summary_label.pack(pady=5)

# Treeview to show attendance log
tree_frame = CTkFrame(attendance_frame)
tree_frame.pack(pady=20)

tree = ttk.Treeview(tree_frame, columns=("Name", "Timestamp"), show="headings", height=10)
tree.heading("Name", text="Employee Name")
tree.heading("Timestamp", text="Date & Time")
tree.pack()

# Back button
CTkButton(attendance_frame, text="Back", command=lambda: show_frame(home_frame)).pack(pady=10)

# Fetch attendance for logged-in user
def load_attendance():
    tree.delete(*tree.get_children())
    conn = database.db_connection()
    if conn:
        cursor = conn.cursor()
        logged_in_user = "Rakhi"
        cursor.execute("SELECT emp_name, time FROM attendance_log WHERE emp_name = %s", (logged_in_user,))
        records = cursor.fetchall()

        total_days = 200
        days_logged_in = len(set(record[1].date() for record in records))

        for rec in records:
            tree.insert("", "end", values=rec)

        attendance_summary_label.configure(
            text=f"📅 Logged in on {days_logged_in + 1} out of {total_days} working days."
        )
        conn.close()

# Show attendance when frame is visible
attendance_frame.bind("<Visibility>", lambda e: load_attendance())

# LEAVE FRAME
CTkLabel(leave_frame, text="Apply for Leave", font=("Arial", 24, "bold")).pack(pady=20)
leave_name_entry = CTkEntry(leave_frame, placeholder_text="Your Name", width=300)
leave_name_entry.pack(pady=10)
reason_entry = CTkTextbox(leave_frame, width=300, height=100)
reason_entry.pack(pady=10)
CTkButton(leave_frame, text="Submit Leave Application", command=lambda: apply_leave()).pack(pady=10)
CTkButton(leave_frame, text="Back", command=lambda: show_frame(home_frame)).pack(pady=10)

# Show default frame
show_frame(home_frame)

app.mainloop()



# from customtkinter import *
# from tkinter import messagebox, ttk
# import datetime
# import database

# # ----------------- BASIC SETUP -----------------
# set_appearance_mode("light")  # Dark mode by default
# set_default_color_theme("blue")  # Or try "blue", "dark-blue", etc.

# app = CTk()
# app.geometry("600x450")
# app.title("Employee Management System")

# # ----------------- FRAME HANDLER -----------------
# frames = {}
# def show_frame(name):
#     for frame in frames.values():
#         frame.place_forget()
#     frames[name].place(relwidth=1, relheight=1)

# # ----------------- GLOBAL DATA -----------------
# attendance_log = []
# leave_applications = []

# # ----------------- FRAME CREATOR -----------------
# def create_frame(name):
#     frame = CTkFrame(app, corner_radius=20, fg_color="transparent")
#     frames[name] = frame
#     return frame

# # ----------------- FUNCTIONALITY -----------------
# def mark_attendance():
#     name = name_entry.get()
#     if not name:
#         messagebox.showerror("Error", "Please enter your name to mark attendance.")
#         return
#     time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     attendance_log.append((name, time_now))
#     messagebox.showinfo("Success", f"Attendance marked for {name} at {time_now}")
#     name_entry.delete(0, "end")

# def view_attendance():
#     tree.delete(*tree.get_children())
#     for record in attendance_log:
#         tree.insert("", "end", values=record)

# def apply_leave():
#     name = leave_name_entry.get()
#     reason = reason_entry.get("1.0", "end").strip()
#     if not name or not reason:
#         messagebox.showerror("Error", "Please fill all the fields.")
#         return
#     leave_applications.append((name, reason))
#     messagebox.showinfo("Success", "Leave application submitted.")
#     leave_name_entry.delete(0, "end")
#     reason_entry.delete("1.0", "end")

# # def show_notice():
# #     notice_msg = "📢 Today's Notices:\n\n1. Team meeting at 4:00 PM\n2. Submit reports by EOD\n3. Office closed on Friday"
# #     messagebox.showinfo("Notice Board", notice_msg)

# def show_notice():
#     conn = database.db_connection()
#     if conn:
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM notice")
#         notice = cursor.fetchone()
#         if notice:
#             messagebox.showinfo("Notice Board", f"📢 Today's Notice:\n\n{notice[0]}")
#         else:
#             messagebox.showinfo("Notice Board", "No notice available.")
#         conn.close()

# # ----------------- HOME FRAME -----------------
# home = create_frame("home")

# CTkLabel(home, text="Employee Dashboard", font=("Arial", 32, "bold")).pack(pady=40)

# CTkButton(home, text="🕒 Attendance log", width=250, height=45, font=("Arial", 16), command=lambda: show_frame("attendance")).pack(pady=10)
# CTkButton(home, text="📝 Apply for Leave", width=250, height=45, font=("Arial", 16), command=lambda: show_frame("leave")).pack(pady=10)
# CTkButton(home, text="📢 View Notice", width=250, height=45, font=("Arial", 16), command=show_notice).pack(pady=10)

# # ----------------- ATTENDANCE FRAME -----------------
# attendance = create_frame("attendance")

# CTkLabel(attendance, text="Mark Attendance", font=("Arial", 28, "bold")).pack(pady=30)

# name_entry = CTkEntry(attendance, placeholder_text="Enter your name", width=300)
# name_entry.pack(pady=10)

# CTkButton(attendance, text="Submit", command=mark_attendance).pack(pady=5)
# CTkButton(attendance, text="View Attendance Log", command=view_attendance).pack(pady=5)

# tree_frame = CTkFrame(attendance, fg_color="transparent")
# tree_frame.pack(pady=20)

# tree = ttk.Treeview(tree_frame, columns=("Name", "Timestamp"), show="headings", height=5)
# tree.heading("Name", text="Employee Name")
# tree.heading("Timestamp", text="Date & Time")
# tree.pack()

# CTkButton(attendance, text="⬅ Back", command=lambda: show_frame("home")).pack(pady=15)

# # ----------------- LEAVE FRAME -----------------
# leave = create_frame("leave")

# CTkLabel(leave, text="Leave Application", font=("Arial", 28, "bold")).pack(pady=30)

# leave_name_entry = CTkEntry(leave, placeholder_text="Enter your name", width=300)
# leave_name_entry.pack(pady=10)

# reason_entry = CTkTextbox(leave, width=300, height=100)
# reason_entry.pack(pady=10)

# CTkButton(leave, text="Submit Leave", command=apply_leave).pack(pady=10)
# CTkButton(leave, text="⬅ Back", command=lambda: show_frame("home")).pack(pady=10)

# # ----------------- RUN APP -----------------
# show_frame("home")
# app.mainloop()

