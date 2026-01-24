# -Activity 1
#Variable setup
apple_price = 1
number_purchased = 3
tax = 1.07

#Total price calculation
total_bill = apple_price * number_purchased * tax
print("You bought", number_purchased, "apples for", apple_price, "per apple. The total bill was", total_bill, "\n")

# -Activity 2
#Get user input
age = int(input("Please enter your age: "))
live_to = int(input("What age would you like to live to?: "))

# Years left calculation
print("You have", live_to - age, "years left to live.")

# -Activity 3
#Get user input
grade = float(input("Enter your grade as a percentage: "))

#Check if A
if grade >= 93:
    print("Congratulations you got an A")
else:
    print("Congratulations, you still learned a ton!")