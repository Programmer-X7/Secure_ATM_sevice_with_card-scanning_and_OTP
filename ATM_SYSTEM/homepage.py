# Dependencies
# pip install tk pyzbar opencv-python mysql-connector-python cryptography python-decouple twilio python-dotenv pillow

import tkinter as tk
from tkinter import messagebox, ttk, PhotoImage
from PIL import Image, ImageTk
import mysql.connector

# Colors
bg_color = "#fff"
bg_secondary = "#99b3e8"  # Sidebar BG
nav_bg = '#dce0e3'
nav_text = '#000'
btn_primary = "#387ed1"
btn_secondary = "#1c589e"
label_color = '#2674f0'
text_white = 'white'


# Fonts
# Family
label_font = 'Times New Roman'
btn_font = 'Ubuntu'
entry_font = 'Times New Roman'
# Size
title_font_size = 20
label_font_size = 14
entry_font_size = 12
btn_font_size = 10


class MainForm:
    def __init__(self, root, cardnumber):
        self.root = root
        self.cardnumber = cardnumber
        self.root.title("ATM SERVICES")

        window_width = 700
        window_height = 480
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.initialize_database_connection()
        self.create_top_frame()
        self.create_dynamic_frame()
        self.create_sidebar_frame()

        self.balance_var = None
        self.load_initial_data()

    def create_top_frame(self):
        self.top_frame = tk.Frame(self.root, height=130, bg=nav_bg)
        self.top_frame.pack(fill=tk.X)

        labels = [
            ("                Name:", "name_value_label"),
            ("           Balance:", "balance_value_label")
        ]

        for text, label_name in labels:
            label = tk.Label(self.top_frame, text=text, font=(label_font, label_font_size, 'bold'), bg=nav_bg, fg=nav_text)
            label.pack(side=tk.LEFT)
            setattr(self, label_name,
                    tk.Label(self.top_frame, text="", font=(label_font, label_font_size, 'bold'), bg=nav_bg, fg=nav_text))
            getattr(self, label_name).pack(side=tk.LEFT)

    def initialize_database_connection(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            port='3306',
            database='sas_bank_db'
        )
        self.cursor = self.connection.cursor()

    def load_initial_data(self):
        initial_card_number = self.cardnumber
        initial_data = self.get_data_from_database(initial_card_number)

        if initial_data:
            initial_name, initial_balance = initial_data
            self.name_value_label.config(text=initial_name)
            self.balance_var = tk.StringVar(value=f"{initial_balance:.2f}")
        else:
            self.name_value_label.config(text="Name not found")
            self.balance_var = tk.StringVar(value="Balance not found")

        self.balance_value_label.config(textvariable=self.balance_var)

    def get_data_from_database(self, card_number):
        try:
            query = "SELECT name, balance FROM `account_holders` WHERE cardnumber = %s"
            self.cursor.execute(query, (card_number,))
            result = self.cursor.fetchone()

            if result:
                return result
            else:
                return None
        except Exception as e:
            return None

    def create_dynamic_frame(self):
        self.dynamic_frame = tk.Frame(self.root, bg=bg_color)
        self.dynamic_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.change_content("Initial Content")

    def create_sidebar_frame(self):
        self.sidebar_frame = tk.Frame(self.root, width=150, bg=bg_secondary)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        buttons = ["Withdraw", "Deposit", "QR Cash", "Transfer", "Mini Statement", "Change PIN", "Logout"]

        for button_text in buttons:
            button = tk.Button(
                self.sidebar_frame,
                text=button_text,
                bg=btn_primary,
                fg=text_white,
                activebackground=btn_secondary,
                activeforeground=text_white,
                cursor='hand2',
                font=(btn_font, btn_font_size, 'bold'),
                command=lambda
                text=button_text: self.change_content(text))
            button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=17)

    def change_content(self, content):
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        if content == "Initial Content":
            self.display_initial_content()
        elif content == "Withdraw":
            self.display_withdraw_content()
        elif content == "Deposit":
            self.display_deposit_content()
        elif content == "QR Cash":
            self.display_qr_cash()
        elif content == "Transfer":
            self.display_transfer_content()
        elif content == "Mini Statement":
            self.display_mini_statement()
        elif content == "Change PIN":
            self.display_change_pin_content()
        elif content == "Logout":
            self.logout()

    def display_initial_content(self):
        initial_content_label = tk.Label(
            self.dynamic_frame,
            text="Dear Customer,"
                 "\nChoose a Transaction to Proceed",
            font=(label_font, title_font_size, "bold"),
            bg=bg_color,
            fg=label_color,
        )
        initial_content_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

    def display_withdraw_content(self):
        title_label = tk.Label(
            self.dynamic_frame,
            text="CASH WITHDRAWAL",
            font=(label_font, title_font_size, "bold"),
            bg=bg_color,
            fg=label_color
        )
        title_label.pack(pady=20)

        amount_label = tk.Label(
            self.dynamic_frame,
            text="AMOUNT",
            bg=bg_color,
            fg=label_color,
            font=(label_font, label_font_size, "bold")
        )
        amount_label.pack(pady=8)

        self.amount_entry = ttk.Entry(
            self.dynamic_frame,
            font=(entry_font, entry_font_size, 'bold'),
            width=18,
            justify='center',
        )
        self.amount_entry.pack()

        withdraw_button = tk.Button(
            self.dynamic_frame,
            text="WITHDRAW",
            bg=btn_primary,
            fg=text_white,
            width=14,
            height=1,
            activebackground=btn_secondary,
            activeforeground=text_white,
            font=(btn_font, btn_font_size, 'bold'),
            cursor='hand2',
            command=self.perform_withdraw
        )
        withdraw_button.pack(pady=15)

    def display_deposit_content(self):
        title_label = tk.Label(
            self.dynamic_frame,
            text="CASH DEPOSIT",
            font=(label_font, title_font_size, "bold"),
            bg=bg_color,
            fg=label_color)
        title_label.pack(pady=20)

        deposit_amount_label = tk.Label(
            self.dynamic_frame,
            text="AMOUNT",
            bg=bg_color,
            fg=label_color,
            font=(label_font, label_font_size, "bold")
        )
        deposit_amount_label.pack(pady=8)

        self.deposit_amount_entry = ttk.Entry(
            self.dynamic_frame,
            font=(entry_font, entry_font_size),
            width=18,
            justify='center',
        )
        self.deposit_amount_entry.pack()

        deposit_button = tk.Button(
            self.dynamic_frame,
            text="DEPOSIT",
            bg=label_color,
            fg=text_white,
            width=12,
            height=1,
            activebackground=btn_secondary,
            activeforeground=text_white,
            font=(btn_font, btn_font_size, 'bold'),
            cursor='hand2',
            command=self.perform_deposit
        )
        deposit_button.pack(pady=15)

    def display_qr_cash(self):
        title_label = tk.Label(
            self.dynamic_frame,
            text="QR CASH",
            font=(label_font, title_font_size, "bold"),
            bg=bg_color,
            fg=label_color,
        )
        title_label.pack(pady=20)

        qrcode_scan_label = tk.Label(
            self.dynamic_frame,
            text="SCAN QR CODE",
            bg=bg_color,
            fg=label_color,
            font=(label_font, label_font_size, "bold")
        )
        qrcode_scan_label.pack(pady=14)

        try:
            # QR Code Image using Pillow
            photo = Image.open('assets/qrcode.png')
            resized_image = photo.resize((150, 150), Image.LANCZOS)
            converted_image = ImageTk.PhotoImage(resized_image)

            qr_code_label = tk.Label(
                self.dynamic_frame,
                image=converted_image,
                width=150,
                height=150,
            )
            qr_code_label.image = converted_image
            qr_code_label.pack()

        except Exception as e:
            print(f"Error loading image: {e}")

        deposit_button = tk.Button(
            self.dynamic_frame,
            text="CONFIRM",
            bg=label_color,
            fg=text_white,
            width=15,
            height=1,
            activebackground=btn_secondary,
            activeforeground=text_white,
            font=(btn_font, btn_font_size, 'bold'),
            cursor='hand2',
            command=self.perform_qr_cash
        )
        deposit_button.pack(pady=15)

    def display_transfer_content(self):
        title_label = tk.Label(
            self.dynamic_frame,
            text="MONEY TRANSFER",
            font=(label_font, title_font_size, "bold"),
            bg=bg_color,
            fg=label_color
        )
        title_label.pack(pady=20)

        labels = [
            ("Receiver Account Details", None),
            ("Enter AC No:", "enter_ac_entry"),
            ("Re-Enter AC No:", "re_enter_ac_entry"),
            ("Amount:", "amount_entry")
        ]

        for text, entry_name in labels:
            label = tk.Label(
                self.dynamic_frame,
                text=text,
                bg=bg_color,
                fg=label_color,
                font=(label_font, label_font_size, "bold")
            )
            label.pack(pady=7)

            if entry_name:
                entry = ttk.Entry(
                    self.dynamic_frame,
                    font=(entry_font, entry_font_size, 'bold'),
                    width=20,
                    justify='center',
                )
                entry.pack()
                setattr(self, entry_name, entry)

        transfer_button = tk.Button(
            self.dynamic_frame,
            text="Transfer",
            bg=label_color,
            fg=text_white,
            width=14,
            height=1,
            activebackground=btn_secondary,
            activeforeground=text_white,
            font=(btn_font, btn_font_size, 'bold'),
            cursor='hand2',
            command=self.perform_transfer
        )
        transfer_button.pack(pady=20)

    def display_mini_statement(self):
        title_label = tk.Label(
            self.dynamic_frame,
            text="MINI STATEMENT",
            font=(label_font, title_font_size, "bold"),
            bg=bg_color,
            fg=label_color,
        )
        title_label.pack(pady=20)

        amount_label = tk.Label(
            self.dynamic_frame,
            text="SELECT ACCOUNT TYPE",
            bg=bg_color,
            fg=label_color,
            font=(label_font, label_font_size, "bold")
        )
        amount_label.pack(pady=12)

        account_types = ["KCC", "Current", "Savings"]

        for account_type in account_types:
            button = tk.Button(
                self.dynamic_frame,
                text=account_type,
                bg=btn_primary,
                fg=text_white,
                width=10,
                height=1,
                activebackground=btn_secondary,
                activeforeground=text_white,
                font=(btn_font, btn_font_size, 'bold'),
                cursor='hand2',
                command=self.perform_mini_statement
            )
            button.pack(pady=10)

    def display_change_pin_content(self):
        title_label = tk.Label(
            self.dynamic_frame,
            text="Change Your PIN",
            font=(label_font, title_font_size, "bold"),
            bg=bg_color,
            fg=label_color
        )
        title_label.pack(pady=20)

        labels = [
            ("Enter Old PIN:", "old_pin_entry"),
            ("Enter New PIN:", "new_pin_entry"),
            ("Re-Enter New PIN:", "re_enter_new_pin_entry")
        ]

        for text, entry_name in labels:
            label = tk.Label(
                self.dynamic_frame,
                text=text,
                bg=bg_color,
                fg=label_color,
                font=(label_font, label_font_size, "bold")
            )
            label.pack(pady=7)

            if entry_name:
                entry = ttk.Entry(
                    self.dynamic_frame,
                    font=(entry_font, entry_font_size, 'bold'),
                    width=20,
                    justify='center',
                )
                entry.pack()
                setattr(self, entry_name, entry)

        change_pin_button = tk.Button(
            self.dynamic_frame,
            text="Change PIN",
            bg=label_color,
            fg=text_white,
            width=14,
            height=1,
            activebackground=btn_secondary,
            activeforeground=text_white,
            font=(btn_font, btn_font_size, 'bold'),
            cursor='hand2',
            command=self.perform_change_pin
        )
        change_pin_button.pack(pady=20)

    def perform_withdraw(self):
        amount = self.amount_entry.get()

        try:
            withdrawal_amount = float(amount)
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid withdrawal amount.")
            return

        current_balance = self.get_current_balance(self.cardnumber)

        if current_balance >= withdrawal_amount:
            new_balance = current_balance - withdrawal_amount
            self.update_balance(self.cardnumber, new_balance)
            self.balance_var.set(f"{new_balance:.2f}")

            self.clear_dynamic_frame()
            transaction_label = tk.Label(
                self.dynamic_frame,
                text="Transaction Complete."
                     "\n\nPlease Collect the Cash",
                bg=bg_color,
                fg=label_color,
                font=(label_font, title_font_size, 'bold'),
            )
            transaction_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        else:
            messagebox.showerror("Insufficient Balance", "You do not have sufficient balance for this withdrawal.")

    def get_current_balance(self, card_number):
        try:
            query = "SELECT balance FROM `account_holders` WHERE cardnumber = %s"
            self.cursor.execute(query, (card_number,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                return 0
        except Exception as e:
            return 0

    def update_balance(self, card_number, new_balance):
        try:
            query = "UPDATE `account_holders` SET balance = %s WHERE cardnumber = %s"
            self.cursor.execute(query, (new_balance, card_number))
            self.connection.commit()
        except Exception as e:
            messagebox.showerror("Error", "Error updating balance in the database.")
            print(e)

    def clear_dynamic_frame(self):
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

    def perform_deposit(self):
        amount = self.deposit_amount_entry.get()

        try:
            deposit_amount = float(amount)
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid deposit amount.")
            return

        current_balance = self.get_current_balance(self.cardnumber)
        new_balance = current_balance + deposit_amount
        self.update_balance(self.cardnumber, new_balance)
        self.balance_var.set(f"{new_balance:.2f}")
        self.clear_dynamic_frame()

        transaction_label = tk.Label(
            self.dynamic_frame,
            text="Deposit Complete."
                 "\n\nThank you!",
            bg=bg_color,
            fg=label_color,
            font=(label_font, title_font_size, 'bold'),
        )
        transaction_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    def perform_qr_cash(self):
        self.clear_dynamic_frame()
        transaction_label = tk.Label(
            self.dynamic_frame,
            text="Transaction Completed.\n"
                 "Please Collect the Cash"
                 "\n\nThank you!",
            bg=bg_color,
            fg=label_color,
            font=(label_font, title_font_size, 'bold'),
        )
        transaction_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    def perform_transfer(self):
        self.clear_dynamic_frame()
        transaction_label = tk.Label(
            self.dynamic_frame,
            text="Transaction Completed."
                 "\n\nThank you!",
            bg=bg_color,
            fg=label_color,
            font=(label_font, title_font_size, 'bold'),
        )
        transaction_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    def perform_mini_statement(self):
        self.clear_dynamic_frame()
        mini_statement_label = tk.Label(
            self.dynamic_frame,
            text="Mini Statement Generated Successfully"
                 "\nCollect the Receipt"
                 "\n\nThank you!",
            bg=bg_color,
            fg=label_color,
            font=(label_font, title_font_size, 'bold'),
        )
        mini_statement_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    def perform_change_pin(self):
        self.clear_dynamic_frame()
        transaction_label = tk.Label(
            self.dynamic_frame,
            text="PIN Changed Successfully."
                 "\n\nThank you!",
            bg=bg_color,
            fg=label_color,
            font=(label_font, title_font_size, 'bold'),
        )
        transaction_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    def logout(self):
        self.cursor.close()
        self.connection.close()
        self.root.quit()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainForm(root)
    root.mainloop()
