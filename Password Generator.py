import string
import random
from tkinter import *
from tkinter import messagebox
import sqlite3

# Initialize Database
with sqlite3.connect("users.db") as db:
    cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (Username TEXT NOT NULL, GeneratedPassword TEXT NOT NULL);")
db.commit()
db.close()


class PasswordGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title('🔐 Password Generator')
        self.master.geometry('680x500')
        self.master.config(bg='#1E1E2F')  # Dark Background
        self.master.resizable(False, False)

        # Variables
        self.username = StringVar()
        self.password_len = IntVar()
        self.generated_password = StringVar()

        # Create a main frame to center all widgets
        main_frame = Frame(master, bg='#1E1E2F')
        main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Header Label
        Label(main_frame, text="🔐 PASSWORD GENERATOR 🔐", fg='#F5C518', bg='#1E1E2F', 
              font='Helvetica 22 bold').grid(row=0, column=0, columnspan=2, pady=15)

        # Input Fields
        Label(main_frame, text="Enter Username:", font='Verdana 14 bold', bg='#1E1E2F', fg='#FFD700').grid(row=1, column=0, padx=10, pady=10, sticky=E)
        self.username_entry = Entry(main_frame, textvariable=self.username, font='Verdana 14', bd=5, relief='ridge', fg='black', bg='#F5F5F5')
        self.username_entry.grid(row=1, column=1, pady=5, padx=10)

        Label(main_frame, text="Password Length (6-100):", font='Verdana 14 bold', bg='#1E1E2F', fg='#FFD700').grid(row=2, column=0, padx=10, pady=10, sticky=E)
        self.length_entry = Entry(main_frame, textvariable=self.password_len, font='Verdana 14', bd=5, relief='ridge', fg='black', bg='#F5F5F5')
        self.length_entry.grid(row=2, column=1, pady=5, padx=10)

        Label(main_frame, text="Generated Password:", font='Verdana 14 bold', bg='#1E1E2F', fg='#FFD700').grid(row=3, column=0, padx=10, pady=10, sticky=E)
        self.password_entry = Entry(main_frame, textvariable=self.generated_password, font='Verdana 14 bold', bd=5, relief='ridge', fg='#DC143C', bg='#FFF8DC')
        self.password_entry.grid(row=3, column=1, pady=5, padx=10)

        # Buttons (Center aligned)
        Button(main_frame, text="🔄 GENERATE PASSWORD", bd=4, relief='solid', font='Verdana 14 bold', fg='#FFFFFF', bg='#FF5733',
               command=self.generate_password).grid(row=4, column=0, columnspan=2, pady=15, ipadx=15)

        Button(main_frame, text="✔ ACCEPT", bd=4, relief='solid', font='Verdana 14 bold', fg='#FFFFFF', bg='#28A745',
               command=self.accept_password).grid(row=5, column=0, columnspan=2, pady=10, ipadx=35)

        Button(main_frame, text="❌ RESET", bd=4, relief='solid', font='Verdana 14 bold', fg='#FFFFFF', bg='#C70039',
               command=self.reset_fields).grid(row=6, column=0, columnspan=2, pady=10, ipadx=45)

    def generate_password(self):
        """Generate a random secure password"""
        username = self.username.get().strip()
        
        # Validate password length
        try:
            length = int(self.password_len.get())
        except ValueError:
            messagebox.showerror("Error", "Password length must be a number!")
            return
        
        if not username:
            messagebox.showerror("Error", "Username cannot be empty!")
            return
        if not username.isalpha():
            messagebox.showerror("Error", "Username must only contain letters!")
            self.username_entry.delete(0, END)
            return
        if length < 6 or length > 100:  # Restrict length between 6-100
            messagebox.showerror("Error", "Password length must be between 6 and 100!")
            return

        # Generate password
        all_chars = string.ascii_letters + string.digits + "@#%&()\"?!"
        password = ''.join(random.sample(all_chars, length))

        # Set generated password
        self.generated_password.set(password)

    def accept_password(self):
        """Save the generated password to the database"""
        username = self.username.get().strip()
        password = self.generated_password.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Username and Password cannot be empty!")
            return

        with sqlite3.connect("users.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE Username = ?", (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                messagebox.showerror("Error", "This username already exists! Please use another username.")
                return

            cursor.execute("INSERT INTO users (Username, GeneratedPassword) VALUES (?, ?)", (username, password))
            db.commit()
            messagebox.showinfo("Success!", "Password saved successfully.")

    def reset_fields(self):
        """Reset all input fields"""
        self.username_entry.delete(0, END)
        self.length_entry.delete(0, END)
        self.password_entry.delete(0, END)


if __name__ == '__main__':
    root = Tk()
    PasswordGenerator(root)
    root.mainloop()
