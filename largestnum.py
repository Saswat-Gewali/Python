# Program to find the largest among three numbers

def find_largest(a, b, c):
    if a >= b and a >= c:
        return a
    elif b >= a and b >= c:
        return b
    else:
        return c

# Input from user
num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))
num3 = float(input("Enter the third number: "))

# Find the largest
largest = find_largest(num1, num2, num3)

# Output
print(f"The largest number among {num1}, {num2}, and {num3} is {largest}")
