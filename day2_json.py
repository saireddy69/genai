import json

user = {
    "name": "Sai",
    "role": "Developer",
    "skills": ["PHP", "Python"]
}

json_data = json.dumps(user)
print(json_data)
print(type(json_data))

parsed = json.loads(json_data)
print(parsed["name"])
print(parsed)
print(type(parsed))