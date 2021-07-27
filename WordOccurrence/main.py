key_word = input()
file = open("data.txt", "r")

data = file.read()
occurrences = data.count(key_word)

print("Number of occurrences of the word {}: {}".format(key_word, occurrences))
