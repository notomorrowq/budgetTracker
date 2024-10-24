import sqlite3

conn  = sqlite3.connect('budget.db')
cursor  = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY,
        date TEXT NOT NULL,
        description TEXT,
        category TEXT,
        amount REAL
        )
    ''')
conn.commit()
print("DATABASE WAS CREATED!")

def add_transaction(date, description, category, amount):
    cursor.execute('''INSERT INTO transactions(date, description, category, amount)
    VALUES(?,?,?,?)
    ''', (date, description, category, amount))
    print("Transaction added successfully!")
    conn.commit()

def view_transactions():
    cursor.execute('SELECT * FROM transactions')
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def update_transaction(transaction_id, date, description, category, amount):
    with conn:
        cursor.execute('''UPDATE transactions
        SET date = ?, description = ?, category = ?, amount = ?
        WHERE id = ?
        ''',(date, description, category, amount, transaction_id))
        print("Transaction updated successfully!")

def delete_transaction(transaction_id):
    with conn:
        cursor.execute('''DELETE FROM transactions WHERE id = ?''', (transaction_id,))
        print("Transaction deleted successfully!")

def view_summary():
    cursor.execute('SELECT SUM(amount) FROM transactions WHERE amount > 0')
    income = cursor.fetchone()[0] or 0

    cursor.execute('SELECT SUM(amount) FROM transactions WHERE amount < 0')
    expences = cursor.fetchone()[0] or 0

    balance = income + expences
    print(f"Total Income: {income}")
    print(f"Total Expenses: {expences}")
    print(f"Balance: {balance}")

def menu():
    while True:
        print("\nPersonal Budget Tracker")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. View Summary")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            date = input("Enter date (YYYY-MM-DD): ")
            description = input("Enter description: ")
            category = input("Enter category: ")
            amount = float(input("Enter amount (negative for expense, positive for income): "))
            add_transaction(date, description, category, amount)
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            transaction_id = int(input("Enter transaction ID to update: "))
            date = input("Enter new date (YYYY-MM-DD): ")
            description = input("Enter new description: ")
            category = input("Enter new category: ")
            amount = float(input("Enter new amount: "))
            update_transaction(transaction_id, date, description, category, amount)
        elif choice == '4':
            transaction_id = int(input("Enter transaction ID to delete: "))
            delete_transaction(transaction_id)
        elif choice == '5':
            view_summary()
        elif choice == '6':
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    menu()