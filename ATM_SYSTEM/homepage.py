# This is a test file for the Project
import tkinter as tk
from tkinter import messagebox
import mysql.connector


class MainForm:
    def __init__(self, root, cardnumber):
        self.root = root
        self.cardnumber = cardnumber
        self.root.title("Banking Application")

        window_width = 800
        window_height = 600
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
        self.top_frame = tk.Frame(self.root, height=100, bg="blue")
        self.top_frame.pack(fill=tk.X)

        labels = [("Name:", "name_value_label"), ("Balance:", "balance_value_label")]

        for text, label_name in labels:
            label = tk.Label(self.top_frame, text=text, font=('verdana', 10, 'bold'))
            label.pack(side=tk.LEFT)
            setattr(self, label_name, tk.Label(self.top_frame, text="", font=('verdana', 10)))
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
        self.dynamic_frame = tk.Frame(self.root)
        self.dynamic_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.change_content("Initial Content")

    def create_sidebar_frame(self):
        self.sidebar_frame = tk.Frame(self.root, width=150, bg="red")
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        buttons = ["Withdraw", "Deposit", "Transfer", "Mini Statement", "Change PIN", "Logout"]

        for button_text in buttons:
            button = tk.Button(self.sidebar_frame, text=button_text,
                               command=lambda text=button_text: self.change_content(text))
            button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=15)

    def change_content(self, content):
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        if content == "Withdraw":
            self.display_withdraw_content()
        if content == "Deposit":
            self.display_deposit_content()
        elif content == "Transfer":
            self.display_transfer_content()
        elif content == "Mini Statement":
            self.display_mini_statement()
        elif content == "Change PIN":
            self.display_change_pin_content()
        elif content == "Logout":
            self.logout()

    def display_withdraw_content(self):
        title_label = tk.Label(self.dynamic_frame, text="Cash Withdrawal", font=("Verdana", 14, "bold"))
        title_label.pack()

        amount_label = tk.Label(self.dynamic_frame, text="Amount:")
        amount_label.pack()

        self.amount_entry = tk.Entry(self.dynamic_frame, font=("Verdana", 12))
        self.amount_entry.pack()

        withdraw_button = tk.Button(self.dynamic_frame, text="Withdraw", command=self.perform_withdraw)
        withdraw_button.pack()

    def display_deposit_content(self):
        title_label = tk.Label(self.dynamic_frame, text="Cash Deposit", font=("Verdana", 14, "bold"))
        title_label.pack()

        deposit_amount_label = tk.Label(self.dynamic_frame, text="Amount:")
        deposit_amount_label.pack()

        self.deposit_amount_entry = tk.Entry(self.dynamic_frame, font=("Verdana", 12))
        self.deposit_amount_entry.pack()

        deposit_button = tk.Button(self.dynamic_frame, text="Deposit", command=self.perform_deposit)
        deposit_button.pack()

    def display_transfer_content(self):
        title_label = tk.Label(self.dynamic_frame, text="Money Transfer", font=("Verdana", 14, "bold"))
        title_label.pack()

        labels = [("Receiver Account Details", None), ("Enter AC No:", "enter_ac_entry"),
                  ("Re-Enter AC No:", "re_enter_ac_entry"), ("Amount:", "amount_entry")]

        for text, entry_name in labels:
            label = tk.Label(self.dynamic_frame, text=text)
            label.pack()

            if entry_name:
                entry = tk.Entry(self.dynamic_frame, font=("Verdana", 12))
                entry.pack()
                setattr(self, entry_name, entry)

        transfer_button = tk.Button(self.dynamic_frame, text="Transfer", command=self.perform_transfer)
        transfer_button.pack()

    def display_mini_statement(self):
        title_label = tk.Label(self.dynamic_frame, text="Select Account Type", font=("Verdana", 14, "bold"))
        title_label.pack()

        account_types = ["KCC", "Current", "Savings"]

        for account_type in account_types:
            button = tk.Button(self.dynamic_frame, text=account_type,
                               command=lambda text=account_type: self.show_statement(text))
            button.pack()

    def display_change_pin_content(self):
        title_label = tk.Label(self.dynamic_frame, text="Change Your PIN", font=("Verdana", 14, "bold"))
        title_label.pack()

        labels = [("Enter Old PIN:", "old_pin_entry"), ("Enter New PIN:", "new_pin_entry"),
                  ("Re-Enter New PIN:", "re_enter_new_pin_entry")]

        for text, entry_name in labels:
            label = tk.Label(self.dynamic_frame, text=text)
            label.pack()

            entry = tk.Entry(self.dynamic_frame, font=("Verdana", 12))
            entry.pack()
            setattr(self, entry_name, entry)

        change_pin_button = tk.Button(self.dynamic_frame, text="Change PIN", command=self.perform_change_pin)
        change_pin_button.pack()

    def show_statement(self, account_type):
        statement_label = tk.Label(self.dynamic_frame, text=f"Mini Statement for {account_type}")
        statement_label.pack()

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
            transaction_label = tk.Label(self.dynamic_frame, text="Transaction Complete. Please Collect the Cash",
                                         font=("Verdana", 14, "bold"))
            transaction_label.pack()
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

        # Deposit the amount by adding it to the current balance
        new_balance = current_balance + deposit_amount
        self.update_balance(self.cardnumber, new_balance)
        self.balance_var.set(f"{new_balance:.2f}")

        self.clear_dynamic_frame()
        transaction_label = tk.Label(self.dynamic_frame, text="Deposit Complete. Thank you!",
                                     font=("Verdana", 14, "bold"))
        transaction_label.pack()

    def perform_transfer(self):
        receiver_ac_no = self.enter_ac_entry.get()
        re_entered_ac_no = self.re_enter_ac_entry.get()
        transfer_amount = self.amount_entry.get()

    def perform_change_pin(self):
        old_pin = self.old_pin_entry.get()
        new_pin = self.new_pin_entry.get()
        re_entered_new_pin = self.re_enter_new_pin_entry.get()

    def logout(self):
        self.cursor.close()
        self.connection.close()
        self.root.quit()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainForm(root)
    root.mainloop()
