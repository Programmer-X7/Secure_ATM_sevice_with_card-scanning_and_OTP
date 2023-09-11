import tkinter as tk
import mysql.connector


class MainForm:
    def __init__(self, root, cardnumber):
        self.root = root
        self.cardnumber = cardnumber
        self.root.title("Banking Application")
        self.root.geometry("800x600")

        self.initialize_database_connection()
        self.create_top_frame()
        self.create_dynamic_frame()
        self.create_sidebar_frame()
        self.load_initial_data()

    def initialize_database_connection(self):
        # Initialize the database connection and cursor
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            port='3306',
            database='sas_bank_db'
        )
        self.cursor = self.connection.cursor()

    def load_initial_data(self):
        # Load the initial name and balance based on the card number
        initial_card_number = self.cardnumber
        initial_data = self.get_data_from_database(initial_card_number)

        if initial_data:
            initial_name, initial_balance = initial_data
            self.name_value_label.config(text=initial_name)
            self.balance_value_label.config(text=initial_balance)
        else:
            self.name_value_label.config(text="Name not found")
            self.balance_value_label.config(text="Balance not found")

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

    def create_top_frame(self):
        # Create the top frame with name and balance labels
        self.top_frame = tk.Frame(self.root, height=100, bg="blue")
        self.top_frame.pack(fill=tk.X)

        labels = [("Name:", "name_value_label"), ("Balance:", "balance_value_label")]

        for text, label_name in labels:
            label = tk.Label(self.top_frame, text=text, font=('verdana', 10, 'bold'))
            label.pack(side=tk.LEFT)
            setattr(self, label_name, tk.Label(self.top_frame, text="", font=('verdana', 10)))
            getattr(self, label_name).pack(side=tk.LEFT)

    def create_dynamic_frame(self):
        # Create the dynamic frame for changing content
        self.dynamic_frame = tk.Frame(self.root)
        self.dynamic_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.change_content("Initial Content")

    def create_sidebar_frame(self):
        # Create the sidebar frame with buttons
        self.sidebar_frame = tk.Frame(self.root, width=150, bg="red")
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        buttons = ["Withdraw", "Transfer", "Mini Statement", "Change PIN", "Logout"]

        for button_text in buttons:
            button = tk.Button(self.sidebar_frame, text=button_text,
                               command=lambda text=button_text: self.change_content(text))
            button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=15)

    def change_content(self, content):
        # Change the content of the dynamic frame
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        if content == "Withdraw":
            # Display Cash Withdrawal content
            self.display_withdraw_content()
        elif content == "Transfer":
            # Display Money Transfer content
            self.display_transfer_content()
        elif content == "Mini Statement":
            # Display Mini Statement content
            self.display_mini_statement()
        elif content == "Change PIN":
            # Display Change PIN content
            self.display_change_pin_content()
        elif content == "Logout":
            # Perform logout
            self.logout()

    def display_withdraw_content(self):
        # Add the content for Cash Withdrawal
        title_label = tk.Label(self.dynamic_frame, text="Cash Withdrawal", font=("Verdana", 14, "bold"))
        title_label.pack()

        amount_label = tk.Label(self.dynamic_frame, text="Amount:")
        amount_label.pack()

        amount_entry = tk.Entry(self.dynamic_frame, font=("Verdana", 12))
        amount_entry.pack()

        withdraw_button = tk.Button(self.dynamic_frame, text="Withdraw", command=self.perform_withdraw)
        withdraw_button.pack()

    def display_transfer_content(self):
        # Add the content for Money Transfer
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
        # Add the content for Mini Statement
        title_label = tk.Label(self.dynamic_frame, text="Select Account Type", font=("Verdana", 14, "bold"))
        title_label.pack()

        account_types = ["KCC", "Current", "Savings"]

        for account_type in account_types:
            button = tk.Button(self.dynamic_frame, text=account_type,
                               command=lambda text=account_type: self.show_statement(text))
            button.pack()

    def display_change_pin_content(self):
        # Add the content for Change PIN
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
        # Display the Mini Statement for the selected account type
        statement_label = tk.Label(self.dynamic_frame, text=f"Mini Statement for {account_type}")
        statement_label.pack()

    def perform_withdraw(self):
        # Add logic for Cash Withdrawal here
        amount = self.amount_entry.get()
        # Implement withdrawal logic

    def perform_transfer(self):
        # Add logic for Money Transfer here
        receiver_ac_no = self.enter_ac_entry.get()
        re_entered_ac_no = self.re_enter_ac_entry.get()
        transfer_amount = self.amount_entry.get()
        # Implement transfer logic

    def perform_change_pin(self):
        # Add logic for changing the PIN here
        old_pin = self.old_pin_entry.get()
        new_pin = self.new_pin_entry.get()
        re_entered_new_pin = self.re_enter_new_pin_entry.get()
        # Implement PIN change logic

    def logout(self):
        # Perform logout actions here (e.g., saving data or cleaning up)
        self.cursor.close()
        self.connection.close()
        self.root.quit()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainForm(root)
    root.mainloop()
