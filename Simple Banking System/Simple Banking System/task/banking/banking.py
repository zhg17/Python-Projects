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


account = Account()
print(account.get_balance())
print(account.get_card_number())
print(account.get_pin())
