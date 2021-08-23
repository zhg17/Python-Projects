import random


def main():
    users = {}
    print("Enter the number of friends joining (including you):")
    num = int(input())
    if num <= 0:
        print("No one is joining for the party")
    else:
        print("Enter the name of every friend (including you), each on a new line:")
        for i in range(0, num):
            name = input()
            users[name] = 0
        print("Enter the total bill value:")
        value = int(input())
        value_per_person = value / num
        value_per_person = round(value_per_person, 2)
        print('Do you want to use the "Who is lucky?" feature? Write Yes/No:')
        choice = input()
        if choice == "No" or choice == "no":
            for ele in users:
                users[ele] = value_per_person
            print("No one is going to be lucky")
            print(users)
        elif choice == "Yes" or choice == "yes":
            entry_list = list(users.items())
            random_entry = random.choice(entry_list)
            print("{} is the lucky one!".format(random_entry[0]))
            new_per_person = value / (num - 1)
            for ele in users:
                users[ele] = new_per_person
            users[random_entry[0]] = 0
            print(users)


main()
