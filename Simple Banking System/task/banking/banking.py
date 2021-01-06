# Write your code here
import sys
import random
import string
import sqlite3


class Database:
    database_file = 'card.s3db'
    code_database_version = 3

    def __init__(self):
        self.conn = sqlite3.connect(Database.database_file)
        current_version = self.get_database_ver()
        if Database.code_database_version > current_version:
            self.update_db(current_version)
            self.update_database_ver(new_version=Database.code_database_version)
            self.conn.commit()
        elif Database.code_database_version < current_version:
            self.downgrade_db(current_version, Database.code_database_version)
            self.update_database_ver(new_version=Database.code_database_version)
            self.conn.commit()

    def get_database_ver(self):
        current_version = self.conn.cursor().execute("PRAGMA user_version")
        return current_version.fetchone()[0]

    def update_database_ver(self, new_version):
        self.conn.cursor().execute("PRAGMA user_version = {v:d}".format(v=new_version))

    def update_db(self, current_version):
        if current_version < 1:
            self.conn.execute("CREATE TABLE card (id INTEGER, number TEXT, pin TEXT, balance INTEGER)")
        if current_version < 2:
            self.conn.executescript("ALTER TABLE card"
                                    " RENAME TO _card;"
                                    " CREATE TABLE card"
                                    " (id      INTEGER,"
                                    " number  TEXT UNIQUE,"
                                    " pin     TEXT,"
                                    " balance INTEGER);"
                                    " INSERT INTO card (number, pin, balance)"
                                    " SELECT number, pin, balance"
                                    " FROM _card;"
                                    " DROP TABLE _card;")
        if current_version < 3:
            self.conn.executescript("ALTER TABLE card"
                                    " rename to _card;"
                                    " CREATE TABLE card"
                                    " ("
                                    "id      INTEGER PRIMARY KEY AUTOINCREMENT,"
                                    " number  TEXT UNIQUE,"
                                    " pin     TEXT,"
                                    " balance INTEGER DEFAULT 0);"
                                    " INSERT INTO card (number, pin, balance)"
                                    " SELECT number, pin, balance"
                                    " FROM _card;"
                                    " DROP TABLE _card;")

    def downgrade_db(self, current_version, target_version):
        if current_version >= 3 > target_version:
            self.conn.executescript("ALTER TABLE card"
                                    " RENAME TO _card;"
                                    " CREATE TABLE card"
                                    " (id      INTEGER,"
                                    " number  TEXT UNIQUE,"
                                    " pin     TEXT,"
                                    " balance INTEGER);"
                                    " INSERT INTO card (number, pin, balance)"
                                    " SELECT number, pin, balance"
                                    " FROM _card;"
                                    " DROP TABLE _card;")
        if current_version >= 2 > target_version:
            self.conn.executescript("ALTER TABLE card"
                                    " RENAME TO _card;"
                                    " CREATE TABLE card"
                                    " (id      INTEGER,"
                                    " number  TEXT,"
                                    " pin     TEXT,"
                                    " balance INTEGER);"
                                    " INSERT INTO card (number, pin, balance)"
                                    " SELECT number, pin, balance"
                                    " FROM _card;"
                                    " DROP TABLE _card;")
        if current_version >= 1 > target_version:
            self.conn.execute("DROP TABLE card ")

    def execute_query(self, query):
        cur = self.conn.execute(query)
        self.conn.commit()
        return cur


class Account:
    database = None

    def __init__(self, card_number, pin, balance=0, account_id=None):
        self.card_number = card_number
        self.pin = pin
        self.balance = balance
        self.account_id = account_id

    @staticmethod
    def generate_card_number():
        account_id = generate_random_number(9)
        account_bin = f"400000{account_id}"
        return f"{account_bin}{Account.generate_luhn_checksum(account_bin)}"

    @staticmethod
    def generate_luhn_checksum(account_bin):
        control_number = Account.generate_control_number(account_bin)
        checksum = 0
        while (control_number + checksum) % 10 != 0:
            checksum += 1
        return checksum

    @staticmethod
    def generate_control_number(account_bin):
        control_number = []
        for index, digit in enumerate(account_bin):
            digit = int(digit)
            if (index + 1) % 2 == 1:
                digit_multiplied_by = digit * 2
                if digit_multiplied_by > 9:
                    digit_multiplied_by -= 9
                control_number.insert(index, digit_multiplied_by)
            else:
                control_number.insert(index, digit)
        return sum(control_number)

    @staticmethod
    def account_already_exists(card_number):
        return Account.get_account_by_card_number(card_number) is not None

    @staticmethod
    def generate_pin():
        return f"{generate_random_number(4)}"

    def print_balance(self):
        print(f"Balance: {self.balance}")

    def is_pin_correct(self, pin):
        return self.pin == pin

    def save_account(self):
        if self.account_id is None:
            self.database.execute_query(
                "INSERT INTO card (number, pin, balance) VALUES ({number:s}, {pin:s}, {balance:d})".format(
                    number=self.card_number, pin=self.pin, balance=self.balance))
        else:
            self.database.execute_query(
                "UPDATE card SET balance = {balance:d} WHERE id = {account_id:d}".format(balance=self.balance,
                                                                                         account_id=self.account_id))

    def close_account(self):
        self.database.execute_query("DELETE FROM card WHERE id = {account_id:d}".format(account_id=self.account_id))

    @staticmethod
    def get_account_by_card_number(card_number):
        cur = Account.database.execute_query(
            "SELECT * FROM card WHERE number = {card_number:s}".format(card_number=card_number))
        data = cur.fetchone()
        if data is None:
            return None
        else:
            return Account(data[1], data[2], data[3], data[0])

    @staticmethod
    def is_card_number_valid(card_number):
        control_number = Account.generate_control_number(card_number[0:len(card_number) - 1])
        luhn_number = card_number[len(card_number) - 1:len(card_number)]
        return (int(control_number) + int(luhn_number)) % 10 == 0

    @staticmethod
    def get_account_by_card_number_and_pin(card_number, pin):
        query = "SELECT * FROM card WHERE number = '{card_number:s}' and pin = '{pin:s}'".format(
            card_number=card_number,
            pin=pin)
        cur = Account.database.execute_query(query)
        data = cur.fetchone()
        if data is None:
            return None
        else:
            return Account(data[1], data[2], data[3], data[0])


database = Database()
Account.database = database


def main_menu():
    main_menu_input = int(input("1. Create an account"
                                "\n2. Log into account"
                                "\n0. Exit\n"))
    if main_menu_input == 0:
        print()
        exit_fn()
    elif main_menu_input == 2:
        account = login()
        if account is not None:
            print("You have successfully logged in!")
            account_menu(account)
        else:
            print("Wrong card number or PIN!")
        print()
    elif main_menu_input == 1:
        account = create_account()
        print_account_data(account)
        print()
    main_menu()


def account_menu(account):
    print()
    account_menu_input = int(input("1. Balance"
                                   "\n2. Add income"
                                   "\n3. Transfer"
                                   "\n4. Close account"
                                   "\n5. Log out"
                                   "\n0. Exit\n"))
    if account_menu_input == 0:
        print()
        exit_fn()
    elif account_menu_input == 5:
        print()
        print("You have successfully logged out!")
        return
    elif account_menu_input == 4:
        print()
        close_account(account)
        return
    elif account_menu_input == 3:
        print()
        do_transfer(account)
    elif account_menu_input == 2:
        print()
        add_income(account)
    elif account_menu_input == 1:
        print()
        account.print_balance()
    account_menu(account)


def print_account_data(account):
    print(f"\nYour card number:\n{account.card_number}\nYour card PIN:\n{account.pin}")


def login():
    print()
    card_number_input = input("Enter your card number:\n")
    pin_number_input = input("Enter your PIN:\n")
    print()
    account = Account.get_account_by_card_number_and_pin(card_number_input, pin_number_input)
    if account is None:
        return None
    return account


def create_account():
    card_number = Account.generate_card_number()
    while Account.account_already_exists(card_number):
        card_number = Account.generate_card_number()
    pin_number = Account.generate_pin()
    account = Account(card_number, pin_number)
    account.save_account()
    return account


def add_income(account):
    income = int(input("Enter income:\n"))
    account.balance += income
    account.save_account()
    print("Income was added!")


def do_transfer(account):
    print("Transfer")
    card_number_2_transfer = input("Enter card number:\n")
    if not Account.is_card_number_valid(card_number_2_transfer):
        print("Probably you made a mistake in the card number. Please try again!")
        return
    if card_number_2_transfer == account.card_number:
        print("You can't transfer money to the same account!")
        return
    account_2_transfer = Account.get_account_by_card_number(card_number_2_transfer)
    if account_2_transfer is None:
        print("Such a card does not exist.")
        return
    money_2_transfer = abs(int(input("Enter how much money you want to transfer:\n")))
    if money_2_transfer > account.balance:
        print("Not enough money!")
        return
    account.balance -= money_2_transfer
    account_2_transfer.balance += money_2_transfer
    account.save_account()
    account_2_transfer.save_account()
    print("Success!")


def close_account(account):
    account.close_account()
    print("The account has been closed!")


def generate_random_number(n_digits):
    return ''.join(random.choices(string.digits, k=n_digits))


def exit_fn():
    print("Bye!")
    sys.exit()


main_menu()
