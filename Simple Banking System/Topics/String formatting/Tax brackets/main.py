# Program that prints out the calculated tax amount based on income.
total = int(input())

if total <= 15527:
    print("The tax for {} is {}%. That is {} dollars!".format(total, "0", "0"))
elif total <= 42707:
    calculated = round(total*(15/100))
    print("The tax for {} is {}%. That is {} dollars!".format(total, "15", calculated))
elif total <= 132406:
    calculated = round(total*(25/100))
    print("The tax for {} is {}%. That is {} dollars!".format(total, "25", calculated))
else:
    calculated = round(total*(28/100))
    print("The tax for {} is {}%. That is {} dollars!".format(total, "28", calculated))
