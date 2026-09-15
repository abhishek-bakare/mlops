# lets familiar with class, methods with 1 ex
class Chatbook:

    __user_id = 1       # setting up static variable
    # we are going to increments this id when new user is registered

    def __init__(self):
        self.id = Chatbook.__user_id        # to access static var inside method we need to use class.__vars
        Chatbook.__user_id += 1             # incremented by 1
        self.__name = "Default User"        # way to encapsulate or hide the data using __var
        self.username = ''
        self.password = ''
        self.loggedin = False
        #self.menu()

    # setting up getter
    def get_name(self):
        return self.__name
    # setting up the setter
    def set_name(self, value):
        self.__name = value

    # getter and setter for __user_id
    @staticmethod           # we used this as saying like this is staticmethod
    def get_id():
        return Chatbook.__user_id
    @staticmethod
    def set_id(value):
        Chatbook.__user_id = value


    def menu(self):
        user_input = input("""Welcome to ChatBook...! How would you like to proceed?
                              1. Press 1 to singup
                              2. Press 2 to signin
                              3. Press 3 to write a post
                              4. Press 4 to message a friend
                              5. Press any other key to exit ->""")
        if user_input == "1":
            self.signup()
        elif user_input == "2":
            self.signin()
        elif user_input == "3":
            self.mypost()
        elif user_input == "4":
            self.sendmsg()
        else:
            exit()

    def signup(self):
        email = input("Enter email here -> ")
        pwd = input("Enter pass here -> ")
        self.username = email
        self.password = pwd
        print("Signed up successfully...!")
        print("\n")
        self.menu()   

    def signin(self):
        if self.username == '' and self.password == '':
            print("Pls signup first by pressing 1 in the menu") 
        else:
            uname = input("Enter your email -> ")
            pwd = input("Enter pass here -> ")
            if self.username == uname and self.password == pwd:
                print("Successfully signed in...!")
                self.loggedin = True
            else:
                print("Please input a correct credentials..!")
        print("\n")
        self.menu()

    def mypost(self):
        if self.loggedin == True:
            post = input("Enter your message here -> ")
            print(f"Thank you for posting..! {post}")
        else:
            print("Need to sign in first to post something...!")
        print("\n")
        self.menu()

    def sendmsg(self):
        if self.loggedin == True:
            msg = input("Enter your message to send -> ")
            friend = input("Enter name of friend to send message {msg} -> ")
            print("Meesage sent to {friend}")
        else:
            print("Need to sign in first to sent a message...!")
        print("\n")
        self.menu()

user = Chatbook()

print(user._Chatbook__name)         # to call the hided attribute we can use like this _Classname__varname