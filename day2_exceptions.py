try:
    age = int(input("Enter your age: "))
    print(f"Next year you will be {age + 1}")
except ValueError:
    print("Please enter a valid number.")
finally:
    print("Program finished.")

raise ValueError("Test error")
print("Will this run?")
