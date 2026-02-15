class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

user1 = User("Sai", 25)

print(user1.name)
print(user1.age)

class User:
    def __init__(self, name, age):
        self.names = name
        self.ages = age

    def greet(self):
        return f"Hello, my name is {self.names}"
    
    def __str__(self):
        return f"User(name={self.names}, age={self.ages})"
    
    # def __repr__(self):
    #     return f"User(name={self.names}, age={self.ages})"
    
user1 = User("Sai", 25)
print(user1.names)
print(user1.ages)


print(user1)  

print(user1.greet())
