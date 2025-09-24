from customtkinter import *
from PIL import Image
from tkinter import messagebox
from tkinter import ttk
import database

#-------------FUNCTIONAL PART----------------------
def delete_all():
    res=messagebox.askyesno('Confirm', 'Do you really want to delete all the records?')
    if res:
        database.delete_all_records()
        clear()
        tree.delete(*tree.get_children())
    else:
        pass

def search_emp():
    if search_entry.get() =='':
        messagebox.showerror('Error', 'Enter value to search')
    elif search_box.get() == 'Search By':
        messagebox.showerror('Error', 'Please select some value')
    else:
        search_data=database.search(search_box.get(), search_entry.get())
        tree.delete(*tree.get_children())
        for employee in search_data:
            tree.insert('', END, values=employee)

def delete_emp():
    selected_item=tree.selection()
    if not selected_item:
        messagebox.showerror('Error', 'Select data to delete')
    else:
        database.delete(id_entry.get())
        tree_view()
        clear()
        messagebox.showerror('Error', 'Data is deleted')

def update_emp():
    selected_item=tree.selection()
    if not selected_item:
        messagebox.showerror('Error', 'Select data to update')
    else:
        database.update(id_entry.get(), name_entry.get(), phone_entry.get(), role_box.get(), gender_box.get(), salary_entry.get())
        tree_view()
        clear()
        messagebox.showinfo('Success', 'Data is updated')

def selection(event):
    selected_item = tree.selection()
    if selected_item:
        clear()
        row = tree.item(selected_item)['values']
        id_entry.insert(0, row[0])
        name_entry.insert(0, row[1])
        phone_entry.insert(0, row[2])
        salary_entry.insert(0, row[5])
        role_box.set(row[3])
        gender_box.set(row[4])

def clear(value=False):
    if value:
        tree.selection_remove(tree.focus())
    id_entry.delete(0, END)
    name_entry.delete(0, END)
    phone_entry.delete(0, END)
    role_box.set('Web Developer')
    gender_box.set('Male')
    salary_entry.delete(0, END)

def tree_view():
    emp = database.fetch_emp()
    tree.delete(*tree.get_children())
    for employee in emp:
        tree.insert('', END, values=employee)

def add_emp():
    if id_entry.get()=='' or phone_entry.get()=='' or name_entry.get()=='' or salary_entry.get()=='':
        messagebox.showerror('Error', 'All feilds are required')
    else:
        database.insert(id_entry.get(), name_entry.get(), phone_entry.get(), role_box.get(), gender_box.get(), salary_entry.get())
        # messagebox.showinfo('Sucess', 'Details Inserted Successfully')
        tree_view()
        clear()

#-------------GUI SETUP---------------
data_entry_window = CTk()
data_entry_window.geometry('1000x590+100+100') #+100 is fixing th position of window
data_entry_window.resizable(0, 0) #can also gove (False, False)
data_entry_window.title("Employee MAnagement System")
data_entry_window.configure(fg_color='#1e3d4f')

img=CTkImage(Image.open('ems_admin_header.jpg'), size=(1000, 180)) #to import the image
imageLabel = CTkLabel(data_entry_window, image=img, text='', bg_color='#eafaf7') #to add the image
imageLabel.grid(row=0, column=0, columnspan=2, sticky='w')

#-----------LEFT ENTRY FRAME-----------------
leftFrame = CTkFrame(data_entry_window, fg_color='#1e3d4f')
leftFrame.grid(row=1, column=0, sticky='w')

#-----------ID LABELS-------------------------
id_label = CTkLabel(leftFrame, text='Id', font=('arial', 15, 'bold'), text_color='black')
id_label.grid(row=0, column=0, padx=15, pady=10)
id_entry = CTkEntry(leftFrame, font=('arial', 15, 'bold'), width=180)
id_entry.grid(row=0, column=1, padx=10)

#---------NAME LABELS------------------------
name_label = CTkLabel(leftFrame, text='Name', font=('arial', 15, 'bold'), text_color='black')
name_label.grid(row=1, column=0, padx=15, pady=10)
name_entry = CTkEntry(leftFrame, font=('arial', 15, 'bold'), width=180)
name_entry.grid(row=1, column = 1)

#-----------PHONE LABELS------------------------
phone_label = CTkLabel(leftFrame, text='Phone no.', font=('arial', 15, 'bold'), text_color='black')
phone_label.grid(row=2, column=0, padx=15, pady=10)
phone_entry = CTkEntry(leftFrame, font=('arial', 15, 'bold'), width=180)
phone_entry.grid(row=2, column=1)

#----------------ROLE LABELS--------------------
role_label = CTkLabel(leftFrame, text='Role', font=('arial', 15, 'bold'), text_color='black')
role_label.grid(row=3, column=0, padx=15, pady=10)
roles = ['Web Developer', 'Graphic Designer', 'Technical Writer', 
         'DevOps', 'UI/UX Developer', 'Data Scientist', 'Network Engineer']
role_box = CTkComboBox(leftFrame, values=roles, width=180, font=('arial', 15, 'bold'), state='readonly')
role_box.grid(row=3, column=1)
role_box.set('Web Developer')

#-------------------GENDER LABELS------------------
gender_label = CTkLabel(leftFrame, text='Gender', font=('arial', 15, 'bold'), text_color='black')
gender_label.grid(row=4, column=0, padx=15, pady=10)
genders = ['Male', 'Female']
gender_box = CTkComboBox(leftFrame, values=genders, width=180, font=('arial', 15, 'bold'), state='readonly')
gender_box.grid(row=4, column=1)
gender_box.set("Male")

#------------------SALARY LABELS----------------------
salary_label = CTkLabel(leftFrame, text='Salary', font=('arial', 15, 'bold'), text_color='black')
salary_label.grid(row=5, column=0, padx=15, pady=10)
salary_entry = CTkEntry(leftFrame, font=('arial', 15, 'bold'), width=180)
salary_entry.grid(row=5, column=1)

#-------------------DATA VISUALISATION FRAME------------------------
rightFrame = CTkFrame(data_entry_window)
rightFrame.grid(row=1, column=1)
# rightFrame.configure(bg_color='#eafaf7')

#------------------SEARCH BOX-------------------------
search_options = ['Id', 'Name', 'Phone', 'Role', 'Gender', 'Salary']
search_box = CTkComboBox(rightFrame, values=search_options, font=('arial', 15, 'bold'), state='readonly')
search_box.grid(row=0, column=0)
search_box.set("Search by")

#------------SEARCH ENTRY----------------------- 
search_entry = CTkEntry(rightFrame, font=('arial', 15, 'bold'), width=180)
search_entry.grid(row=0, column=1)

#---------------SEARCH BUTTON---------------------
search_button = CTkButton(rightFrame, text='Search', command=search_emp)
search_button.grid(row=0, column=2)

#----------------SHOW ALL BUTTON-------------------
showall_button = CTkButton(rightFrame, text='Show All', command=tree_view)
showall_button.grid(row=0, column=3, pady=5)

#-------------------TREE VIEW---------------------
tree = ttk.Treeview(rightFrame, height=13)
tree.grid(row=1, column=0, columnspan=4)

tree['columns'] = ('Id', 'Name', 'Phone', 'Role', 'Gender', 'Salary')

#----------------COLUMN HEADS---------------------
tree.heading('Id', text='Id')
tree.heading('Name', text='Name')
tree.heading('Phone', text='Phone')
tree.heading('Role', text='Role')
tree.heading('Gender', text='Gender')
tree.heading('Salary', text='Salary')

tree.config(show='headings')

#-----------------CONFIGURATION COLUMN---------------
tree.column('Id', width=100)
tree.column('Name', width=160)
tree.column('Phone', width=160)
tree.column('Role', width=200)
tree.column('Gender', width=100)
tree.column('Salary', width=140)

style = ttk.Style()

style.configure('Treeview.Heading', font=('arial', 15, 'bold'))
style.configure('Treeview', font=('arial', 12), rowheight=30)

scrollbar = ttk.Scrollbar(rightFrame, orient=VERTICAL,)
scrollbar.grid(row=1, column=4, sticky='ns')

#---------TAIL FRAME FOR BUTTONS-----------------------
buttonFrame = CTkFrame(data_entry_window, fg_color='#1e3d4f')
buttonFrame.grid(row=2, column=0, columnspan=2)

newButton = CTkButton(buttonFrame, text="New Employee", font=('arial', 15, 'bold'), width=160, corner_radius=15, command=lambda:clear(True))
newButton.grid(row=0, column=0, pady=5)

addButton = CTkButton(buttonFrame, text="Add Employee", font=('arial', 15, 'bold'), width=160, corner_radius=15, command=add_emp)
addButton.grid(row=0, column=1, pady=5, padx=5)

updateButton = CTkButton(buttonFrame, text="Update Employee", font=('arial', 15, 'bold'), width=160, corner_radius=15, command=update_emp)
updateButton.grid(row=0, column=2, pady=5, padx=5)

deleteButton = CTkButton(buttonFrame, text="Delete Employee", font=('arial', 15, 'bold'), width=160, corner_radius=15, command=delete_emp)
deleteButton.grid(row=0, column=3, pady=5, padx=5)

deleteallButton = CTkButton(buttonFrame, text="Delete All", font=('arial', 15, 'bold'), width=160, corner_radius=15, command=delete_all)
deleteallButton.grid(row=0, column=4, pady=5, padx=5)

#---------------FOR TABLE VIEW---------------
tree_view()
data_entry_window.bind('<ButtonRelease>', selection)

#-----------RUN APP------------------------
data_entry_window.mainloop()