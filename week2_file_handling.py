with open("users.txt", "w") as file:
    file.write("Sai,26,SE\n")
    file.write("Kumar,30\n")

print("File written successfully.")

with open("users.txt", "r") as file:
    content = file.read()

print(content)

with open("users.txt", "a") as file:
    file.write("Anil,28\n")

print("Appended successfully.")

try:
    with open("unknown.txt", "r") as file:
        print(file.read())
except FileNotFoundError:
    print("File does not exist.")


