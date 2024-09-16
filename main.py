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
import requests
import json

from userDashboard import DashboardWindow
from adminDashboard import AdminDashboardWindow
from userRegistration import RegisterWindow
from userForgotPass import ForgotWindow

# Update checking
CURRENT_VERSION = "1.0"
VERSION_INFO_URL = "https://hostel-management-system---aux.web.app/version_info.json"

def check_for_updates():
    try:
        response = requests.get(VERSION_INFO_URL)
        if response.status_code == 200:
            version_info = response.json()
            latest_version = version_info["latest_version"]
            if latest_version != CURRENT_VERSION:
                notify_update_available(version_info["update_url"])
    except Exception as e:
        print(f"Error checking for updates: {e}")

def notify_update_available(update_url):
    while True:
        result = messagebox.askyesno("Update Available", "A new version of the application is available. Would you like to update?")
        if result:
            import webbrowser
            webbrowser.open(update_url)

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

# Initialize Firebase
initialize_firebase()

# Login window
class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.center_window()

        self.geometry("1366x768")
        self.title("Login - Hostel Management System")
        self.iconbitmap(resource_path("Assets/icon.ico"))
        self.configure(bg="#ffffff")

        # Disable window resizing
        self.resizable(False, False)

        # Automatically check for updates when the login window loads
        self.after(1000, check_for_updates)

        # Load the image
        img1 = Image.open(resource_path("Assets/background.jpg"))

        # Resize the image to the desired width and height
        img1 = img1.resize((1366, 768), Image.LANCZOS)

        # Create a PhotoImage object
        self.bg_image = ImageTk.PhotoImage(img1)

        # Create a label with the image and place it with specific dimensions
        l1 = customtkinter.CTkLabel(master=self, image=self.bg_image, width=1366, height=768)
        l1.pack()


        frame = customtkinter.CTkFrame(master=l1, width=450, height=400, corner_radius=15, fg_color="#333333")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        l2 = customtkinter.CTkLabel(master=frame, text="Log into your Account", font=("Arial", 28))
        l2.place(x=90, y=60)

        self.username_entry = customtkinter.CTkEntry(master=frame, width=350, placeholder_text="Username")
        self.username_entry.place(x=50, y=140)

        self.password_entry = customtkinter.CTkEntry(master=frame, width=350, placeholder_text="Password", show="*")
        self.password_entry.place(x=50, y=200)

        forgotPassword_link = customtkinter.CTkLabel(master=frame, text="Forgot Password?", width=22, cursor="hand2")
        forgotPassword_link.place(x=275, y=240)
        forgotPassword_link.bind("<Button-1>", lambda e: self.on_forgot_password_click())

        login_button = customtkinter.CTkButton(master=frame, text="Login", width=350, cursor="hand2", command=self.authenticate_user)
        login_button.place(x=50, y=280)

        register_button = customtkinter.CTkButton(master=frame, text="Register", width=350, cursor="hand2", command=self.on_register_click)
        register_button.place(x=50, y=330)
    
    def authenticate_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        user_data = read_data(f'users/{username}')
        if user_data and user_data.get('password') == hashed_password:
            #messagebox.showinfo("Success", "Login successful")
            self.open_dashboard_window(username)
        elif username == "admin" and password == "propertymanagementauxmen@admin":
            self.withdraw()
            admin_dashboard_window = AdminDashboardWindow(self, username)
            admin_dashboard_window.mainloop()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def open_dashboard_window(self, username):
        self.withdraw()
        dashboard_window = DashboardWindow(self, username)
        dashboard_window.mainloop()
    
    def on_register_click(self):
        self.withdraw()
        register_window = RegisterWindow(self)
        register_window.mainloop()

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (1366 / 2)
        y = (screen_height / 2) - (768 / 2)
        self.geometry(f"1366x768+{int(x)}+{int(y)}")

    def on_forgot_password_click(self):
        self.withdraw()
        forgot_window = ForgotWindow(self)
        forgot_window.mainloop()

if __name__ == "__main__":
    app = LoginWindow()
    #app = DashboardWindow(None, "sahan")
    #app = AdminDashboardWindow(None, "sahan")
    app.mainloop()