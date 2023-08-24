import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import cv2
from pyzbar.pyzbar import decode as pyzbar_decode
import mysql.connector
from cryptography.fernet import Fernet
from decouple import config
from ATM_SYSTEM.otppage import OtpForm


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
        w = 630
        h = 450

        # Center the window
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        x = (ws - w) / 2
        y = (hs - h) / 2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

        # Create styles
        self.style = ttk.Style()
        self.style.configure('TLabel', background='#fff', font=('Verdana', 16))
        self.style.configure('TEntry', font=('Verdana', 12), width=20, borderwidth='2', relief='ridge')
        self.style.configure('TButton', font=('Verdana', 12), padx=25, pady=10)

        # Create widgets
        self.frame = ttk.Frame(self.master)
        self.btnsFrame = ttk.Frame(self.frame, padding=(40, 15))

        self.windowTitle = ttk.Label(self.frame, text='Welcome', font=('Tahoma', 20), foreground='blue')
        self.cardnumberLabel = ttk.Label(self.frame, text='Card Number:')
        self.cardnumberTextbox = ttk.Entry(self.frame)
        self.pinLabel = ttk.Label(self.frame, text='PIN:')
        self.pinTextbox = ttk.Entry(self.frame, show='*')

        self.btnScanBarcode = ttk.Button(self.btnsFrame, text='Scan', style='TButton', command=self.scan_barcode)
        self.btnSendOtp = ttk.Button(self.btnsFrame, text='Send OTP', style='TButton', command=self.otp_func)
        self.btnCancel = ttk.Button(self.btnsFrame, text='Cancel', style='TButton', command=self.close_window)

        # Place widgets
        self.frame.pack(fill='both', expand=True)
        self.windowTitle.grid(row=0, column=1, columnspan=2, pady=(30, 20))
        self.cardnumberLabel.grid(row=1, column=0)
        self.cardnumberTextbox.grid(row=1, column=1)
        self.pinLabel.grid(row=2, column=0, pady=(10, 0))
        self.pinTextbox.grid(row=2, column=1, pady=(10, 0))
        self.btnsFrame.grid(row=3, column=0, columnspan=2, pady=10)
        self.btnScanBarcode.grid(row=1, column=2, padx=(0, 35))
        self.btnSendOtp.grid(row=0, column=0, padx=(0, 35))
        self.btnCancel.grid(row=0, column=1)

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


def main():
    root = tk.Tk()
    LoginForm(root)
    root.resizable(False, False)  # Prevent from resizing the window in both directions
    root.mainloop()


if __name__ == '__main__':
    main()
