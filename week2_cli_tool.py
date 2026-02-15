import json

def add_user(name, age):
    if not name:
        raise ValueError("Name required")
    if age < 0:
        raise ValueError("Invalid age")

    user = {"name": name, "age": age}

    with open("users.json", "a") as file:
        file.write(json.dumps(user) + "\n")

    print("User saved successfully.")


try:
    name = input("Enter name: ")
    age = int(input("Enter age: "))
    add_user(name, age)

except ValueError as e:
    print("Error:", e)
