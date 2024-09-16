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

# Forgot password window
class ForgotWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Instance variable to store the OTP
        self.generated_otp = None

        self.center_window()

        self.geometry("1366x768")
        self.title("Forgot Password")
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

        frame = customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        l2 = customtkinter.CTkLabel(master=frame, text="Forgot Password", font=("Arial", 28))
        l2.place(x=60, y=45)

        self.username_entry = customtkinter.CTkEntry(master=frame, width=220, placeholder_text="Username")
        self.username_entry.place(x=50, y=110)

        self.email_entry = customtkinter.CTkEntry(master=frame, width=220, placeholder_text="Email")
        self.email_entry.place(x=50, y=160)

        self.otp_entry = customtkinter.CTkEntry(master=frame, width=100, placeholder_text="OTP")
        self.otp_entry.place(x=50, y=190)

        otp_button = customtkinter.CTkButton(master=frame, text="Send OTP", width=110, cursor="hand2",command=self.send_otp_resetW)
        otp_button.place(x=160, y=190)

        self.password_entry = customtkinter.CTkEntry(master=frame, width=220, placeholder_text="New Password", show="*")
        self.password_entry.place(x=50, y=240)

        reset_button = customtkinter.CTkButton(master=frame, text="Reset", width=220, cursor="hand2", command=self.reset_password)
        reset_button.place(x=50, y=280)

        login_button = customtkinter.CTkButton(master=frame, text="Login", width=220, cursor="hand2", command=self.on_login_click)
        login_button.place(x=50, y=315)

        # Bind the window close event to the on_close method
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (1366 / 2)
        y = (screen_height / 2) - (768 / 2)
        self.geometry(f"1366x768+{int(x)}+{int(y)}")

    def reset_password(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        enter_otp = self.otp_entry.get()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

         # Check if any of the fields are empty
        if not username or not email or not password or not enter_otp:
            messagebox.showerror("Input Error", "All fields are required. Please fill in all fields.")
            return

        if str(self.generated_otp) != enter_otp :
            messagebox.showerror("Error", "Invalid OTP. Please try again.")
            return

        user_data = read_data(f'users/{username}')
        if user_data and user_data.get('email') == email:
            update_data({'password': hashed_password}, f'users/{username}')
            messagebox.showinfo("Success", "Password reset successful!")
        else:
            messagebox.showerror("Error", "User not found or incorrect credentials!")

    # OTP verification
    def send_otp_resetW(self):
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
            <p>Thank you,<br>Sahan Ranasingha</p>
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

    def on_login_click(self):
        self.destroy()
        self.parent.deiconify()
    
    def on_close(self):
        # Close the entire application
        self.master.destroy()
        sys.exit()
