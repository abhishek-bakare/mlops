# simple ex
class Animal:
    def __init__(self):
        self.name = "Buddy"

    def speak(self):
        print(f"{self.name} makes a sound.")

# derived class
class Dog(Animal):
    def __init__(self, breed):
        super().__init__()          # using this we can access parent class __init__
        self.breed = breed

    def speak(self):
        super().speak()             # using this we can access parent class speak method
        print(f"{self.name} barks. It is a {self.breed}.")

dog = Dog("Golder Retriever")
dog.speak() 