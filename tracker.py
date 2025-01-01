import json
from datetime import datetime

DATA_FILE = "data.json"

# Load or initialize data
def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return an empty list if file doesn't exist or contains invalid JSON
        return []

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Add a new transaction
def add_transaction(data):
    amount = float(input("Enter amount: "))
    description = input("Enter description: ")
    category = input("Enter category: ")
    date = input("Enter date (YYYY-MM-DD) or leave blank for today: ") or datetime.today().strftime('%Y-%m-%d')

    transaction = {
        "amount": amount,
        "description": description,
        "category": category,
        "date": date
    }
    data.append(transaction)
    save_data(data)
    print("Transaction added!")

# View all transactions
def view_transactions(data):
    if not data:
        print("\nNo transactions found.")
        return
    print("\nTransactions:")
    for idx, transaction in enumerate(data, 1):
        print(f"{idx}. {transaction['date']} - {transaction['description']}: ${transaction['amount']} ({transaction['category']})")

# Calculate and display balance
def calculate_balance(data):
    if not data:
        print("\nNo transactions to calculate balance.")
        return
    income = sum(t['amount'] for t in data if t['amount'] > 0)
    expenses = sum(t['amount'] for t in data if t['amount'] < 0)
    print(f"\nIncome: ${income:.2f}")
    print(f"Expenses: ${abs(expenses):.2f}")
    print(f"Net Balance: ${income + expenses:.2f}")

# Clear all transactions
def clear_transactions(data):
    confirm = input("Are you sure you want to clear all transactions? (yes/no): ").strip().lower()
    if confirm == "yes":
        data.clear()  # Clear in-memory data
        save_data(data)  # Overwrite the file with an empty list
        print("All transactions have been cleared!")
    else:
        print("Clear transactions canceled.")

# Delete a specific transaction
def delete_transaction(data):
    if not data:
        print("\nNo transactions to delete.")
        return
    view_transactions(data)
    try:
        index = int(input("\nEnter the number of the transaction to delete: "))
        if 1 <= index <= len(data):
            deleted_transaction = data.pop(index - 1)
            save_data(data)
            print(f"Deleted transaction: {deleted_transaction['description']} on {deleted_transaction['date']}")
        else:
            print("Invalid selection. No transaction deleted.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

# Main menu
def main():
    print("Welcome to the Budget Tracker!")
    data = load_data()
    while True:
        print("\nBudget Tracker")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. View Balance")
        print("4. Clear Transactions")
        print("5. Delete a Transaction")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_transaction(data)
        elif choice == "2":
            view_transactions(data)
        elif choice == "3":
            calculate_balance(data)
        elif choice == "4":
            clear_transactions(data)
        elif choice == "5":
            delete_transaction(data)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
