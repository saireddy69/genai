name = "Sai"
age = 25
is_developer = True

print(name)
print(age)
print(is_developer)

skills = ["PHP", "HTML", "CSS"]
print(skills)
print(skills[0])

skills.append("Python")
print(skills)

skills.append('sai')
print(skills)

user = {
    "name": "Sai",
    "role": "Developer",
    "experience": 3
}

print(user["name"])
print(user)

for skill in skills:
    print(skill)

def greet(name):
    return f"Hello {name}"

print(greet("Sai"))

name = input("Enter your name: ")
role = input("Enter your role: ")

user = {
    "name": name,
    "role": role
}

print(f"{user['name']} is a {user['role']}")
