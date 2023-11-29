from ATM_SYSTEM.otppage import OtpForm
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import cv2
from pyzbar.pyzbar import decode as pyzbar_decode
import mysql.connector
from cryptography.fernet import Fernet
from decouple import config

# Color Constants
bg_color = "#221824"
text_primary = "#d87bf3"
btn_primary = bg_color
btn_secondary = "#1c589e"
# btn_primary = "#387ed1"
# btn_secondary = "#1c589e"


class LoginForm:
    CARD_ENCRYPTION_KEYS = {
        config('CARDNUMBER_1'): config('ENCRYPTION_KEY_1'),
        config('CARDNUMBER_2'): config('ENCRYPTION_KEY_2'),
        config('CARDNUMBER_3'): config('ENCRYPTION_KEY_3'),
        config('CARDNUMBER_4'): config('ENCRYPTION_KEY_4')
    }

    def __init__(self, master):

        self.master = master
        self.master.title("Login Window")

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
            font=('verdana', 20, 'bold'),
            fg=text_primary,
            bg=bg_color)  # Title
        # Main Content Frame
        self.frame = tk.Frame(self.master, background=bg_color)
        self.cardnumberLabel = ttk.Label(
            self.frame,
            text='Card Number:',
            background=bg_color,
            foreground=text_primary,
            font=('verdana', 12, 'bold'))
        self.cardnumberTextbox = ttk.Entry(self.frame)
        self.btnScanQR = tk.Button(
            self.frame,
            text='Scan',
            width=6,
            height=1,
            bg=btn_primary,
            fg=text_primary,
            activebackground=btn_secondary,
            activeforeground=bg_color,
            cursor='hand2',
            borderwidth=2,

            font=('TkDefaultFont', 10, 'bold'),
            command=self.scan_barcode)
        self.pinLabel = ttk.Label(
            self.frame,
            text='PIN:',
            background=bg_color,
            foreground=text_primary,
            font=('verdana', 12, 'bold'))
        self.pinTextbox = ttk.Entry(self.frame, show='*')
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
            border=0,
            font=('TkDefaultFont', 10, 'bold'),
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
            border=0,
            font=('TkDefaultFont', 10, 'bold'),
            command=self.close_window)

        # Packing the frames
        self.title_lbl.place(rely=0.1, relx=0.5, anchor=tk.N)  # Title
        # Main Content Frame
        self.frame.place(rely=0.5, relx=0.48, anchor=tk.CENTER)
        self.cardnumberLabel.grid(row=1, column=1, padx=(0, 10), pady=(0, 10))
        self.cardnumberTextbox.grid(row=1, column=2, padx=(10, 10), pady=(0, 10))
        self.btnScanQR.grid(row=1, column=3, padx=(5, 0), pady=(0, 10))
        self.pinLabel.grid(row=2, column=1)
        self.pinTextbox.grid(row=2, column=2, padx=10, pady=10)
        # Button Frame
        self.frame2.place(rely=0.75, relx=0.55, anchor=tk.S)
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
                x_2, y_2, w_2, h_2 = barcode.rect  # Get the bounding box of the detected barcode
                cv2.rectangle(frame, (x_2, y_2), (x_2 + w_2, y_2 + h_2), (0, 255, 0),
                              2)  # Draw a green rectangle around the barcode

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

    # START Validate Credentials Function
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

        # Start Validate Credentials Function
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

    # END Validate Credentials Function

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
    root.resizable(False, False)  # Prevent from resizing the window in both directions
    root.mainloop()
