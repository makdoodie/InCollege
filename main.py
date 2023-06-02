from system import MenuMediator
from system import System   
from students import Student         
system = System(False) #creating instance of System
system.loginMenu()
print("Accessing Main Menu")
if(system.loggedOn == True):
    print("Welcome to the main page. The mediator is being written")
    system.mainMenu()
else:
  print("Goodbye")