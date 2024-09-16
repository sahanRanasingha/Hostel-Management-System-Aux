import firebase_admin
from firebase_admin import credentials, db
import customtkinter
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel
from tkinter import messagebox
import hashlib
from PIL import Image, ImageTk
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkcalendar import Calendar
import random
import os
import sys
import warnings

# Function to get the absolute path of a resource
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Function to initialize Firebase
def initialize_firebase():
    try:
        cred = credentials.Certificate(resource_path('serviceAccountKey.json'))
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://hostel-management-4534b-default-rtdb.firebaseio.com/'
        })
        print("Firebase app initialized successfully!")
    except Exception as e:
        print(f"Error initializing Firebase app: {e}")
        exit(1)

def write_data(data, path):
    try:
        ref = db.reference(path)
        ref.set(data)
        print(f"Data written to {path} successfully!")
    except Exception as e:
        print(f"Error writing data: {e}")

def read_data(path):
    try:
        ref = db.reference(path)
        data = ref.get()
        return data
    except Exception as e:
        print(f"Error reading data: {e}")
        return None

def update_data(data, path):
    try:
        ref = db.reference(path)
        ref.update(data)
        print(f"Data updated at {path} successfully!")
        messagebox.showinfo("Success", "Status updated successfully!")
    except Exception as e:
        print(f"Error updating data: {e}")

def delete_data(path):
    try:
        ref = db.reference(path)
        ref.delete()
        print(f"Data deleted from {path} successfully!")
    except Exception as e:
        print(f"Error deleting data: {e}")
    

# Dashboard window
class AdminDashboardWindow(tk.Toplevel):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.parent = parent
        self.username = username

        self.center_window()

        self.geometry("1366x768")
        self.title("Admin Dashboard")
        self.iconbitmap(resource_path("Assets/icon.ico"))
        self.configure(bg="#ffffff")

        # Disable window resizing
        self.resizable(False, False)

        # Load the image
        img1 = Image.open(resource_path("Assets/background.jpg"))

        # Resize the image to the desired width and height
        img1 = img1.resize((1366, 768), Image.LANCZOS)

        # Create a PhotoImage object
        self.bg_image = ImageTk.PhotoImage(img1)

        # Create a label with the image and place it with specific dimensions
        l1 = customtkinter.CTkLabel(master=self, image=self.bg_image, width=1366, height=768)
        l1.pack()

        header_frame = customtkinter.CTkFrame(master=l1, width=1366, height=200, corner_radius=0)
        header_frame.place(relx=0.5, rely=0, anchor=tk.CENTER)

        welcome_label = customtkinter.CTkLabel(master=header_frame, text=f"Welcome, {username}!", font=("Arial", 36))
        welcome_label.place(x=50, y=130)

        left_frame = customtkinter.CTkFrame(master=l1, width=200, height=768, corner_radius=0)
        left_frame.place(x=0, y=100)

        logout_button = customtkinter.CTkButton(master=left_frame, text="Logout", width=200, height=100, corner_radius=0, cursor="hand2", font=("Arial", 20), command=self.on_logout_click)
        logout_button.place(x=0, y=570)

        self.main_frame = customtkinter.CTkFrame(master=l1, width=1166, height=668, corner_radius=0)
        self.main_frame.place(x=200, y=100)

        # Assign application_frame as a class attribute using self
        self.application_frame1 = customtkinter.CTkFrame(master=self.main_frame, width=1166, height=668, corner_radius=0, fg_color="#2b2b2b", bg_color="#2b2b2b")
        self.application_frame1.place(x=0, y=0)
        self.application_frame2 = customtkinter.CTkFrame(master=self.main_frame, width=1166, height=668, corner_radius=0, fg_color="#2b2b2b", bg_color="#2b2b2b")
        self.application_frame2.place(x=0, y=0)
        self.application_frame3 = customtkinter.CTkFrame(master=self.main_frame, width=1166, height=668, corner_radius=0, fg_color="#2b2b2b", bg_color="#2b2b2b")
        self.application_frame3.place(x=0, y=0)
        self.application_frame4 = customtkinter.CTkFrame(master=self.main_frame, width=1166, height=668, corner_radius=0, fg_color="#2b2b2b", bg_color="#2b2b2b")
        self.application_frame4.place(x=0, y=0)

        self.application_table_frame = customtkinter.CTkFrame(master=self.main_frame, width=1166, height=600, corner_radius=0, fg_color="#2b2b2b", bg_color="#2b2b2b")
        self.application_table_frame.place(x=0, y=68)

        # Load the image using PIL
        background_image = Image.open(resource_path("Assets/background.jpg"))
        bg_image_resized = background_image.resize((1166, 668))
        bg_image = ImageTk.PhotoImage(bg_image_resized)

        # Create a label to hold the background image, with text set to an empty string
        self.background_label = customtkinter.CTkLabel(master=self.application_frame1, image=bg_image, text="")
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        adminDashboard_button = customtkinter.CTkButton(master=left_frame, text="Dashboard", width=200, height=100,corner_radius=0, cursor="hand2", font=("Arial", 20), command=self.admin_dashboard)
        adminDashboard_button.place(x=0, y=0)

        newForms_button = customtkinter.CTkButton(master=left_frame, text="View New Forms", width=200, height=100,corner_radius=0, cursor="hand2", font=("Arial", 20), command=self.view_new_forms)
        newForms_button.place(x=0, y=100)

        viewAll_button = customtkinter.CTkButton(master=left_frame, text="View All Forms", width=200, height=100,corner_radius=0, cursor="hand2", font=("Arial", 20), command=self.view_all_forms)
        viewAll_button.place(x=0, y=200)

        #hostelUpdate_button = customtkinter.CTkButton(master=left_frame, text="Add Hostel", width=200, height=100,corner_radius=0, cursor="hand2", font=("Arial", 20), command=self.update_hostel)
        #hostelUpdate_button.place(x=0, y=300)

        self.admin_dashboard()

        # Bind the window close event to the on_close method
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    
    # Method to display the admin dashboard
    def admin_dashboard(self):
        # Hide other frames
        self.application_frame2.place_forget()
        self.application_frame3.place_forget()
        self.application_table_frame.place_forget()
        self.application_frame4.place_forget()
    
        # Show admin dashboard
        self.application_frame1.place(x=0, y=0, relwidth=1, relheight=1)

        self.full_application_frame = customtkinter.CTkFrame(master=self.application_frame1, width=300, height=150, corner_radius=0, fg_color="#303030", bg_color="#303030")
        self.full_application_frame.place(x=100, y=10)

        self.full_application_label = customtkinter.CTkLabel(master=self.full_application_frame, text="Full Applications Count", font=("Arial", 20))
        self.full_application_label.place(x=150, y=50, anchor=tk.CENTER)

        self.full_application_count_label = customtkinter.CTkLabel(master=self.full_application_frame, text="0", font=("Arial", 20))
        self.full_application_count_label.place(x=150, y=100, anchor=tk.CENTER)

        self.approved_application_frame = customtkinter.CTkFrame(master=self.application_frame1, width=300, height=150, corner_radius=0, fg_color="#303030", bg_color="#303030")
        self.approved_application_frame.place(x=450, y=10)

        self.approved_application_label = customtkinter.CTkLabel(master=self.approved_application_frame, text="Approved Applications Count", font=("Arial", 20))
        self.approved_application_label.place(x=150, y=50, anchor=tk.CENTER)

        self.approved_application_count_label = customtkinter.CTkLabel(master=self.approved_application_frame, text="0", font=("Arial", 20))
        self.approved_application_count_label.place(x=150, y=100, anchor=tk.CENTER)

        self.pending_application_frame = customtkinter.CTkFrame(master=self.application_frame1, width=300, height=150, corner_radius=0, fg_color="#303030", bg_color="#303030")
        self.pending_application_frame.place(x=800, y=10)

        self.pending_application_label = customtkinter.CTkLabel(master=self.pending_application_frame, text="Pending Applications Count", font=("Arial", 20))
        self.pending_application_label.place(x=150, y=50, anchor=tk.CENTER)

        self.pending_application_count_label = customtkinter.CTkLabel(master=self.pending_application_frame, text="0", font=("Arial", 20))
        self.pending_application_count_label.place(x=150, y=100, anchor=tk.CENTER)

        self.live_update_application_counts()

    def live_update_application_counts(self):
        # Reference the applications node in Firebase
        ref = db.reference('applications')

        # Add a listener for live updates
        def listener(event):
            try:
                applications_data = ref.get()

                # Initialize counters
                full_applications_count = 0
                approved_applications_count = 0
                pending_applications_count = 0

                # Check if there are any applications in the data
                if applications_data:
                    # Iterate through each user in 'applications'
                    for user, user_applications in applications_data.items():
                        # If user_applications is a list, iterate over the list
                        if isinstance(user_applications, list):
                            for app_data in user_applications:
                                if isinstance(app_data, dict):  # Ensure it's a valid dictionary
                                    # Count every application
                                    full_applications_count += 1

                                    # Check the status of each application
                                    status = app_data.get('status', 'Pending').lower()

                                    if status == 'approved':
                                        approved_applications_count += 1
                                    elif status == 'pending':
                                        pending_applications_count += 1
                        # If user_applications is a dictionary (in case of another structure)
                        elif isinstance(user_applications, dict):
                            for app_key, app_data in user_applications.items():
                                if isinstance(app_data, dict):  # Ensure it's a valid dictionary
                                    # Count every application
                                    full_applications_count += 1

                                    # Check the status of each application
                                    status = app_data.get('status', 'Pending').lower()

                                    if status == 'approved':
                                        approved_applications_count += 1
                                    elif status == 'pending':
                                        pending_applications_count += 1

                # Update the labels with live counts
                self.full_application_count_label.configure(text=str(full_applications_count))
                self.approved_application_count_label.configure(text=str(approved_applications_count))
                self.pending_application_count_label.configure(text=str(pending_applications_count))

                print(f"Live updated counts - Full: {full_applications_count}, Approved: {approved_applications_count}, Pending: {pending_applications_count}")

            except Exception as e:
                print(f"Error updating application counts: {e}")

        # Attach the listener to the reference
        ref.listen(listener)

    # Method to display new forms
    def view_new_forms(self):
        # Hide other frames
        self.application_frame1.place_forget()
        self.application_frame3.place_forget()
        self.application_frame4.place_forget()

        # Show the frame where we want to display the table
        self.application_frame2.place(x=0, y=0, relwidth=1, relheight=1)
        self.application_table_frame.place(x=0, y=68, relwidth=1, relheight=0.9)

        # Clear any existing widgets in application_table_frame
        for widget in self.application_table_frame.winfo_children():
            widget.destroy()

        # Create the Treeview widget as an instance variable
        columns = (
            "Name", "Email", "Mobile", "Gender", "Nationality", "Position",
            "Department", "SAP Number", "Shift", "Apartment Number", "Room Number",
            "Capacity", "Which Line", "Which Floor", "Arrival Date", "Departure Date", "Location", "Status"
        )

        self.tree = ttk.Treeview(self.application_table_frame, columns=columns, show='headings', height=20)

        # Set up column headings and widths
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        # Create vertical scrollbar
        y_scrollbar = ttk.Scrollbar(self.application_table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=y_scrollbar.set)

        # Create horizontal scrollbar
        x_scrollbar = ttk.Scrollbar(self.application_table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=x_scrollbar.set)

        # Place the treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky='nsew')
        y_scrollbar.grid(row=0, column=1, sticky='ns')
        x_scrollbar.grid(row=1, column=0, sticky='ew')

        self.application_table_frame.grid_rowconfigure(0, weight=1)
        self.application_table_frame.grid_columnconfigure(0, weight=1)

        # Fetch all applications data from Firebase
        applications_data = read_data('applications')

        # Call your filter function
        self.filter_forms(self.application_frame2)

        # Insert data into Treeview for applications with "Pending" status
        if applications_data:
            for user, user_applications in applications_data.items():
                if isinstance(user_applications, list):
                    for app_data in user_applications:
                        if isinstance(app_data, dict) and app_data.get('status', 'Pending') == 'Pending':
                            values = (
                                app_data.get('name', 'N/A'),
                                app_data.get('email', 'N/A'),
                                app_data.get('mobile', 'N/A'),
                                app_data.get('gender', 'N/A'),
                                app_data.get('nationality', 'N/A'),
                                app_data.get('position', 'N/A'),
                                app_data.get('department', 'N/A'),
                                app_data.get('sap_number', 'N/A'),
                                app_data.get('shift', 'N/A'),
                                app_data.get('apartment_number', 'N/A'),
                                app_data.get('room_number', 'N/A'),
                                app_data.get('capacity', 'N/A'),
                                app_data.get('which_line', 'N/A'),
                                app_data.get('which_floor', 'N/A'),
                                app_data.get('arrival_date', 'N/A'),
                                app_data.get('departure_date', 'N/A'),
                                app_data.get('location', 'N/A'),
                                app_data.get('status', 'Pending')
                            )
                            self.tree.insert("", tk.END, values=values)
                elif isinstance(user_applications, dict):
                    for app_key, app_data in user_applications.items():
                        if isinstance(app_data, dict) and app_data.get('status', 'Pending') == 'Pending':
                            values = (
                                app_data.get('name', 'N/A'),
                                app_data.get('email', 'N/A'),
                                app_data.get('mobile', 'N/A'),
                                app_data.get('gender', 'N/A'),
                                app_data.get('nationality', 'N/A'),
                                app_data.get('position', 'N/A'),
                                app_data.get('department', 'N/A'),
                                app_data.get('sap_number', 'N/A'),
                                app_data.get('shift', 'N/A'),
                                app_data.get('apartment_number', 'N/A'),
                                app_data.get('room_number', 'N/A'),
                                app_data.get('capacity', 'N/A'),
                                app_data.get('which_line', 'N/A'),
                                app_data.get('which_floor', 'N/A'),
                                app_data.get('arrival_date', 'N/A'),
                                app_data.get('departure_date', 'N/A'),
                                app_data.get('location', 'N/A'),
                                app_data.get('status', 'Pending')
                            )
                            self.tree.insert("", tk.END, values=values)

        # Bind the double-click event to load the selected row data
        self.tree.bind("<Double-1>", lambda event: self.on_row_double_click())

        self.user_name_entry = customtkinter.CTkEntry(master=self.application_frame2, width=200, placeholder_text="Enter Name")
        self.user_name_entry.place(x=10, y=10)
        self.user_name_entry.configure(state='readonly')  # Set to read-only

        self.new_status_combobox = customtkinter.CTkComboBox(master=self.application_frame2, values=["Approved", "Reject", "Pending"], width=100)
        self.new_status_combobox.place(x=220, y=10)

        update_button = customtkinter.CTkButton(master=self.application_frame2, text="Update Status", width=100, cursor="hand2", command=self.approve_application_status_update)
        update_button.place(x=330, y=10)

    # Method to handle double-click on Treeview row
    def on_row_double_click(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            values = item['values']

            # Load data into the fields
            self.user_name_entry.configure(state='normal')  # Temporarily allow editing to set the value
            self.user_name_entry.delete(0, tk.END)
            self.user_name_entry.insert(0, values[0])  # Load "Name" into the user_name_entry
            self.user_name_entry.configure(state='readonly')  # Set back to read-only

            # Load the current status into new_status_combobox
            self.new_status_combobox.set(values[-1])  # Load "Status"

    # Method to update the status in TreeView and Firebase
    def approve_application_status_update(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            values = item['values']

            # Get the new status from the combobox
            new_status = self.new_status_combobox.get()

            # Update the status in the Treeview
            self.tree.set(selected_item, column="Status", value=new_status)

            # Update the status in Firebase
            applications_data = read_data('applications')

            if applications_data:
                for user, user_applications in applications_data.items():
                    if isinstance(user_applications, list):
                        for app_data in user_applications:
                            if isinstance(app_data, dict) and app_data.get('name', 'N/A') == values[0]:
                                app_data['status'] = new_status
                    elif isinstance(user_applications, dict):
                        for app_key, app_data in user_applications.items():
                            if isinstance(app_data, dict) and app_data.get('name', 'N/A') == values[0]:
                                app_data['status'] = new_status
                
                update_data(applications_data, 'applications')
                


    # Method to display all forms
    def view_all_forms(self):
        # Hide other frames
        self.application_frame1.place_forget()
        self.application_frame2.place_forget()
        self.application_frame4.place_forget()

        # Show the frame where we want to display the table
        self.application_frame3.place(x=0, y=0, relwidth=1, relheight=1)
        self.application_table_frame.place(x=0, y=68, relwidth=1, relheight=0.9)  

        # Clear any existing widgets in application_table_frame
        for widget in self.application_table_frame.winfo_children():
            widget.destroy()

        # Create the Treeview widget
        columns = (
            "Name", "Email", "Mobile", "Gender", "Nationality", "Position",
            "Department", "SAP Number", "Shift", "Apartment Number", "Room Number",
            "Capacity", "Which Line", "Which Floor", "Arrival Date", "Departure Date", "Location", "Status"
        )

        tree = ttk.Treeview(self.application_table_frame, columns=columns, show='headings', height=20)
        
        # Set up column headings and widths
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")

        # Create vertical scrollbar
        y_scrollbar = ttk.Scrollbar(self.application_table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=y_scrollbar.set)

        # Create horizontal scrollbar
        x_scrollbar = ttk.Scrollbar(self.application_table_frame, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=x_scrollbar.set)

        # Place the treeview and scrollbars
        tree.grid(row=0, column=0, sticky='nsew')
        y_scrollbar.grid(row=0, column=1, sticky='ns')
        x_scrollbar.grid(row=1, column=0, sticky='ew')

        self.application_table_frame.grid_rowconfigure(0, weight=1)
        self.application_table_frame.grid_columnconfigure(0, weight=1)

        # Fetch all applications data from Firebase
        applications_data = read_data('applications')

        self.filter_forms(self.application_frame3)

        # Insert data into Treeview
        if applications_data:
            for user, user_applications in applications_data.items():
                if isinstance(user_applications, list):
                    for app_data in user_applications:
                        if isinstance(app_data, dict):
                            values = (
                                app_data.get('name', 'N/A'),
                                app_data.get('email', 'N/A'),
                                app_data.get('mobile', 'N/A'),
                                app_data.get('gender', 'N/A'),
                                app_data.get('nationality', 'N/A'),
                                app_data.get('position', 'N/A'),
                                app_data.get('department', 'N/A'),
                                app_data.get('sap_number', 'N/A'),
                                app_data.get('shift', 'N/A'),
                                app_data.get('apartment_number', 'N/A'),
                                app_data.get('room_number', 'N/A'),
                                app_data.get('capacity', 'N/A'),
                                app_data.get('which_line', 'N/A'),
                                app_data.get('which_floor', 'N/A'),
                                app_data.get('arrival_date', 'N/A'),
                                app_data.get('departure_date', 'N/A'),
                                app_data.get('location', 'N/A'),
                                app_data.get('status', 'Pending')
                            )
                            tree.insert("", tk.END, values=values)
                elif isinstance(user_applications, dict):
                    for app_key, app_data in user_applications.items():
                        if isinstance(app_data, dict):
                            values = (
                                app_data.get('name', 'N/A'),
                                app_data.get('email', 'N/A'),
                                app_data.get('mobile', 'N/A'),
                                app_data.get('gender', 'N/A'),
                                app_data.get('nationality', 'N/A'),
                                app_data.get('position', 'N/A'),
                                app_data.get('department', 'N/A'),
                                app_data.get('sap_number', 'N/A'),
                                app_data.get('shift', 'N/A'),
                                app_data.get('apartment_number', 'N/A'),
                                app_data.get('room_number', 'N/A'),
                                app_data.get('capacity', 'N/A'),
                                app_data.get('which_line', 'N/A'),
                                app_data.get('which_floor', 'N/A'),
                                app_data.get('arrival_date', 'N/A'),
                                app_data.get('departure_date', 'N/A'),
                                app_data.get('location', 'N/A'),
                                app_data.get('status', 'Pending')
                            )
                            tree.insert("", tk.END, values=values)

    # Method to center the window
    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (1366 / 2)
        y = (screen_height / 2) - (768 / 2)
        self.geometry(f"1366x768+{int(x)}+{int(y)}")

    # Set up the filter forms
    def filter_forms(self,frame_name):
        self.search_data_entry = customtkinter.CTkEntry(master=frame_name, width=200, placeholder_text="Search")
        self.search_data_entry.place(x=550, y=10)
        
        # Placeholder for Combobox
        self.search_column_combobox = ttk.Combobox(master=frame_name, values=("Name", "Email", "Mobile", "SAP Number"), width=20)
        self.search_column_combobox.place(x=760, y=13)
        
        # Set placeholder text
        self.search_column_combobox.insert(0, "Select Column")
        self.search_column_combobox.bind("<FocusIn>", self.remove_placeholder)
        self.search_column_combobox.bind("<FocusOut>", self.add_placeholder)
        
        search_button = customtkinter.CTkButton(master=frame_name, text="Search", width=100, cursor="hand2", command=self.perform_search)
        search_button.place(x=910, y=10)

        show_all_button = customtkinter.CTkButton(master=frame_name, text="Show All", width=100, cursor="hand2", command=self.view_all_forms)
        show_all_button.place(x=1020, y=10)

    # Method to perform search
    def perform_search(self):
        search_term = self.search_data_entry.get()
        selected_column = self.search_column_combobox.get()

        if not search_term.strip():
            # Display a warning if the search term is empty
            tk.messagebox.showwarning("Warning", "Please enter a search term.")
            return

        if selected_column == "Select Column":
            # Display a warning if no column is selected
            tk.messagebox.showwarning("Warning", "Please select a column to search.")
            return

        # If validation passes, call the search method
        self.search(search_term, selected_column)

    # Method to search for data
    def search(self, search_term, column):
        # Clear existing data in the Treeview
        tree = self.application_table_frame.winfo_children()[0] if self.application_table_frame.winfo_children() else None
        if tree:
            tree.delete(*tree.get_children())

        # Fetch all applications data from Firebase
        applications_data = read_data('applications')

        # Insert data into Treeview with filtering
        if applications_data:
            for user, user_applications in applications_data.items():
                if isinstance(user_applications, list):
                    for app_data in user_applications:
                        if isinstance(app_data, dict):
                            values = (
                                app_data.get('name', 'N/A'),
                                app_data.get('email', 'N/A'),
                                app_data.get('mobile', 'N/A'),
                                app_data.get('gender', 'N/A'),
                                app_data.get('nationality', 'N/A'),
                                app_data.get('position', 'N/A'),
                                app_data.get('department', 'N/A'),
                                app_data.get('sap_number', 'N/A'),
                                app_data.get('shift', 'N/A'),
                                app_data.get('apartment_number', 'N/A'),
                                app_data.get('room_number', 'N/A'),
                                app_data.get('capacity', 'N/A'),
                                app_data.get('which_line', 'N/A'),
                                app_data.get('which_floor', 'N/A'),
                                app_data.get('arrival_date', 'N/A'),
                                app_data.get('departure_date', 'N/A'),
                                app_data.get('location', 'N/A'),
                                app_data.get('status', 'Pending')
                            )
                            
                            # Check if the data matches the search criteria
                            if column == "Name" and search_term.lower() == app_data.get('name', '').lower() or \
                                column == "Email" and search_term.lower() == app_data.get('email', '').lower() or \
                                column == "Mobile" and search_term.lower() == app_data.get('mobile', '').lower() or \
                                column == "SAP Number" and search_term.lower() == app_data.get('sap_number', '').lower():
                                tree.insert("", tk.END, values=values)
                elif isinstance(user_applications, dict):
                    for app_key, app_data in user_applications.items():
                        if isinstance(app_data, dict):
                            values = (
                                app_data.get('name', 'N/A'),
                                app_data.get('email', 'N/A'),
                                app_data.get('mobile', 'N/A'),
                                app_data.get('gender', 'N/A'),
                                app_data.get('nationality', 'N/A'),
                                app_data.get('position', 'N/A'),
                                app_data.get('department', 'N/A'),
                                app_data.get('sap_number', 'N/A'),
                                app_data.get('shift', 'N/A'),
                                app_data.get('apartment_number', 'N/A'),
                                app_data.get('room_number', 'N/A'),
                                app_data.get('capacity', 'N/A'),
                                app_data.get('which_line', 'N/A'),
                                app_data.get('which_floor', 'N/A'),
                                app_data.get('arrival_date', 'N/A'),
                                app_data.get('departure_date', 'N/A'),
                                app_data.get('location', 'N/A'),
                                app_data.get('status', 'Pending')
                            )
                            
                            # Check if the data matches the search criteria
                            if column == "Name" and search_term.lower() == app_data.get('name', '').lower() or \
                                column == "Email" and search_term.lower() == app_data.get('email', '').lower() or \
                                column == "Mobile" and search_term.lower() == app_data.get('mobile', '').lower() or \
                                column == "SAP Number" and search_term.lower() == app_data.get('sap_number', '').lower() :
                                tree.insert("", tk.END, values=values)
                            
    '''def update_hostel(self):
        # Hide other frames
        self.application_frame2.place_forget()
        self.application_frame3.place_forget()
        self.application_table_frame.place_forget()
        self.application_frame1.pack_forget()
    
        # Show admin dashboard
        self.application_frame4.place(x=0, y=0, relwidth=1, relheight=1)
    '''

    def remove_placeholder(self, event):
        if self.search_column_combobox.get() == "Select Column":
            self.search_column_combobox.delete(0, tk.END)

    def add_placeholder(self, event):
        if self.search_column_combobox.get() == "":
            self.search_column_combobox.insert(0, "Select Column")

    def on_logout_click(self):
        self.destroy()
        self.parent.deiconify()

    def on_close(self):
        # Close the entire application
        self.master.destroy()
        sys.exit()