from system import MenuMediator
from system import System   
from user import User        

system = System(False) #creating instance of System
system.loginMenu()
if(system.loggedOn == True):
    print("Welcome to the main page. The mediator is being written")
    system.mainMenu()
else:
  print("Exited from InCollege")