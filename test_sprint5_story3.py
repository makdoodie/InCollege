from user import *

# Story 3 Classes: User, profile, education, experience ========================================================

def test_profile_class():
  """Confirms that the profile class has the correct attributes."""
  profileObj = profile()
  assert hasattr(profileObj, 'headline')
  assert hasattr(profileObj, 'about')
  assert hasattr(profileObj, 'education')
  assert hasattr(profileObj, 'experiences')

def test_education_class():
  """Confirms that the education class has the correct attributes."""
  eduObj = education('uni', 'major', 'yA')
  assert hasattr(eduObj, 'university')
  assert hasattr(eduObj, 'major')
  assert hasattr(eduObj, 'yearsAttended')

def test_experience_class():
  """Confirms that the experience class has the correct attributes."""
  expObj = experience(1, 'emp', 'title', 'YYYY-MM-DD', 'YYYY-MM-DD', 'loc', 'desc')
  assert hasattr(expObj, 'ID')
  assert hasattr(expObj, 'title')
  assert hasattr(expObj, 'employer')
  assert hasattr(expObj, 'startDate')
  assert hasattr(expObj, 'endDate')
  assert hasattr(expObj, 'location')
  assert hasattr(expObj, 'description')