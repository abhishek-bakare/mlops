# learn to import files

from oop_proj import Chatbook

abhishek = Chatbook()

# fetching the getter
print(abhishek.get_name())
# changing using setter
abhishek.set_name("Agent K")
print(abhishek.get_name())
print("\n")

# testing the staticmethod
user1 = Chatbook() 
print(user1.id)

user2 = Chatbook()
print(user2.id)

user3 = Chatbook()
print(user3.id)