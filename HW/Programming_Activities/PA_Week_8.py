
import numpy as np
# Activity 1
# get input from user
name = input("Enter your name: ")
fav_color = input("Enter your favorite color: ")

# write data to file
with open("example.txt", "w") as file:
    file.write(name + "'s favorite color is " + fav_color + "\n")


# Activity 2
# initialize numpy array
np1 = np.zeros(100)
np1 = np.random.rand(100)
print("np1:", np1)
 