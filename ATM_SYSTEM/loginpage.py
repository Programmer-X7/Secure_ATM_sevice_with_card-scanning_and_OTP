# Dependencies
# pip install tk pyzbar opencv-python mysql-connector-python cryptography python-decouple twilio python-dotenv pillow

from ATM_SYSTEM.otppage import OtpForm
import tkinter as tk
from tkinter import messagebox, ttk, PhotoImage
import cv2
from pyzbar.pyzbar import decode as pyzbar_decode
import mysql.connector
from cryptography.fernet import Fernet
from decouple import config

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
title_font_size = 22
label_font_size = 14
entry_font_size = 12
btn_font_size = 10


class LoginForm:
    CARD_ENCRYPTION_KEYS = {
        config('CARDNUMBER_1'): config('ENCRYPTION_KEY_1'),
        config('CARDNUMBER_2'): config('ENCRYPTION_KEY_2'),
        config('CARDNUMBER_3'): config('ENCRYPTION_KEY_3'),
        config('CARDNUMBER_4'): config('ENCRYPTION_KEY_4')
    }

    def __init__(self, master):

        self.master = master
        self.master.title("ATM SERVICES")

        # Width and height
        w = 580
        h = 400

        # Center the window
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        x = (ws - w) / 2
        y = (hs - h) / 2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

        # Create styles
        self.master.config(bg=bg_color)  # Body
        self.title_lbl = tk.Label(
            self.master,
            text='WELCOME TO ATM SERVICES',
            font=(label_font, title_font_size, 'bold'),
            fg='#2674f0',
            bg=bg_color)  # Title

        # Main Content Frame
        self.frame = tk.Frame(self.master, background=bg_color)
        self.cardnumberLabel = ttk.Label(
            self.frame,
            text='Card Number:',
            background=bg_color,
            foreground=text_color,
            font=(label_font, label_font_size, 'bold'))
        self.cardnumberTextbox = ttk.Entry(
            self.frame,
            font=(entry_font, entry_font_size, 'bold'),
            justify="center"
        )
        self.btnScanQR = tk.Button(
            self.frame,
            text='Scan',
            width=6,
            height=1,
            bg=btn_primary,
            fg=bg_color,
            activebackground=btn_secondary,
            activeforeground=bg_color,
            cursor='hand2',
            font=(btn_font, btn_font_size, 'bold'),
            command=self.scan_barcode)
        self.pinLabel = ttk.Label(
            self.frame,
            text='PIN:',
            background=bg_color,
            foreground=text_color,
            font=(label_font, label_font_size, 'bold'))
        self.pinTextbox = ttk.Entry(
            self.frame,
            font=(entry_font, entry_font_size, 'bold'),
            show='*',
            justify="center",
        )

        # Button Frame
        self.frame2 = tk.Frame(self.master, background=bg_color)
        self.btnSendOtp = tk.Button(
            self.frame2,
            text='Send OTP',
            fg=bg_color,
            bg=btn_primary,
            width=9,
            height=1,
            activebackground=btn_secondary,
            activeforeground=bg_color,
            cursor='hand2',
            font=(btn_font, btn_font_size, 'bold'),
            command=self.otp_func)
        self.btnCancel = tk.Button(
            self.frame2,
            text='Cancel',
            fg=bg_color,
            bg=btn_primary,
            width=9,
            height=1,
            activebackground=btn_secondary,
            activeforeground=bg_color,
            cursor='hand2',
            font=(btn_font, btn_font_size, 'bold'),
            command=self.close_window)

        # Packing the frames
        # Title
        self.title_lbl.place(relx=0.5, rely=0.12, anchor=tk.N)
        # Main Content Frame
        self.frame.place(relx=0.48, rely=0.45, anchor=tk.CENTER)
        self.cardnumberLabel.grid(row=1, column=1, padx=(0, 10), pady=(0, 10))
        self.cardnumberTextbox.grid(row=1, column=2, padx=(10, 10), pady=(0, 10))
        self.btnScanQR.grid(row=1, column=3, padx=(5, 0), pady=(0, 10))
        self.pinLabel.grid(row=2, column=1)
        self.pinTextbox.grid(row=2, column=2, padx=10, pady=10)
        # Button Frame
        self.frame2.place(relx=0.54, rely=0.7, anchor=tk.S)
        self.btnSendOtp.grid(row=1, column=1, padx=7, pady=10)
        self.btnCancel.grid(row=1, column=2, padx=9, pady=10)

    # START Barcode/QR Code Scanner
    def scan_barcode(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, 500)  # Camera frame width
        cap.set(4, 360)  # Camera frame height
        scanned_data = ''

        while True:
            ret, frame = cap.read()
            barcodes = pyzbar_decode(frame)

            for barcode in barcodes:
                scanned_data = barcode.data.decode("utf-8")
                x_2, y_2, w_2, h_2 = barcode.rect
                cv2.rectangle(
                    frame,
                    (x_2, y_2),
                    (x_2 + w_2, y_2 + h_2),
                    (0, 255, 0),
                    2
                )

            cv2.imshow("Card Scanner", frame)
            if cv2.waitKey(1) & 0xFF == 27 or scanned_data:  # Press 'Esc' or barcode detected to exit the loop
                break

        cap.release()
        cv2.destroyAllWindows()

        if scanned_data:
            self.cardnumberTextbox.delete(0, tk.END)
            self.cardnumberTextbox.insert(0, scanned_data)
        else:
            messagebox.showinfo("Card Scanner", "No barcode detected.")

    # END of Barcode Scanner

    # Destroy Active Window
    def close_window(self):
        self.master.destroy()

    def otp_func(self):
        cardnumber = self.cardnumberTextbox.get()
        pin = self.pinTextbox.get()

        encryption_key = self.CARD_ENCRYPTION_KEYS.get(cardnumber)

        if encryption_key is None:
            messagebox.showwarning('Error', 'Enter a Valid Card Number First')
            return

        cipher_suite = Fernet(encryption_key)

        # START Connection with DataBase
        with mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                port='3306',
                database='sas_bank_db'
        ) as connection:
            c = connection.cursor()
            select_query = 'SELECT `pin` FROM `account_holders` WHERE `cardnumber` = %s'
            vals = (cardnumber,)
            c.execute(select_query, vals)
            encrypted_pin = c.fetchone()
        # END Connection with DataBase

        # Start Validate Credentials
        if encrypted_pin is not None:
            decrypted_pin = self.decrypt_pin(encrypted_pin[0], cipher_suite)
            if decrypted_pin == pin:
                otpFormwindow = tk.Toplevel()
                OtpForm(otpFormwindow, cardnumber)
                self.master.withdraw()
                otpFormwindow.protocol('WM_DELETE_WINDOW', self.close_window)
            else:
                messagebox.showwarning('Error', 'Enter a Valid PIN')
                self.pinTextbox.delete(0, 'end')  # Clear the contents of Pin entry box
        else:
            messagebox.showwarning('Error', 'Enter a Valid Card Number First')

    # Decrypt PIN
    @staticmethod
    def decrypt_pin(encrypted_pin, cipher_suite):
        try:
            decrypted_pin = cipher_suite.decrypt(encrypted_pin.encode())
            return decrypted_pin.decode()
        except Exception as e:
            print(f"Error decrypting PIN: {str(e)}")
            return ''


if __name__ == '__main__':
    root = tk.Tk()
    LoginForm(root)
    img = PhotoImage(file='assets/icon.png')
    root.iconphoto(False, img)
    root.resizable(False, False)
    root.mainloop()
