# 2.3
grade = 91;
if grade >= 90:
    {
        print ("Congratulations! Your grade of 91 earns you an A in this course")
    }   

# 2.4
print(27.5 + 2)
print(27.5 - 2)
print(27.5 * 2)
print(27.5 / 2)
print(27.5 // 2)
print(27.5 ** 2)

# 2.5
r = 2
pi = 3.14159
Diameter = 2 * r
Circumference = 2 * pi * r
Area = pi * (r ** 2)
print (" D: " + str(Diameter) + " C: " + str(Circumference) + " A: " + str(Area) + "^2")

# 2.6
num1 = 197
if (num1 % 2) == 0:
    {
        print ("Even!")
    }
if (num1 % 2) > 0:
    {
        print ("Odd!")
    }

# 2.7
if 1024 % 4 == 0:
    {
        print("Multiple of 4")
    }
else:
    {
        print("Not multiple of 4")
    }
if 2 % 10 == 0:
    {
        print("Multiple of 10")
    }
else:
    {
        print("Not multipe of 10")
    }

# 2.8
for i in range(6):
    square = i ** 2
    cube = i ** 3
    print (i, "\t", square, "\t", cube)
