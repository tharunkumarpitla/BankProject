import mysql.connector
import datetime
from random import randint
from prettytable import PrettyTable

# ----------------------------------------
# DATABASE CLASS (Connection Handling)
# ----------------------------------------
class Database:
    def __init__(self):
        self.config = {
            "host": "localhost",
            "user": "root",
            "password": "database_password",
            "database": "database_name",
        }

    def connect(self):
        return mysql.connector.connect(**self.config)
# ----------------------------------------
# DATABASE
db= Database()
# ----------------------------------------

# ----------------------------------------
# CREATE CUSTOMER_ACCOUNT
# ----------------------------------------
def create_account():
    Account_number=randint(1111111111,9999999999)
    Account_pin=randint(1111,9999)
    name=input('Enter your name: ')
    age=input('Enter your age: ')
    Adhar=int(input('Enter your adhar number: '))
    amount=int(input('Enter your amount: '))
    conn =db.connect()
    cursor =conn.cursor()
    cursor.execute(
        "insert into accounts(account_number,pin,name,age,adhar,amount) values(%s,%s,%s,%s,%s,%s)",
        (Account_number,Account_pin,name,age,Adhar,amount)
    )
    conn.commit()
    cursor.close()
    conn.close()
    print('Account was created sucessfully')
    print(f'Your account number is {Account_number}')
    print(f'Your pin is {Account_pin}')
# ----------------------------------------

# ----------------------------------------
# FIND ACCOUNT IN DATABASE
# ----------------------------------------
def _find_account(cursor, account_number, pin):
    cursor.execute(
        "SELECT * FROM accounts WHERE account_number=%s AND pin=%s",
        (account_number, pin)
    )
    return cursor.fetchone()  # (account_id, account_number, pin, name, age, adhar, amount)
# ----------------------------------------

# ----------------------------------------
#   CUSTOMER DEPOSIT
# ----------------------------------------
def customer_deposit():
    Account_number=int(input('Enter your account number: '))
    Account_pin=int(input('Enter your pin number: '))
    conn =db.connect()
    cursor=conn.cursor()
    account=_find_account(cursor, Account_number,Account_pin)
    if not account:
        print('Account Does not exit')
        cursor.close()
        conn.close()
        return
    try:
        amount=int(input('Enter your amount: '))
    except ValueError and Exception:
        print('Check Your output')
        cursor.close()
        conn.close()
        return
    new_balance=account[6]+amount
    cursor.execute(
        "update accounts set amount=%s where account_number=%s",
        (new_balance,Account_number)
    )
    cursor.execute(
        "insert into transactions(account_number,time,type,amount) values(%s,%s,%s,%s)",
        (Account_number,datetime.datetime.now(),'deposit',amount)
    )
    conn.commit()
    print(f'Account Holder Name=>{account[3]}')
    print(f'Account Holder Amount=>{new_balance}')
    print('Account has been deposited sucessfully')
    cursor.close()
    conn.close()
# ----------------------------------------

# ----------------------------------------
# CUSTOMER WITHDRAW
# ----------------------------------------
def customer_withdraw():
    global count
    Account_number = int(input('Enter your account number: '))
    Account_pin = int(input('Enter your pin number: '))
    conn = db.connect()
    cursor = conn.cursor()
    account = _find_account(cursor, Account_number, Account_pin)
    if not account:
        print('Account Does not exit')
        cursor.close()
        conn.close()
        return

    amount = int(input('Enter your amount: '))
    current_balance = account[6]
    if amount > current_balance:
        print("Insufficient funds")
    else:
        new_balance=current_balance-amount
        cursor.execute(
            "Update accounts set amount=%s where account_number=%s",
            (new_balance,Account_number)
        )
        cursor.execute(
            "insert into transactions(account_number,time,type,amount) values(%s,%s,%s,%s)",
            (Account_number,datetime.datetime.now(),'withdraw',amount)
        )

        conn.commit()
        print(f'Account Holder Name=>{account[3]}')
        print(f'Account Holder Amount=>{new_balance}')
        print('Account has been withdraw successfully')
    cursor.close()
    conn.close()

# ----------------------------------------

# ----------------------------------------
# FIND TOTAL CUSTOMER DETAILS
# ----------------------------------------
def customer_details():
    Account_number = int(input('Enter your account number: '))
    Account_pin = int(input('Enter your pin number: '))
    conn=db.connect()
    cursor=conn.cursor()
    account= _find_account(cursor, Account_number, Account_pin)
    cursor.close()
    conn.close()
    if account:
        print(f'Account Number=>{account[1]}')
        print(f'Account Holder Name=>{account[3]}')
        print(f'Account Holder Age=>{account[4]}')
        print(f'Account Holder Amount=>{account[6]}')
    else:
        print("Account Holder Not Found")
# ----------------------------------------


# ----------------------------------------
#  ACCOUNT STATEMENT
# ----------------------------------------
def  Account_statement():
    Account_number = int(input('Enter your account number: '))
    Account_pin = int(input('Enter your pin number: '))
    conn = db.connect()
    cursor = conn.cursor()
    account = _find_account(cursor, Account_number, Account_pin)
    if not account:
        print('Account Does not exit')
        cursor.close()
        conn.close()
        return
    cursor.execute(
        "select trn_id,time,type,amount from transactions where account_number=%s",
        (Account_number,)
    )
    rows=cursor.fetchall()
    cursor.close()
    conn.close()
    table = PrettyTable(['id', 'datetime', 'trn type', 'amount'])
    for trn in rows:
        table.add_row(trn)
    print(table)

# ----------------------------------------
# MAIN EXECUTION CODE
# ----------------------------------------
def menu():
    print('MENU\n1.create_account\n2.deposit\n3.withdraw\n4.account_details\n5.Account_statement')
    while True:
        choice=int(input('Enter your choice: '))
        match choice:
            case 1:
                create_account()
            case 2:
                customer_deposit()
            case 3:
                customer_withdraw()
            case 4:
                customer_details()
            case 5:
                Account_statement()
            case _:
                print('Invalid choice')
# ----------------------------------------
menu()
# ----------------------------------------
