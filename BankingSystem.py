import os
import struct

ACCOUNT_FILE = 'account.dat'
ACCOUNT_STRUCT_FORMAT = '50sif'  # Corresponds to (name, acc_no, balance)

class Account:
    def __init__(self, name, acc_no, balance=0.0):
        self.name = name
        self.acc_no = acc_no
        self.balance = balance

    def __repr__(self):
        return f"Account(name={self.name}, acc_no={self.acc_no}, balance={self.balance})"

    def serialize(self):
        name_bytes = self.name.encode('utf-8')
        name_bytes = name_bytes[:50] + b'\x00' * (50 - len(name_bytes))
        return struct.pack(ACCOUNT_STRUCT_FORMAT, name_bytes, self.acc_no, self.balance)

    @staticmethod
    def deserialize(data):
        name, acc_no, balance = struct.unpack(ACCOUNT_STRUCT_FORMAT, data)
        name = name.decode('utf-8').rstrip('\x00')
        return Account(name, acc_no, balance)

def create_account():
    name = input("Enter your name: ").strip()
    acc_no = int(input("Enter your account number: "))
    new_account = Account(name, acc_no)

    with open(ACCOUNT_FILE, 'ab') as file:
        file.write(new_account.serialize())

    print("\nAccount created successfully!")

def deposit_money():
    acc_no = int(input("Enter your account number: "))
    amount = float(input("Enter amount to deposit: "))

    accounts = read_all_accounts()
    for account in accounts:
        if account.acc_no == acc_no:
            account.balance += amount
            write_all_accounts(accounts)
            print(f"Successfully deposited Rs.{amount:.2f}. New balance is Rs.{account.balance:.2f}")
            return

    print(f"Account number {acc_no} not found.")

def withdraw_money():
    acc_no = int(input("Enter your account number: "))
    amount = float(input("Enter amount to withdraw: "))

    accounts = read_all_accounts()
    for account in accounts:
        if account.acc_no == acc_no:
            if account.balance >= amount:
                account.balance -= amount
                write_all_accounts(accounts)
                print(f"Successfully withdrawn Rs.{amount:.2f}. Remaining balance is Rs.{account.balance:.2f}")
            else:
                print("Insufficient balance!")
            return

    print(f"Account number {acc_no} not found.")

def check_balance():
    acc_no = int(input("Enter your account number: "))

    accounts = read_all_accounts()
    for account in accounts:
        if account.acc_no == acc_no:
            print(f"\nYour current balance is Rs.{account.balance:.2f}")
            return

    print(f"\nAccount number {acc_no} not found.")

def read_all_accounts():
    accounts = []
    if os.path.exists(ACCOUNT_FILE):
        with open(ACCOUNT_FILE, 'rb') as file:
            while True:
                data = file.read(struct.calcsize(ACCOUNT_STRUCT_FORMAT))
                if not data:
                    break
                accounts.append(Account.deserialize(data))
    return accounts

def write_all_accounts(accounts):
    with open(ACCOUNT_FILE, 'wb') as file:
        for account in accounts:
            file.write(account.serialize())

def main():
    while True:
        print("\n\n*** Bank Management System ***")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            create_account()
        elif choice == 2:
            deposit_money()
        elif choice == 3:
            withdraw_money()
        elif choice == 4:
            check_balance()
        elif choice == 5:
            print("\nClosing the Bank, Thanks for your visit.")
            break
        else:
            print("\nInvalid choice!")

if __name__ == "__main__":
    main()
