import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ATM_SYSTEM.homepage import mainform
import mysql.connector
import random
from twilio.rest import Client
import os
from dotenv import load_dotenv


class OtpForm:
    def __init__(self, master, cardnumber):
        self.master = master

        # Store the cardnumber in the instance variable
        self.cardnumber = cardnumber

        self.master.geometry('700x450')
        self.master.title('OTP Window')

        # Width and height
        W = 450
        H = 280

        # Center the window
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        x = (ws - W) / 2
        y = (hs - H) / 2
        self.master.geometry('%dx%d+%d+%d' % (W, H, x, y))

        # Disable window resizing from both axis
        self.master.resizable(False, False)

        # Generate random OTP
        self.random_otp = random.randint(111111, 999999)
        # See the OTP in console
        print(self.random_otp)  # Debug Only

        # Start - OTP Sender
        # ------------- Unlock during Actual Testing or Production --------------

        # # Load environment variables from .env file
        # load_dotenv()
        #
        # # Fetch phone number using card number from the database
        # phoneNumber = self.fetch_phone_by_card(self.cardnumber)
        #
        # if phoneNumber:
        #     account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        #     auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        #     verified_number = phoneNumber
        #     self.client = Client(account_sid, auth_token)
        #     self.client.messages.create(
        #         from_=os.getenv('TWILIO_FROM_NUMBER'),
        #         to=verified_number,
        #         body=f'Your OTP for SAS ATM Service is {self.random_otp}'
        #     )
        # else:
        #     print("Phone number not found for the given card number:", self.cardnumber)

        # End - OTP Sender

        # Create & Pack Frame
        self.frame = ttk.Frame(self.master)
        self.frame.pack(fill='both')

        # Create styles
        self.style = ttk.Style()
        self.style.configure('TLabel', background='#fff', font=('Verdana', 16))
        self.style.configure('TEntry', font=('Verdana', 12), width=10, borderwidth='2', relief='ridge')
        self.style.configure('TButton', font=('Verdana', 12), padx=25, pady=10)

        self.window_title = ttk.Label(self.frame, text='Login Window', style='TLabel')
        self.window_title.grid(row=0, column=0, columnspan=2)

        self.otp_label = ttk.Label(self.frame, text='OTP:', style='TLabel')
        self.otp_label.grid(row=1, column=0, pady=(10, 0))

        self.otp_textbox = ttk.Entry(self.frame, font=('Verdana', 12), style='TEntry')
        self.otp_textbox.grid(row=1, column=1, pady=(10, 0))

        self.btns_frame = ttk.Frame(self.frame, padding=(40, 15))
        self.btns_frame.grid(row=4, column=0, columnspan=2, pady=10)

        self.btn_login = ttk.Button(self.btns_frame, text='LOGIN', style='TButton', command=self.login_func)
        self.btn_login.grid(row=0, column=0, padx=(0, 35))

        self.btn_resend_otp = ttk.Button(self.btns_frame, text='Resend OTP', style='TButton', command=self.resend_otp)
        self.btn_resend_otp.grid(row=0, column=1)

    # START - OTP Checker & LOGIN
    def login_func(self):
        entered_otp = self.otp_textbox.get()

        if int(entered_otp) == self.random_otp:
            if self.random_otp == "done":
                messagebox.showinfo("showinfo", "Already Logged In")
            else:
                self.random_otp = "done"
                mainformwindow = tk.Toplevel()
                mainform(mainformwindow)
                self.master.withdraw()  # Hide the OTP form window
                self.master.protocol('WM_DELETE_WINDOW', self.on_close)
        else:
            messagebox.showinfo("showinfo", "Wrong OTP")
        # END - OTP Checker & LOGIN

    # Destroy Active Window
    def on_close(self):
        self.master.destroy()  # Close the OTP_form window

    # START - OTP RE-SENDER
    def resend_otp(self):
        # Generate random OTP
        self.random_otp = random.randint(111111, 999999)
        # See the OTP in console
        print(self.random_otp)    # Debug Only

        # START - OTP (RE-) Sender
        # ------------- Unlock during Actual Testing or Production --------------

        # # Fetch phone number using card number from the database
        # phoneNumber = self.fetch_phone_by_card(self.cardnumber)
        # # print(phoneNumber)    # Debug Only (type: <str>)
        # if phoneNumber:
        #     # Load environment variables from .env file
        #     load_dotenv()
        #
        #     account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        #     auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        #     verified_number = phoneNumber
        #     self.client = Client(account_sid, auth_token)
        #     self.client.messages.create(
        #         from_=os.getenv('TWILIO_FROM_NUMBER'),
        #         to=verified_number,
        #         body=f'Your OTP for SAS ATM Service is {self.random_otp}'
        #     )
        # else:
        #     print("Phone number not found for the given card number:", self.cardnumber)

        # END - OTP (RE-) Sender

    # START - Fetch Phone Number using Card Number
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
    # END - Fetch Phone Number using Card Number


def main():
    root = tk.Tk()
    OtpForm(root)
    root.resizable(False, False)  # Prevent resizing the window in both directions
    root.mainloop()


if __name__ == '__main__':
    main()
