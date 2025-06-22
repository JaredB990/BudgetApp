import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

class BudgetTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Tracker")
        self.accounts = {}  # Dynamic accounts dictionary

        # Info Display
        self.info_display = tk.Text(root, height=15, width=60, state='disabled')
        self.info_display.pack(pady=10)

        # Button Frame for better layout
        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)

        # Arrange buttons in two columns
        tk.Button(button_frame, text="Add Account", command=self.add_account, width=18).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Add Transaction", command=self.add_transaction, width=18).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="View Transactions", command=self.view_transactions, width=18).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Show Balances", command=self.show_balances, width=18).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Clear All", command=self.clear_all, width=18).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Clear Balances", command=self.clear_balances, width=18).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Load Data", command=self.load_data, width=39).grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        tk.Button(button_frame, text="Save Data", command=self.save_data, width=39).grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        tk.Button(button_frame, text="Exit", command=self.root.quit, width=39).grid(row=5, column=0, columnspan=2, padx=5, pady=10)

        self.load_data()

    def update_info_display(self, text):
        self.info_display.config(state='normal')
        self.info_display.delete(1.0, tk.END)
        self.info_display.insert(tk.END, text)
        self.info_display.config(state='disabled')

    def add_account(self):
        account = simpledialog.askstring(
            "Add Account",
            "Enter new account name:"
        )
        if not account:
            return
        account = account.strip().capitalize()
        if account in self.accounts:
            messagebox.showinfo("Info", f"Account '{account}' already exists.")
            return
        self.accounts[account] = []
        self.update_info_display(f"Account '{account}' added.")
        messagebox.showinfo("Success", f"Account '{account}' has been added.")

    def add_transaction(self):
        account = simpledialog.askstring(
            "Account",
            "Enter account name (e.g., Checking, Savings, Retirement, etc.):"
        )
        if not account:
            return
        account = account.strip().capitalize()
        if account not in self.accounts:
            if not messagebox.askyesno("New Account", f"Account '{account}' does not exist. Create it?"):
                return
            self.accounts[account] = []

        trans_type = simpledialog.askstring(
            "Transaction Type",
            "Enter type: Deposit, Withdrawal, or Expense:"
        )
        if not trans_type or trans_type.lower() not in ["deposit", "withdrawal", "expense"]:
            messagebox.showerror("Error", "Invalid transaction type.")
            return
        trans_type = trans_type.capitalize()

        amount = simpledialog.askfloat("Amount", "Enter the amount:")
        if amount is None:
            return
        description = simpledialog.askstring("Description", "Enter the description:")
        if description is None:
            return

        # Store as (type, amount, description)
        self.accounts[account].append((trans_type, amount, description))
        self.update_info_display(f"Added to {account}: {trans_type} ${amount:.2f} - {description}")
        messagebox.showinfo("Success", f"Transaction added to {account}!")

    def view_transactions(self):
        if not self.accounts:
            self.update_info_display("No accounts or transactions.")
            return
        text = ""
        for account, transactions in self.accounts.items():
            text += f"{account} Transactions:\n"
            if transactions:
                text += "\n".join(
                    f"  {t_type}: ${amount:.2f} - {desc}" for t_type, amount, desc in transactions
                ) + "\n\n"
            else:
                text += "  No transactions.\n\n"
        self.update_info_display(text)

    def show_balances(self):
        if not self.accounts:
            self.update_info_display("No accounts or balances.")
            return
        text = ""
        for account, transactions in self.accounts.items():
            deposits = sum(amount for t_type, amount, _ in transactions if t_type == "Deposit")
            withdrawals = sum(amount for t_type, amount, _ in transactions if t_type == "Withdrawal")
            expenses = sum(amount for t_type, amount, _ in transactions if t_type == "Expense")
            balance = deposits - withdrawals - expenses
            text += (
                f"{account}:\n"
                f"  Deposits: ${deposits:.2f}\n"
                f"  Withdrawals: ${withdrawals:.2f}\n"
                f"  Expenses: ${expenses:.2f}\n"
                f"  Balance: ${balance:.2f}\n\n"
            )
        self.update_info_display(text)

    def clear_all(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all accounts and transactions?"):
            self.accounts.clear()
            self.update_info_display("All accounts and transactions cleared.")
            messagebox.showinfo("Success", "All accounts and transactions cleared.")

    def clear_balances(self):
        if not self.accounts:
            self.update_info_display("No accounts to clear balances.")
            return
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all account balances (transactions will be removed, but accounts will remain)?"):
            for account in self.accounts:
                self.accounts[account] = []
            self.update_info_display("All account balances cleared (accounts remain).")
            messagebox.showinfo("Success", "All account balances cleared.")

    def save_data(self, filename=None):
        if filename is None:
            filename = simpledialog.askstring("Save Data", "Enter filename to save (e.g., john.json):")
            if not filename:
                return
        with open(filename, "w") as f:
            json.dump(self.accounts, f)
        messagebox.showinfo("Saved", f"Data saved successfully as '{filename}'.")

    def load_data(self, filename=None):
        if filename is None:
            filename = simpledialog.askstring("Load Data", "Enter filename to load (e.g., john.json):")
            if not filename:
                self.update_info_display("No filename provided.")
                return
        if os.path.exists(filename):
            with open(filename, "r") as f:
                self.accounts = json.load(f)
            self.update_info_display(f"Data loaded successfully from '{filename}'.")
        else:
            self.update_info_display(f"No saved data found for '{filename}'.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetTracker(root)
    root.mainloop()
