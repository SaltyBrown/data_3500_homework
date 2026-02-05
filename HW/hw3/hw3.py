# 3.4
#loops to create two rows of 7 '@'
for i in range(2):
    for j in range(7):
        print('@', end='')
    print()

# 3.9
#variables
num_str = input("Enter a number 7 to 10 digits: ")
num = int(num_str)

#determine the starting divisor based on number length
divisor = 10 ** (len(num_str) - 1)

# Loop through each digit
while divisor > 0:
    digit = num // divisor
    print(digit)
    num %= divisor
    divisor //= 10

# 3.11
#variables
total_miles = 0
total_gallons = 0

#ask for gallons input
gallons_used = float(input("Enter the gallons used (-1 to end): "))

#ask for miles input
while gallons_used != -1:
    miles_driven = float(input("Enter the miles driven: "))
    
#mpg calculations
    mpg = miles_driven / gallons_used
    print(f"The miles/gallon for this tank was {mpg:.6f}")
    total_miles += miles_driven
    total_gallons += gallons_used
#ask again
    gallons_used = float(input("Enter the gallons used (-1 to end): "))

#overall result
if total_gallons > 0:
    average_mpg = total_miles / total_gallons
    print(f"The overall average miles/gallon was {average_mpg:.6f}")

# 3.12
#variables
value = input("Enter a five-digit number: ")

palindrome = True
length = len(value)

#compare characters from the front and back moving inward
for index in range(length // 2):
    if value[index] != value[length - 1 - index]:
        palindrome = False
        break

#result
if palindrome:
    print("The number is a palindrome.")
else:
    print("The number is not a palindrome.")

# 3.14
#variables
pi_estimate = 0.0
direction = 1

count_314 = 0
count_3141 = 0

#loop that estimates pi and counts how many iterations needed before 3.14 and 3.141 is done twice in a row
for n in range(1, 3001):
    pi_estimate += direction * (4 / (2 * n - 1))
    direction *= -1
    
    pi_rounded_2 = round(pi_estimate, 2)
    pi_rounded_3 = round(pi_estimate, 3)
    
    if pi_rounded_2 == 3.14:
        count_314 += 1
        if count_314 == 2:
            print("3.14 twice in a row at iteration:", n)
    else:
        count_314 = 0
    
    if pi_rounded_3 == 3.141:
        count_3141 += 1
        if count_3141 == 2:
            print("3.141 twice in a row at iteration:", n)
    else:
        count_3141 = 0