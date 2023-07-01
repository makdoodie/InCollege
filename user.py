class User:
  ## Not in Use Yet but will hold saved progress and relationships eventually
  ## Probably instantiate in system class and hold logged in status as well
  def __init__(self, userName, fName, lName, loggedOn=False, university=None, major=None, profile=None):
    from system import LANGUAGES
    self.userName = userName
    self.fName = fName
    self.lName = lName
    # added university and major fields
    self.university = university
    self.major = major
    self.profile = profile
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
    self.createdProfile = None
  
    
  # check if profile has been created
  def checkProfile(self):
    return self.profile is not None

  def displayProfile(self, mode):
    if mode == "full":
      if self.profile:
        print(f"Name: {self.fName} {self.lName}\nTitle: {self.profile.headline}\nAbout: {self.profile.about}\nUiversity: {self.profile.education.university}\nExperieneces: {self.profile.experiences[0].title}")
    elif mode == "part":
      return f"Name: {self.fName} {self.lName}"

class profile:
  def __init__(self, headline=None, about=None, education=None, experiences=None):
    self.headline = headline
    self.about = about
    self.education = education
    self.experiences = experiences

class experience:
  def __init__(self, ID, title, employer, startDate, endDate, location, description):
    self.ID = ID
    self.title = title
    self.employer = employer
    self.startDate = startDate
    self.endDate = endDate
    self.location = location
    self.description = description

class education:
  def __init__(self, university, major, yearsAttended):
    self.university = university
    self.major = major
    self.yearsAttended = yearsAttended  