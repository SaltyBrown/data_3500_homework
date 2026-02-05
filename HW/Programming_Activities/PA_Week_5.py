


# -Activity 1
#variables
is_palidrome = int(input("Enter a three digit number: "))

first_digit = is_palidrome // 100
third_digit = is_palidrome % 10

#check if palindrome
if first_digit == third_digit:
    print("Palindrome!")
else:
    print("Not palindrome")


# -Activity 2
#variables
num = 2
total = 0

#run loop that sums total
for i in range(1, 1001):
    total += 1/num
    num *= 2
    
print("total:", total)


# -Acvitity 3
#variables and get user input
age = eval(input("Enter child's age: "))
weight = eval(input("Enter child's weight: "))

#result
if age >= 12:
    print("Child can sit in the front seat")
elif age == 11 and weight > 90:
    print("Child can sit in the front seat")
elif age < 11 and weight > 100:
    print("Child can sit in the front seat")
else:
    print("Child cannot sit in the front seat")


