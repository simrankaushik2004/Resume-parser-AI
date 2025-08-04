# n=int(input("enter the number : "))
# for i in range(1,11):
#     i=i*n
#     print(i)



import math  # Importing math module for square root calculation

n = int(input("Enter the number: "))

# Printing the multiplication table
print(f"\nMultiplication table of {n}:")
for i in range(1, 11):
    print(f"{n} x {i} = {n * i}")

# Calculating and printing the square root
square_root = math.sqrt(n)
print(f"\nSquare root of {n}: {square_root:.2f}")
