# Dependencies
# pip install tk pyzbar opencv-python mysql-connector-python cryptography python-decouple twilio python-dotenv pillow

from ATM_SYSTEM.homepage import MainForm
import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import random
from twilio.rest import Client
import os
from dotenv import load_dotenv

# Colors
bg_color = "#fff"
text_color = "#2a78d1"
btn_primary = "#387ed1"
btn_secondary = "#1c589e"

# Fonts
# Family
label_font = 'Times New Roman'
btn_font = 'Ubuntu'
entry_font = 'Times New Roman'
# Size
title_font_size = 23
label_font_size = 14
entry_font_size = 12
btn_font_size = 10


class OtpForm:
    def __init__(self, master, cardnumber):
        self.master = master
        self.cardnumber = cardnumber
        self.random_otp = None
        self.init_otp_window()

    def init_otp_window(self):
        self.master.geometry('700x450')
        self.master.title('ATM SERVICES')

        # Center the window
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        x = (ws - 450) / 2
        y = (hs - 280) / 2
        self.master.geometry(f'450x280+{int(x)}+{int(y)}')
        self.master.resizable(False, False)

        # Style
        self.master.config(bg=bg_color)  # Body
        # Main Content Frame
        self.frame = tk.Frame(
            self.master,
            background=bg_color
        )
        self.otp_label = ttk.Label(
            self.frame,
            text='OTP:',
            background=bg_color,
            foreground=text_color,
            font=(label_font, label_font_size, 'bold')
        )
        self.otp_textbox = ttk.Entry(
            self.frame,
            font=(entry_font, entry_font_size, 'bold'),
            width=20,
            justify="center"
        )

        # Button Frame
        self.frame2 = tk.Frame(
            self.master,
            background=bg_color
        )
        self.btn_login = tk.Button(
            self.frame2,
            text='LOGIN',
            fg=bg_color,
            bg=btn_primary,
            width=8,
            height=1,
            activeforeground=bg_color,
            activebackground=btn_secondary,
            cursor='hand2',
            font=(btn_font, btn_font_size, 'bold'),
            command=self.login_func
        )
        self.btn_resend_otp = tk.Button(
            self.frame2,
            text='Resend',
            fg=bg_color,
            bg=btn_primary,
            width=8,
            height=1,
            activeforeground=bg_color,
            activebackground=btn_secondary,
            cursor='hand2',
            font=(btn_font, btn_font_size, 'bold'),
            command=self.resend_otp
        )

        # Pack
        # Main Content Frame
        self.frame.place(rely=0.4, relx=0.45, anchor=tk.CENTER)
        self.otp_label.grid(row=1, column=1, padx=(0, 10), pady=(0, 10))
        self.otp_textbox.grid(row=1, column=2, padx=(10, 0), pady=(0, 10))
        # Button Frame
        self.frame2.place(rely=0.65, relx=0.51, anchor=tk.S)
        self.btn_login.grid(row=1, column=1, padx=7, pady=10)
        self.btn_resend_otp.grid(row=1, column=2, padx=9, pady=10)

        self.send_otp()

    # Generate and send OTP
    def send_otp(self):
        self.random_otp = random.randint(111111, 999999)
        # print(self.random_otp)  # Debug

        # -------------- Unlock during Production --------------
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
            self.otp_textbox.delete(0, 'end')
            return

        if int(entered_otp) == self.random_otp:
            if self.random_otp == "done":
                messagebox.showinfo("showinfo", "Already Logged In")
            else:
                self.random_otp = "done"
                mainformwindow = tk.Toplevel()
                MainForm(mainformwindow, self.cardnumber)
                self.master.withdraw()
                self.master.protocol('WM_DELETE_WINDOW', self.on_close)
        else:
            messagebox.showinfo("showinfo", "Wrong OTP")
            self.otp_textbox.delete(0, 'end')

    def on_close(self):
        self.master.destroy()

    def resend_otp(self):
        self.send_otp()
        self.otp_textbox.delete(0, 'end')

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
