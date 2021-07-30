import random


class Account:
    IIN = 400000

    def __init__(self):
        sample_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        account_number = str(random.sample(sample_list, 9))
        checksum = str(random.sample(sample_list, 1))
        self.card_number = '400000' + str(account_number.strip("[]") + checksum.strip("[]")) \
            .replace(',', '').replace(' ', '')
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

    def start_system(self):
        while True:
            print("1. Create an account")
            print("2. Log into account")
            print("0. Exit")
            choice = int(input())
            if choice == 1:
                System.create_account(self)
            elif choice == 2:
                print("Enter your card number:")
                card_num = input()
                print("Enter your PIN:")
                pin = input()
                System.login_account(self, card_num, pin)
            else:
                print('Bye!')
                exit()

    def create_account(self):
        new_account = Account()
        self.all_accounts.append(new_account)
        self.accounts_info[new_account.get_card_number()] = new_account
        print('Your card number:')
        print(new_account.get_card_number())
        print('Your card PIN:')
        print(new_account.get_pin())

    def check_account(self, card_number, pin):
        for ele in self.all_accounts:
            if ele.get_card_number() == card_number:
                if ele.get_pin() == pin:
                    return True
        return False

    def login_account(self, card_number, pin):
        successful = System.check_account(self, card_number, pin)
        if not successful:
            print("Wrong card number or PIN!")
        else:
            print("You have successfully logged in!")
            System.logged_in(self, card_number)

    def logged_in(self, card_number):
        print("1. Balance")
        print("2. Log out")
        print("0. Exit")
        choice = input()
        if choice == 1:
            print("Balance:", self.accounts_info[card_number].get_balance())
        elif choice == 2:
            print('You have successfully logged out!')
            System.start_system(self)
        else:
            print('Bye!')
            exit()


system = System()
system.start_system()
