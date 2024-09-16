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

# Suppress specific warnings
warnings.filterwarnings("ignore", message="CTkLabel Warning: Given image is not CTkImage but <class 'PIL.ImageTk.PhotoImage'>. Image can not be scaled on HighDPI displays, use CTkImage instead.\n")


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

# Register window
class RegisterWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.center_window()

        # Instance variable to store the OTP
        self.generated_otp = None

        self.geometry("1366x768")
        self.title("Register")
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

        frame = customtkinter.CTkFrame(master=l1, width=600, height=500, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


        l2 = customtkinter.CTkLabel(master=frame, text="Create an Account", font=("Arial", 28))
        l2.place(x=180, y=45)

        self.name_entry = customtkinter.CTkEntry(master=frame, width=230, placeholder_text="Name")
        self.name_entry.place(x=50, y=110)

        self.email_entry = customtkinter.CTkEntry(master=frame, width=230, placeholder_text="Email")
        self.email_entry.place(x=310, y=110)

        self.mobile_entry = customtkinter.CTkEntry(master=frame, width=230, placeholder_text="Mobile Number")
        self.mobile_entry.place(x=50, y=150)

        self.gender_entry = customtkinter.CTkOptionMenu(master=frame, width=230, values=["Male","Female","Other"])
        self.gender_entry.place(x=310, y=150)

        self.position_entry = customtkinter.CTkEntry(master=frame, width=230, placeholder_text="Enter Job Position")
        self.position_entry.place(x=50, y=190)

        self.department_entry = customtkinter.CTkEntry(master=frame, width=230, placeholder_text="Enter Department")
        self.department_entry.place(x=310, y=190)

        self.sapnumber_entry = customtkinter.CTkEntry(master=frame, width=230, placeholder_text="Enter SAP Number")
        self.sapnumber_entry.place(x=50, y=230)

        self.nationality_entry = customtkinter.CTkEntry(master=frame, width=230, placeholder_text="Enter Nationality")
        self.nationality_entry.place(x=310, y=230)

        self.username_entry = customtkinter.CTkEntry(master=frame, width=230, placeholder_text="Username")
        self.username_entry.place(x=50, y=270)

        self.password_entry = customtkinter.CTkEntry(master=frame, width=230, placeholder_text="Password", show="*")
        self.password_entry.place(x=310, y=270)

        self.otp_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="OTP")
        self.otp_entry.place(x=50, y=310)

        l3 = customtkinter.CTkLabel(master=frame, text="*After entering your email, click 'Get OTP Code' to receive an OTP via email.", font=("Arial", 12))
        l3.place(x=50, y=345)

        otp_button = customtkinter.CTkButton(master=frame, text="Get OTP Code", width=100, cursor="hand2", command=self.send_otp)
        otp_button.place(x=180, y=310)

        register_button = customtkinter.CTkButton(master=frame, text="Register", width=490, cursor="hand2", command=self.register_user)
        register_button.place(x=50, y=380)

        login_button = customtkinter.CTkButton(master=frame, text="Login", width=490, cursor="hand2",command=self.on_login_click)
        login_button.place(x=50, y=430)

        # Bind the window close event to the on_close method
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    
    # Function to register a user
    def register_user(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        mobile = self.mobile_entry.get()
        gender = self.gender_entry.get()
        position = self.position_entry.get()
        department = self.department_entry.get()
        sapnumber = self.sapnumber_entry.get()
        nationality = self.nationality_entry.get()
        otp = self.otp_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if not (name and email and mobile and gender and position and department and sapnumber and nationality and otp and username and password):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        # Check if the entered OTP is correct
        if str(self.generated_otp) != otp :
            messagebox.showerror("Error", "Invalid OTP. Please try again.")
            return     

        user_data = read_data(f'users/{username}')
        if user_data:
            messagebox.showerror("Error", "Username already exists")
        else:
            # Prepare the data dictionary with all the collected inputs
            data = {
                'username': username,
                'name': name,
                'email': email,
                'mobile': mobile,
                'gender': gender,
                'position': position,
                'department': department,
                'sapnumber': sapnumber,
                'nationality': nationality,
                'password': hashed_password
            }

            # Save the data
            write_data(data, f'users/{username}')
            
            messagebox.showinfo("Success", "Registration successful")
            self.destroy()
            self.master.deiconify()

    # OTP verification
    def send_otp(self):
        receiverEmail = self.email_entry.get()
        if not receiverEmail:
            messagebox.showerror("Error", "Please enter an email address")
            return
        
        # Generate OTP

        # Email details
        email = 'propertymanagementauxmen@gmail.com'

        # Generate OTP
        otp = random.randint(100000, 999999)  # Generates a 6-digit OTP
        self.generated_otp = otp  # Store OTP in the instance variable

        # Create email content
        subject = 'Your OTP Code'
        message = f"""
        <html>
        <body>
            <p>Hello,</p>
            <p>Your One-Time Password (OTP) is: <strong>{otp}</strong></p>
            <p>Please use this code to complete your verification. This code is valid for 10 minutes.</p>
            <p>Thank you,<br>Hostel Managment Admin</p>
        </body>
        </html>
        """

        # Setup the MIME
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = receiverEmail
        msg['Subject'] = subject

        # Attach the HTML message with the msg instance
        msg.attach(MIMEText(message, 'html'))

        # Sending the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, 'arkszkvyxrfkpztq')
        server.sendmail(email, receiverEmail, msg.as_string())
        server.quit()

        print(f"OTP {otp} has been sent to {receiverEmail}")
        messagebox.showinfo("Success", "OTP Send successful")
        return otp

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (1366 / 2)
        y = (screen_height / 2) - (768 / 2)
        self.geometry(f"1366x768+{int(x)}+{int(y)}")

    def on_login_click(self):
        self.destroy()
        self.master.deiconify()

    def on_close(self):
        # Close the entire application
        self.master.destroy()
        sys.exit()
