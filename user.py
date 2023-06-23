class User:
  ## Not in Use Yet but will hold saved progress and relationships eventually
  ## Probably instantiate in system class and hold logged in status as well
  def __init__(self, userName, fName, lName, loggedOn=False, university=None, major=None):
    from system import LANGUAGES
    self.userName = userName
    self.fName = fName
    self.lName = lName
    # added university and major fields
    self.university = university
    self.major = major
    self.email = True
    self.sms = True
    self.targetedAds = True
    self.language = LANGUAGES[0]
    # added three dicts for friend request feature 
    # key: username, value: user object
    self.sentRequests = {}
    self.acceptedRequests = {}
    self.receivedRequests = {}
    # loggedOn now false by default
    self.loggedOn = loggedOn
  def login(self, userName, fName, lName, university, major, email, sms, targetedAds, language):
    self.userName = userName
    self.fName = fName
    self.lName = lName
    self.university = university
    self.major = major
    self.email = email
    self.sms = sms
    self.targetedAds = targetedAds
    self.language = language
    self.loggedOn = True
  def logout(self):
    self.userName = "guest"
    self.fName = ""
    self.lName = ""
    self.sentRequests = {}
    self.acceptedRequests = {}
    self.receivedRequests = {}
    self.loggedOn = False
  
    