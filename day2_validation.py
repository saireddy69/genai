import json
def create_user(name, age):
    if not name:
        raise ValueError("Name cannot be empty")

    if age < 0:
        raise ValueError("Age cannot be negative")

    return {
        "name": name,
        "age": age + 1
    }

try:
    user = create_user(str(input("Enter your name: ")), int(input("Enter your age: ")))
    print(user)

    json_data = json.dumps(user)
    print(json_data)
    print(type(json_data))

    parsed = json.loads(json_data)
    print(parsed["name"])
    print(parsed)
    print(type(parsed))

except ValueError as e:
    print("Error:", e)
