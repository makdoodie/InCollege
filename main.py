from objects import System
from objects import Student
def loginMenu(system):
  loggedOn = False
  print("Welcome to the InCollege login page!\n")
  choice = input("[1] Login [2] Create Account [0] Exit\n")
  while(choice != 0 and loggedOn == False):
    if(choice == "1"):
      username = input("Enter User Name: ")
      password = input("Enter Password: ")
      loggedOn = system.login(username, password)
    elif(choice == "2"):
      username = input("Enter User Name: ")
      password = input("Enter Password: ")
      passwordCheck = input("Confirm Password: ")
      loggedOn = system.register(username, password, passwordCheck)
    print("Incorrect input. Please try again.")
    choice = input("[1] Login [2] Create Account [0] Exit\n")
    
system = System() #creating instance of System
loginMenu(system)   