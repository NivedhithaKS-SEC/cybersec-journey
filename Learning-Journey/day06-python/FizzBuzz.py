# Day 3 - Python Loops + FizzBuzz
# Author: Nivedhitha KS
# GitHub: github.com/NivedhithaKS-SEC/cybersec-journey

# FizzBuzz using for loop
print("=== FizzBuzz (1-100) ===")

for i in range(1, 101):
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")   # Check BOTH first — order matters!
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)