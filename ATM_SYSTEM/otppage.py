from ATM_SYSTEM.homepage import MainForm
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import random
from twilio.rest import Client
import os
from dotenv import load_dotenv


class OtpForm:
    def __init__(self, master, cardnumber):
        self.master = master
        self.cardnumber = cardnumber
        self.random_otp = None

        # Initialize the OTP window
        self.init_otp_window()

    def init_otp_window(self):
        self.master.geometry('700x450')
        self.master.title('OTP Window')

        # Center the window
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        x = (ws - 450) / 2
        y = (hs - 280) / 2
        self.master.geometry(f'450x280+{int(x)}+{int(y)}')

        # Disable window resizing
        self.master.resizable(False, False)

        # Style
        self.master.config(bg="#f2f2f2")  # Body
        # Main Content Frame
        self.frame = tk.Frame(self.master, background="#f2f2f2")
        self.otp_lebel = ttk.Label(self.frame, text='OTP:', background="#f2f2f2", font=('Verdana', 11, 'bold'))
        self.otp_textbox = ttk.Entry(self.frame, font=('Verdana', 12), width=15)
        # Button Frame
        self.frame2 = tk.Frame(self.master, background="#f2f2f2")
        self.btn_login = tk.Button(self.frame2, text='LOGIN', fg='white', bg='#36d6d6', command=self.login_func)
        self.btn_resend_otp = tk.Button(self.frame2, text='Resend OTP', fg='white', bg='#36d6d6', command=self.resend_otp)

        # Pack
        # Main Content Frame
        self.frame.place(rely=0.4, relx=0.45, anchor=tk.CENTER)
        self.otp_lebel.grid(row=1, column=1, padx=(0, 10), pady=(0, 10))
        self.otp_textbox.grid(row=1, column=2, padx=(10, 0), pady=(0, 10))
        # Button Frame
        self.frame2.place(rely=0.65, relx=0.51, anchor=tk.S)
        self.btn_login.grid(row=1, column=1, padx=7, pady=10)
        self.btn_resend_otp.grid(row=1, column=2, padx=9, pady=10)

        # Generate and send OTP
        self.send_otp()

    def send_otp(self):
        self.random_otp = random.randint(111111, 999999)
        print(self.random_otp)  # Debug Only

        # -------------- Unlock during Production --------------
        # # Fetch phone number using card number from the database
        # phone_number = self.fetch_phone_by_card(self.cardnumber)
        #
        # if phone_number:
        #     load_dotenv()
        #     account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        #     auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        #     verified_number = phone_number
        #     client = Client(account_sid, auth_token)
        #     client.messages.create(
        #         from_=os.getenv('TWILIO_FROM_NUMBER'),
        #         to=verified_number,
        #         body=f'Your OTP for SAS ATM Service is {self.random_otp}'
        #     )
        # else:
        #     print("Phone number not found for the given card number:", self.cardnumber)

    def login_func(self):
        entered_otp = self.otp_textbox.get()

        # Check if entered OTP is a valid integer
        if not entered_otp.isdigit():
            messagebox.showerror("Invalid OTP", "Please enter a valid OTP (numeric digits only).")
            self.otp_textbox.delete(0, 'end')  # Clear the contents of the OTP entry box
            return

        if int(entered_otp) == self.random_otp:
            if self.random_otp == "done":
                messagebox.showinfo("showinfo", "Already Logged In")
            else:
                self.random_otp = "done"
                mainformwindow = tk.Toplevel()
                MainForm(mainformwindow, self.cardnumber)
                self.master.withdraw()  # Hide the OTP form window
                self.master.protocol('WM_DELETE_WINDOW', self.on_close)
        else:
            messagebox.showinfo("showinfo", "Wrong OTP")
            self.otp_textbox.delete(0, 'end')  # Clear the contents of the OTP entry box

    def on_close(self):
        self.master.destroy()  # Close the OTP_form window

    def resend_otp(self):
        self.send_otp()
        self.otp_textbox.delete(0, 'end')  # Clear the contents of the OTP entry box

    @staticmethod
    def fetch_phone_by_card(cardnumber):
        try:
            with mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='',
                    port='3306',
                    database='sas_bank_db'
            ) as connection:
                c = connection.cursor()
                select_query = 'SELECT Phone_Number FROM `account_holders` WHERE cardnumber = %s'
                vals = (cardnumber,)
                c.execute(select_query, vals)
                mobile_number = c.fetchone()
                return mobile_number[0] if mobile_number else None
        except mysql.connector.Error as err:
            print("Error accessing database:", err)
            return None


if __name__ == '__main__':
    root = tk.Tk()
    OtpForm(root)
    root.resizable(False, False)  # Prevent resizing the window in both directions
    root.mainloop()
