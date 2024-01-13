from mongo_connection import MongoDBConnection

class AccountManagement:
    def __init__(self):
        self.connection = MongoDBConnection()
        self.users_collection = self.connection.db['users']

    def add_user(self, user_data):
        self.users_collection.insert_one(user_data)

    def get_Account(self, accountNo):
        return self.users_collection.find_one({'accno': accountNo})
    def delete_user(self, accountNo):
        self.users_collection.delete_one({'accno': accountNo})
        print(f"Account {accountNo} deleted successfully.")


class BankAccount:
    def __init__(self, accountNo):
        self.accountNo = accountNo
        self.obj = AccountManagement()

    def deposit(self, amount):
        if amount > 0:
            user = self.obj.get_Account(self.accountNo)
            new_balance = user['balance'] + amount
            self.obj.users_collection.update_one({'accno': self.accountNo}, {'$set': {'balance': new_balance}})
            print(f"Deposited ${amount}. New balance: ${new_balance}")
        else:
            print("Invalid deposit amount. Please enter a positive value.")

    def withdraw(self, amount):
        user = self.obj.get_Account(self.accountNo)
        if amount > 0 and amount <= user['balance']:
            new_balance = user['balance'] - amount
            self.obj.users_collection.update_one({'accno': self.accountNo}, {'$set': {'balance': new_balance}})
            print(f"Withdrew ${amount}. New balance: ${new_balance}")
        elif amount <= 0:
            print("Invalid withdrawal amount. Please enter a positive value.")
        else:
            print("Insufficient funds for withdrawal.")

    def display_balance(self):
        user = self.obj.get_Account(self.accountNo)
        print(f"Account Holder: {user['name']}")
        print(f"Account Number: {user['accno']}")
        print(f"Current Balance: ${user['balance']}")

def loginTransactions(accountNo):
    obj = BankAccount(accountNo)
    while True:
        print("1: Deposit Amount")
        print("2: Amount Withdrawal")
        print("3: Check Balance")
        print("4: Return back")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            amount = int(input("Enter amount to deposit: "))
            obj.deposit(amount)
        elif choice == 2:
            amount = int(input("Enter amount to withdraw: "))
            obj.withdraw(amount)
        elif choice == 3:
            obj.display_balance()
        elif choice == 4:

            break
        else:
            print("Invalid choice. Please enter a valid option.")

while True:
    print("1. Add Bank account")
    print("2. Login to Bank account")
    print("3. Delete Bank Account")
    print("4. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        obj = AccountManagement()
        name = input("Enter Account holder name: ")
        accountNo = input("Enter Account No: ")
        if obj.get_Account(accountNo):
            print("User already exists...")
            continue
        pin = int(input("Enter pin: "))
        cpin = int(input("Confirm pin: "))
        if pin == cpin:
            user_data = {
                'name': name,
                'accno': accountNo,
                'pin': pin,
                'balance': 0
            }
            try:
                obj.add_user(user_data)
                print("Account Created successfully")
            except Exception as e:
                print(f"Account not created. Error: {e}. Try again.")
    elif choice == 2:
        obj = AccountManagement()
        accountNo = input("Enter Account no: ")
        if obj.get_Account(accountNo):
            pin = int(input("Enter pin: "))
            user = obj.get_Account(accountNo)
            if pin == user["pin"]:
                loginTransactions(accountNo)
            else:
                print("Incorrect Pin..")
        else:
            print("Account Not Found....")
    elif choice == 3:
        obj = AccountManagement()
        accountNo = input("Enter Account no to delete: ")
        if obj.get_Account(accountNo):
            pin = int(input("Enter pin for verification: "))
            user = obj.get_Account(accountNo)
            if pin == user["pin"]:
                obj.delete_user(accountNo)
            else:
                print("Incorrect Pin. Deletion failed.")
        else:
            print("Account Not Found....")
    elif choice == 4:
        print("Exiting..")
        print("Have a great day...")
        break
    else:
        print("Invalid choice. Please enter a valid option.")
