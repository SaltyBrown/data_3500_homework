
# -Activity 1
# set up colors
message = "My favorite colors are: "
fav_colors = ["blue", "white", "red"]
message += ", ".join(fav_colors)
print(message)


# -Activity 2
# get user input
address = input("Enter your address: ")
address.strip()
address = address.replace(" ", "")
address = address.replace(".", "")
address = address.replace(",", "")
print("address:", address, address.isalnum())
