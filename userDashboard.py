import firebase_admin
from firebase_admin import credentials, db
import customtkinter
import customtkinter as ctk
import tkinter as tk
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
class DashboardWindow(tk.Toplevel):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.parent = parent
        self.username = username

        self.center_window()

        self.geometry("1366x768")
        self.title("Dashboard")
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
        self.application_frame = customtkinter.CTkFrame(master=self.main_frame, width=1166, height=668, corner_radius=0, fg_color="#2b2b2b", bg_color="#2b2b2b")
        self.application_frame.place(x=0, y=0)

        self.application_frame1 = customtkinter.CTkFrame(master=self.main_frame, width=1166, height=668, corner_radius=0, fg_color="#2b2b2b", bg_color="#2b2b2b")
        self.application_frame1.place(x=0, y=0)

        # Open Ticket Frame
        self.open_ticket_frame = customtkinter.CTkFrame(master=self.main_frame, width=1166, height=668, corner_radius=0, fg_color="#2b2b2b", bg_color="#2b2b2b")
        self.open_ticket_frame.place(x=0, y=0)

        # hide all frames initially
        self.application_frame1.place_forget()
        self.open_ticket_frame.place_forget()

        # Load the image using PIL
        background_image = Image.open(resource_path("Assets/background.jpg"))
        bg_image_resized = background_image.resize((1166, 668))
        bg_image = ImageTk.PhotoImage(bg_image_resized)

        # Create a label to hold the background image, with text set to an empty string
        self.background_label = customtkinter.CTkLabel(master=self.application_frame, image=bg_image, text="")
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        application_button = customtkinter.CTkButton(master=left_frame, text="Application Form", width=200, height=100,corner_radius=0, cursor="hand2", font=("Arial", 20), command=self.show_application_form)
        application_button.place(x=0, y=0)

        open_ticket_button = customtkinter.CTkButton(master=left_frame, text="Open Ticket", width=200, height=100,corner_radius=0, cursor="hand2", font=("Arial", 20), command=self.show_open_ticket_form)
        open_ticket_button.place(x=0, y=100)

        # Bind the window close event to the on_close method
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (1366 / 2)
        y = (screen_height / 2) - (768 / 2)
        self.geometry(f"1366x768+{int(x)}+{int(y)}")

    def show_application_form(self):
        # Ensure the background image is removed
        if self.background_label:
            self.background_label.place_forget()

        # Hide other frames
        self.hide_all_frames()

        # Add the new label for "Application Form"
        l2 = customtkinter.CTkLabel(master=self.application_frame1, text="Application Form", font=("Arial", 36))
        l2.place(x=450, y=20)
        
        # Create the form fields
        self.name_entry = customtkinter.CTkEntry(master=self.application_frame1, width=400, placeholder_text="Name")
        self.name_entry.place(x=150, y=100)

        self.email_entry = customtkinter.CTkEntry(master=self.application_frame1, width=400, placeholder_text="Email")
        self.email_entry.place(x=150, y=150)

        self.mobile_entry = customtkinter.CTkEntry(master=self.application_frame1, width=400, placeholder_text="Mobile Number")
        self.mobile_entry.place(x=150, y=200)

        self.gender_entry = customtkinter.CTkOptionMenu(master=self.application_frame1, width=400, values=["Male","Female","Other"])
        self.gender_entry.place(x=150, y=250) 

        self.nationality_entry = customtkinter.CTkEntry(master=self.application_frame1, width=400, placeholder_text="Nationality")
        self.nationality_entry.place(x=150, y=300)

        self.position_entry = customtkinter.CTkEntry(master=self.application_frame1, width=400, placeholder_text="Enter Job Position")
        self.position_entry.place(x=150, y=350)

        self.department_entry = customtkinter.CTkEntry(master=self.application_frame1, width=400, placeholder_text="Enter Department")
        self.department_entry.place(x=150, y=400)

        self.sapnumber_entry = customtkinter.CTkEntry(master=self.application_frame1, width=400, placeholder_text="Enter SAP Number")
        self.sapnumber_entry.place(x=150, y=450)

        self.shift_entry = customtkinter.CTkOptionMenu(master=self.application_frame1, width=400, values=["Shift Worker","Non-shift Worker"])
        self.shift_entry.place(x=150, y=500)

        self.apartmentnumber_entry = customtkinter.CTkEntry(master=self.application_frame1, width=400, placeholder_text="Enter Apartment Number")
        self.apartmentnumber_entry.place(x=600, y=100)

        self.roomnumber_entry = customtkinter.CTkEntry(master=self.application_frame1, width=400, placeholder_text="Enter Room Number")
        self.roomnumber_entry.place(x=600, y=150)

        self.capacity_entry = customtkinter.CTkEntry(master=self.application_frame1, width=400, placeholder_text="Enter Capacity")
        self.capacity_entry.place(x=600, y=200)

        self.whichline_entry = customtkinter.CTkOptionMenu(master=self.application_frame1, width=400, values=["1st Line","2nd Line","3rd Line","4th Line","5th Line","6th Line","7th Line","8th Line","9th Line","10th Line"])
        self.whichline_entry.place(x=600, y=250)

        self.whichfloor_entry = customtkinter.CTkOptionMenu(master=self.application_frame1, width=400, values=["1st Floor","2nd Floor","3rd Floor","4th Floor","5th Floor","6th Floor","7th Floor","8th Floor","9th Floor","10th Floor"])
        self.whichfloor_entry.place(x=600, y=300)

        # Arrival Date Entry with placeholder
        self.arrivaldate_entry = ctk.CTkEntry(master=self.application_frame1, width=400, placeholder_text="Enter Arrival Date")
        self.arrivaldate_entry.place(x=600, y=350)
        self.arrivaldate_entry.bind("<Button-1>", lambda event: self.show_calendar(self.arrivaldate_entry))

        # Despature Date Entry with placeholder
        self.despaturedate_entry = ctk.CTkEntry(master=self.application_frame1, width=400, placeholder_text="Enter Despature Date")
        self.despaturedate_entry.place(x=600, y=400)
        self.despaturedate_entry.bind("<Button-1>", lambda event: self.show_calendar(self.despaturedate_entry))

        self.accomadationlocation_entry = customtkinter.CTkOptionMenu(master=self.application_frame1, width=400, values=["Colombo","Galle","Kandy","Anuradhapura","Jaffna","Trincomalee","Batticaloa","Matara","Kurunegala","Negombo"])  
        self.accomadationlocation_entry.place(x=600, y=450)

        submit_button = customtkinter.CTkButton(master=self.application_frame1, text="Submit", width=500, cursor="hand2", command=self.save_application_data)
        submit_button.place(x=320, y=600)

        self.current_status = 'Pending'

        self.application_frame1.place(x=0, y=0)

        self.load_user_data()
    
    def show_calendar(self, entry_widget):
        # Create a Toplevel window for the calendar
        self.calendar_window = Toplevel(self.application_frame1)
        self.calendar_window.grab_set()  # Focus on the calendar window

        # Set window title and icon (replace 'icon.ico' with the actual path of your icon file)
        self.calendar_window.title("Select a Date")
        self.calendar_window.iconbitmap(resource_path("Assets/icon.ico")) 

        # Position the calendar window next to the entry widget
        entry_x = entry_widget.winfo_rootx()
        entry_y = entry_widget.winfo_rooty() + entry_widget.winfo_height()
        self.calendar_window.geometry(f"250x250+{entry_x+200}+{entry_y-100}")

        # Add Calendar widget to the Toplevel window
        self.calendar = Calendar(master=self.calendar_window, date_pattern="dd/mm/yyyy")
        self.calendar.pack(padx=10, pady=10)

        # Add a button to confirm date selection
        select_button = ctk.CTkButton(master=self.calendar_window, text="Select", command=lambda: self.select_date(entry_widget))
        select_button.pack(pady=5)

    def select_date(self, entry_widget):
        # Get selected date from the calendar
        selected_date = self.calendar.get_date()

        # Insert selected date into the appropriate Entry widget
        entry_widget.delete(0, "end")  # Clear the entry field
        entry_widget.insert(0, selected_date)

        # Close the calendar window
        self.calendar_window.destroy()

    def load_user_data(self):
        # Fetch user data from the database
        user_data = read_data(f'users/{self.username}')
        if user_data:
            self.name_entry.insert(0, user_data.get('name', ''))
            self.email_entry.insert(0, user_data.get('email', ''))
            self.mobile_entry.insert(0, user_data.get('mobile', ''))
            self.gender_entry.set(user_data.get('gender', ''))
            self.position_entry.insert(0, user_data.get('position', ''))
            self.department_entry.insert(0, user_data.get('department', ''))
            self.sapnumber_entry.insert(0, user_data.get('sapnumber', ''))
            self.nationality_entry.insert(0, user_data.get('nationality', ''))

    def save_application_data(self):
        # Get data from form entries
        name = self.name_entry.get()
        email = self.email_entry.get()
        mobile = self.mobile_entry.get()
        gender = self.gender_entry.get()
        nationality = self.nationality_entry.get()
        position = self.position_entry.get()
        department = self.department_entry.get()
        sap_number = self.sapnumber_entry.get()
        shift = self.shift_entry.get()
        apartment_number = self.apartmentnumber_entry.get()
        room_number = self.roomnumber_entry.get()
        capacity = self.capacity_entry.get()
        which_line = self.whichline_entry.get()
        which_floor = self.whichfloor_entry.get()
        arrival_date = self.arrivaldate_entry.get()
        departure_date = self.despaturedate_entry.get()
        location = self.accomadationlocation_entry.get()

        # Format the path using the username
        path = f'applications/{self.username}'

        try:
            # Reference to the 'Applications' node for this user
            ref = db.reference(path)
            
            # Retrieve all the data from the 'Applications' node
            applications_data = ref.get()

            # Count the number of records (children)
            if applications_data:
                count = len(applications_data) 
            else:
                count = 1
            
            print(f"Total number of records: {count}")

            current_status = read_data(f'applications/{self.username}/{count-1}/status')
            if current_status == 'Pending':
                messagebox.showerror("Error", "You have already submitted an application. Please wait for the approval.")
                return

            # Prepare the data dictionary with all the collected inputs
            application_data = {
                "name": name,
                "email": email,
                "mobile": mobile,
                "gender": gender,
                "nationality": nationality,
                "position": position,
                "department": department,
                "sap_number": sap_number,
                "shift": shift,
                "apartment_number": apartment_number,
                "room_number": room_number,
                "capacity": capacity,
                "which_line": which_line,
                "which_floor": which_floor,
                "arrival_date": arrival_date,
                "departure_date": departure_date,
                "location": location,
                "status": "Pending"
            }

            # Save the application data with count as the ID
            ref.child(str(count)).set(application_data)
            messagebox.showinfo("Success", "Application submitted successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Open Ticket Function
    def show_open_ticket_form(self):
        # Ensure the background image is removed
        if self.background_label:
            self.background_label.place_forget()
        
        # Hide other frames
        self.hide_all_frames()

        # Show open ticket frame
        self.open_ticket_frame.place(x=0, y=0)
            
        # Add the new label for "Open Ticket"
        l2 = customtkinter.CTkLabel(master=self.open_ticket_frame, text="Open Ticket", font=("Arial", 36))
        l2.place(x=450, y=20)

        # Create the form fields
        self.ticket_reason_entry = customtkinter.CTkEntry(master=self.open_ticket_frame, width=500, placeholder_text="Reason")
        self.ticket_reason_entry.place(x=150, y=100)

        # Create a CTkTextbox for ticket description
        self.ticket_description_entry = customtkinter.CTkTextbox(master=self.open_ticket_frame,
            width=1000,
            height=200,
            corner_radius=10,
            border_width=2,
            border_color="#003660",
            border_spacing=10,
            fg_color="silver",
            text_color="grey",
            font=("Arial", 18),
            wrap="word",
            activate_scrollbars=True)
        self.ticket_description_entry.place(x=150, y=150)

        # Insert placeholder text
        self.ticket_description_entry.insert("1.0", "Explain it...")

        # Bind focus events to add placeholder functionality
        self.ticket_description_entry.bind("<FocusIn>", self.on_focus_in)
        self.ticket_description_entry.bind("<FocusOut>", self.on_focus_out)

        # Submit button
        submit_button = customtkinter.CTkButton(master=self.open_ticket_frame, text="Submit", width=1000, cursor="hand2", command=self.save_ticket_data)
        submit_button.place(x=150, y=400)

    # Function to clear placeholder on focus in
    def on_focus_in(self, event):
        if self.ticket_description_entry.get("1.0", "end-1c") == "Explain it...":
            self.ticket_description_entry.delete("1.0", "end")
            self.ticket_description_entry.configure(text_color="black")

    # Function to restore placeholder on focus out
    def on_focus_out(self, event):
        if self.ticket_description_entry.get("1.0", "end-1c") == "":
            self.ticket_description_entry.insert("1.0", "Explain it...")
            self.ticket_description_entry.configure(text_color="grey")

    # Function to save ticket data and send emails
    def save_ticket_data(self):
        # Get data from form entries
        reason = self.ticket_reason_entry.get()
        description = self.ticket_description_entry.get("1.0", "end-1c")

        # Validate the form
        if (description == "Enter ticket description..." or description == "") or reason == "":
            messagebox.showerror("Input Error", "Please fill in all required fields.")
            return  # Exit the function if validation fails

        # Fetch the user's email from the database (e.g., Firebase or other storage)
        user_email = read_data(f'users/{self.username}/email')  # Replace with actual method to get user's email
        admin_email = 'propertymanagementauxmen@gmail.com'  # Admin's email

        # Create admin email content
        admin_subject = f"New Ticket: {reason}"
        admin_message = f"""
        <html>
        <body>
            <p>Hello Admin,</p>
            <p>A new ticket has been submitted by {self.username} with the following details:</p>
            <p><strong>Reason:</strong> {reason}</p>
            <p><strong>Description:</strong></p>
            <p>{description}</p>
            <p>You can reply to this email to communicate directly with the user: {user_email}</p>
            <p>Thank you,<br>{self.username}</p>
        </body>
        </html>
        """

        # Create user confirmation email content
        user_subject = "Ticket Submission Confirmation"
        user_message = f"""
        <html>
        <body>
            <p>Dear {self.username},</p>
            <p>Thank you for submitting a ticket with the following details:</p>
            <p><strong>Reason:</strong> {reason}</p>
            <p><strong>Description:</strong></p>
            <p>{description}</p>
            <p>Our support team will review your ticket and get back to you soon. If you need further assistance, feel free to reply to this email.</p>
            <p>Best regards,<br>Support Team</p>
        </body>
        </html>
        """

        try:
            # Setup the MIME for admin email
            admin_msg = MIMEMultipart()
            admin_msg['From'] = admin_email  
            admin_msg['To'] = admin_email
            admin_msg['Subject'] = admin_subject
            admin_msg.add_header('Reply-To', user_email)
            admin_msg.attach(MIMEText(admin_message, 'html'))

            # Setup the MIME for user confirmation email
            user_msg = MIMEMultipart()
            user_msg['From'] = admin_email 
            user_msg['To'] = user_email
            user_msg['Subject'] = user_subject
            user_msg.attach(MIMEText(user_message, 'html'))

            # Sending the emails
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(admin_email, 'arkszkvyxrfkpztq')  

            # Send the email to the admin
            server.sendmail(admin_email, admin_email, admin_msg.as_string())

            # Send the confirmation email to the user
            server.sendmail(admin_email, user_email, user_msg.as_string())

            server.quit()

            messagebox.showinfo("Success", "Ticket submitted successfully! A confirmation email has been sent to your email address.")
        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Failed to send the ticket and confirmation. Please try again.")

    def hide_all_frames(self):
        # Hide all frames
        self.application_frame.place_forget()
        self.application_frame1.place_forget()
        self.open_ticket_frame.place_forget()

    # Function to handle the logout button click event
    def on_logout_click(self):
        self.destroy()
        self.parent.deiconify()

    def on_close(self):
        # Close the entire application
        self.master.destroy()
        sys.exit()