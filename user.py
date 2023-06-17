class User:
  ## Not in Use Yet but will hold saved progress and relationships eventually
  ## Probably instantiate in system class and hold logged in status as well
  def __init__(self, userName,fName,lName,loggedOn):
    self.userName = userName
    self.fName = fName
    self.lName = lName
    self.loggedOn = loggedOn
  def login(self,userName,fName,lName):
    self.userName = userName
    self.fName = fName
    self.lName = lName
    self.loggedOn = True
  def logout(self):
    self.userName = "guest"
    self.fName = ""
    self.lName = ""
    self.loggedOn = False