from objects import System
def loginMenu(system):
  loggedOn = False
  print("Welcome to the InCollege home page!\n")
  choice = input("[1] Login [2] Create Account [0] Exit\n")
  while(choice != "0" and loggedOn == False):
    if(choice == "1"):
      username = input("Enter Username: ")
      password = input("Enter Password: ")
      system.login(username, password)
      loggedOn = True
    elif(choice == "2"):
      username = input("Enter Username: ")
      password = input("Enter Password: ")
      passwordCheck = input("Confirm Password: ")
      system.register(username, password, passwordCheck)
    else:
      print("Incorrect input. Please try again.")
      choice = input("[1] Login [2] Create Account [0] Exit\n")
system = System() #creating instance of System
loginMenu(system)   