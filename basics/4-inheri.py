# simple ex
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f"{self.name} makes a sound.")

# derived class
class Dog(Animal):
    def speak(self):
        print(f"{self.name} barks.")

# create an object
animal = Animal("Generic animal")
animal.speak()

dog = Dog("Buddy")
dog.speak() 