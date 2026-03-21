
# -Activity 1
# create list
evens = [i for i in range(2, 101, 2)]
print("evens list:", evens)


# -Activity 2
# initialize list of stings
strings = ["   hello  ", "whitespace      ", "   :)  "]

# list comprehension to remove whitespace
new_list = [string.strip() for string in strings]
print(new_list)


# -Activity 3
# get user input
name = input("Enter your name: ")
name = name.upper()
print("Welcome", name, "!")


# -Activity 4
#set up sentence
sentence = "dude, I just biked down that mountain \
and at first I was like Whoa and then I was like Whoa"
print(sentence)
sentence = sentence.capitalize()

# split words on the spaces
words = sentence.split(" ")

first_whoa = True # set up a variable to track how many times we've seen whoa
i = 0
for word in words:
    if words[i] == "whoa" and first_whoa:
        words[i] = words[i].lower()
        first_whoa = False # set tracker to false
    elif words[i] == "whoa" and not first_whoa:
        words[i] = words[i].upper()
    else:
        pass
    i += 1

# output new sentence
new_sentence = ""
for word in words:
    new_sentence += " " + word

print(new_sentence)
