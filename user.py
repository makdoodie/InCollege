class User:
  ## Not in Use Yet but will hold saved progress and relationships eventually
  ## Probably instantiate in system class and hold logged in status as well
  def __init__(self, userName, fName, lName, loggedOn=False, university=None, major=None, Profile=None):
    from system import LANGUAGES
    self.userName = userName
    self.fName = fName
    self.lName = lName
    # added university and major fields
    self.university = university
    self.major = major
    self.Profile = Profile
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
    self.Profile = None
  
    
  # check if profile has been created
  def checkProfile(self):
    return self.Profile is not None

  def displayProfile(self, mode):
    firstName = self.fName.capitalize()
    lastName = self.lName.capitalize()
    if mode == "full":
      headline = self.profile.headline
      about = self.profile.about
      university = self.profile.education.university.title()
      major = self.profile.education.major.title()
      yearsAttended = self.profile.education.yearsAttended
      # experience 1 fields
      exp_title1 = self.profile.experiences[0].title
      exp_employer1 = self.profile.experiences[0].employer
      exp_startDate1 = self.profile.experiences[0].startDate
      exp_endDate1 = self.profile.experiences[0].endDate
      exp_location1 = self.profile.experiences[0].location
      exp_description1 = self.profile.experiences[0].startDate
      # experience 2 fields
      if len(self.profile.experiences) == 2 or len(self.profile.experiences) == 3:
        exp_title2 = self.profile.experiences[1].title
        exp_employer2 = self.profile.experiences[1].employer
        exp_startDate2 = self.profile.experiences[1].startDate
        exp_endDate2 = self.profile.experiences[1].endDate
        exp_location2 = self.profile.experiences[1].location
        exp_description2 = self.profile.experiences[1].startDate
      # experience 3 fields
      if len(self.profile.experiences) == 3:
        exp_title3 = self.profile.experiences[2].title
        exp_employer3 = self.profile.experiences[2].employer
        exp_startDate3 = self.profile.experiences[2].startDate
        exp_endDate3 = self.profile.experiences[2].endDate
        exp_location3 = self.profile.experiences[2].location
        exp_description3 = self.profile.experiences[2].startDate
      if self.Profile:
        if len(self.profile.experiences) == 1:
          return f"--------------------\nViewing Your Profile\n--------------------\n\nName: {firstName} {lastName}\nTitle: {headline if headline else 'N/A'}\nAbout: {about if about else 'N/A'}\n\nEducation\n..........\n\n University: {university}\n Major: {major if major else 'N/A'}\n Years Attended: {yearsAttended if yearsAttended else 'N/A'}\n\nExperience 1\n..............\n\n Title: {exp_title1 if exp_title1 else 'N/A'}\n Employer: {exp_employer1 if exp_employer1 else 'N/A'}\n Start Date: {exp_startDate1 if exp_startDate1 else 'N/A'}\n End Date: {exp_endDate1 if exp_endDate1 else 'N/A'}\n Location: {exp_location1 if exp_location1 else 'N/A'}\n Description: {exp_description1 if exp_description1 else 'N/A'}"
        elif len(self.profile.experiences) == 2:
          return f"--------------------\nViewing Your Profile\n--------------------\n\nName: {firstName} {lastName}\nTitle: {headline if headline else 'N/A'}\nAbout: {about if about else 'N/A'}\n\nEducation\n..........\n\n University: {university}\n Major: {major if major else 'N/A'}\n Years Attended: {yearsAttended if yearsAttended else 'N/A'}\n\nExperience 1\n..............\n\n Title: {exp_title1 if exp_title1 else 'N/A'}\n Employer: {exp_employer1 if exp_employer1 else 'N/A'}\n Start Date: {exp_startDate1 if exp_startDate1 else 'N/A'}\n End Date: {exp_endDate1 if exp_endDate1 else 'N/A'}\n Location: {exp_location1 if exp_location1 else 'N/A'}\n Description: {exp_description1 if exp_description1 else 'N/A'}\n\nExperience 2\n..............\n\n Title: {exp_title2 if exp_title2 else 'N/A'}\n Employer: {exp_employer2 if exp_employer2 else 'N/A'}\n Start Date: {exp_startDate2 if exp_startDate2 else 'N/A'}\n End Date: {exp_endDate2 if exp_endDate2 else 'N/A'}\n Location: {exp_location2 if exp_location2 else 'N/A'}\n Description: {exp_description2 if exp_description2 else 'N/A'}"
        elif len(self.profile.experiences) == 3:
          return f"--------------------\nViewing Your Profile\n--------------------\n\nName: {firstName} {lastName}\nTitle: {headline if headline else 'N/A'}\nAbout: {about if about else 'N/A'}\n\nEducation\n..........\n\n University: {university}\n Major: {major if major else 'N/A'}\n Years Attended: {yearsAttended if yearsAttended else 'N/A'}\n\nExperience 1\n..............\n\n Title: {exp_title1 if exp_title1 else 'N/A'}\n Employer: {exp_employer1 if exp_employer1 else 'N/A'}\n Start Date: {exp_startDate1 if exp_startDate1 else 'N/A'}\n End Date: {exp_endDate1 if exp_endDate1 else 'N/A'}\n Location: {exp_location1 if exp_location1 else 'N/A'}\n Description: {exp_description1 if exp_description1 else 'N/A'}\n\nExperience 2\n..............\n\n Title: {exp_title2 if exp_title2 else 'N/A'}\n Employer: {exp_employer2 if exp_employer2 else 'N/A'}\n Start Date: {exp_startDate2 if exp_startDate2 else 'N/A'}\n End Date: {exp_endDate2 if exp_endDate2 else 'N/A'}\n Location: {exp_location2 if exp_location2 else 'N/A'}\n Description: {exp_description2 if exp_description2 else 'N/A'}\n\nExperience 3\n..............\n\n Title: {exp_title3 if exp_title3 else 'N/A'}\n Employer: {exp_employer3 if exp_employer3 else 'N/A'}\n Start Date: {exp_startDate3 if exp_startDate3 else 'N/A'}\n End Date: {exp_endDate3 if exp_endDate3 else 'N/A'}\n Location: {exp_location3 if exp_location3 else 'N/A'}\n Description: {exp_description3 if exp_description3 else 'N/A'}"
    elif mode == "part":
      return f"Name: {firstName} {lastName}"

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