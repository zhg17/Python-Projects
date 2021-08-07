import random
import sqlite3


def generate_checksum(identifier):
    # multiply the odd digits by 2
    identifier_lst = list(map(int, str(identifier)))
    for i, val in enumerate(identifier_lst):
        if i % 2 == 0:
            identifier_lst[i] = identifier_lst[i] * 2
    # subtract 9 from numbers over 9
    for i, val in enumerate(identifier_lst):
        if val > 9:
            identifier_lst[i] = val - 9
    # add all numbers
    sum_of_digits = 0
    for i, val in enumerate(identifier_lst):
        sum_of_digits += val
    checksum = 10 - (sum_of_digits % 10)
    return checksum


class Account:
    IIN = 400000

    def __init__(self):
        sample_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        account_number = str(random.sample(sample_list, 9))
        card_number = '400000' + str(account_number.strip("[]")).replace(',', '').replace(' ', '')
        checksum = generate_checksum(int(card_number))
        # checking if the checksum is only 1 digit, if not, randomly generate the identifier again
        while checksum > 9:
            account_number = str(random.sample(sample_list, 9))
            card_number = '400000' + str(account_number.strip("[]")).replace(',', '').replace(' ', '')
            checksum = generate_checksum(int(card_number))
        self.card_number = card_number + str(checksum)
        self.pin = str(random.sample(sample_list, 4)) \
            .strip("[]").replace(',', '').replace(' ', '')
        self.balance = 0

    def get_card_number(self):
        return self.card_number

    def get_balance(self):
        return self.balance

    def get_pin(self):
        return self.pin


class System:
    def __init__(self):
        self.all_accounts = []
        self.accounts_info = {}
        self.conn = sqlite3.connect('card.s3db')
        self.curr = self.conn.cursor()
        self.curr.execute('''CREATE TABLE IF NOT EXISTS card (
                          id INTEGER,
                          number TEXT NOT NULL,
                          pin TEXT NOT NULL,
                          balance INTEGER DEFAULT 0
                          );
                          ''')
        self.conn.commit()

    def start_system(self):
        while True:
            print("1. Create an account")
            print("2. Log into account")
            print("0. Exit")
            choice = int(input())
            if choice == 1:
                System.create_account(self)
            elif choice == 2:
                card_num = input("Enter your card number:")
                pin = input("Enter your PIN:")
                System.login_account(self, card_num, pin)
            else:
                print('Bye!')
                exit()

    def create_account(self):
        new_account = Account()
        self.curr.execute(
            f"INSERT INTO card(number, pin, balance) VALUES({new_account.get_card_number()}, {new_account.get_pin()}, 0)")
        self.conn.commit()
        print('Your card number:')
        print(new_account.get_card_number())
        print('Your card PIN:')
        print(new_account.get_pin())

    def check_account(self, card_number, pin):
        self.curr.execute('SELECT * FROM card')
        for ele in self.curr.fetchall():
            if ele[1] == card_number:
                if ele[2] == pin:
                    return True
                else:
                    return False

    def login_account(self, card_number, pin):
        successful = System.check_account(self, card_number, pin)
        if not successful:
            print("Wrong card number or PIN!")
        else:
            print("You have successfully logged in!")
            System.logged_in(self, card_number)

    def add_income(self, card_number, income):
        self.curr.execute(f'SELECT * FROM card WHERE number = {card_number}')
        temp = self.curr.fetchall()
        self.curr.execute(f'UPDATE card SET balance = {temp[0][3] + int(income)} WHERE number = {card_number}')
        self.conn.commit()

    def check_checksum(self, card_number):
        checksum = card_number[-1]
        identifier = card_number.rstrip(card_number[-1])
        if generate_checksum(identifier) == checksum:
            return True
        else:
            return False

    def check_receiver(self, card_number):
        self.curr.execute('SELECT * FROM card')
        for ele in self.curr.fetchall():
            if ele[1] == card_number:
                return True
        return False

    def get_balance(self, card_number):
        self.curr.execute(f'SELECT * FROM card WHERE number = {card_number}')
        card = self.curr.fetchall()
        balance = card[0][3]
        return balance

    def subtract_income(self, card_number, amount):
        self.curr.execute(f'SELECT * FROM card WHERE number = {card_number}')
        card = self.curr.fetchall()
        self.curr.execute(f'UPDATE card SET balance = {card[0][3] - amount} WHERE number = {card_number}')
        self.conn.commit()

    def do_transfer(self, sender, receiver):
        if not System.check_checksum(self, receiver):
            print("Probably you made a mistake in the card number. Please try again!")
        if not System.check_receiver(self, receiver):
            print("Such a card does not exist.")
        elif sender == receiver:
            print("You can't transfer money to the same account!")
        else:
            print("Enter how much money you want to transfer:")
            amount = int(input())
            curr_balance = System.get_balance(self, sender)
            if curr_balance < amount:
                print("Not enough money!")
            else:
                System.add_income(self, receiver, amount)
                System.subtract_income(self, sender, amount)
                print("Success!")

    def logged_in(self, card_number):
        while True:
            self.curr.execute(f'SELECT * FROM card WHERE number = {card_number}')
            card = self.curr.fetchall()
            choice = input('1. Balance \n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n')
            if choice == '1':
                print("Balance:", card[0][3])
            elif choice == '2':
                income = int(input('Enter income:'))
                System.add_income(self, card_number, income)
                print("Income was added!")
            elif choice == '3':
                receiver = input('Enter card number:')
                System.do_transfer(self, card_number, receiver)
            elif choice == '4':
                self.curr.execute(f'DELETE FROM card WHERE number = {card_number}')
                self.conn.commit()
                print('The account has been closed!')
                break
            elif choice == '5':
                print('You have successfully logged out!')
                break
            else:
                print('Bye!')
                exit()


system = System()
system.start_system()
