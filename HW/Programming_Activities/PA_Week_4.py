
# -Activity 1
#Get user input
year_born = int(input("Enter the year you were born: "))

#Check which generation
if year_born >= 1997:
    print("You are a zoomer!\n")
elif year_born >= 1981:
    print("You are a millenial!\n")
elif year_born >= 1965:
    print("You are gen x!\n")
elif year_born >= 1946:
    print("You are a baby boomer!\n")
else:
    print("I'm not sure which generation you belong to?\n")

# -Activity 2
#Get user input
age = int(input("Enter your age: "))

#Set year
current_year = 2026

#While loop for age
while age >= 1:
    print("You were alive in", current_year)
    current_year -=1
    age -= 1
else:
    current_year -=1
    print("You were born in", current_year, "\n")

# -Acvitity 3
#Set up loop
for i in range(1, 96):
    if i % 5 == 0:
        print(i)

# -Activity 4
#Set up while loop
num = 1

while num < 96:
    if num % 5 == 0:
        print(num)
    num += 1
