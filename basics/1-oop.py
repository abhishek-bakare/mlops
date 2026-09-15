# class, object and methods
class Employee:
    # init is special method called constructor or its called as magic method/dunder
    def __init__(self, name, id, dep, salary):
        self.name = name
        self.id = id
        self.dep = dep
        self.salary = salary

    def travel(self, destination):
        print("This travel method calls manually")
        print(f"Employee is now travelling to {destination}")

# create an object of the class
sam = Employee("Abhishek","123","DevOps","5L")

print(sam.salary,sam.id)

# calling a method
sam.travel("Mumbai")

# creating new attribute from outside
sam.sex = "Male"
print(sam.sex)
