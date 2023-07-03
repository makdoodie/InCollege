from test_sprint5 import *
from user import * # imports User, experience, education, and profile classes
import inspect

# a list of test users with the attributes necessary for registration
TEST_USER = [ 
  ['user1', 'hank', 'hill', 'uni1', 'major1', 'Password1!'],
  ['user2', 'bobby', 'hill', 'uni2', 'major2', 'Password2@'],
  ['user3', 'dale', 'gribble', 'uni3', 'major3', 'Password3#'],
  ['user4', 'john', 'redcorn', 'uni4', 'major4', 'Password4$'],
  ['user5', 'khan', 'souphanousinph', 'uni5', 'major5', 'Password5%'],
]

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


def test_user_profile_attr():
  """Checks that the user class contains the new profile attribute, 
  and that the constructor includes a profile parameter that defaults to none"""
  # test the constructor signature for the profile parameter
  profile = 'Profile'
  sig = inspect.signature(User.__init__)
  params = sig.parameters
  assert profile in params and params[profile].default is None
  # test a user instance for the profile attribute 
  minimal_user = User('user1', 'firstname', 'lastname')
  assert hasattr(minimal_user, profile)
  assert minimal_user.Profile is None


def test_basic_check_profile():
  """Checks that boolean checkProfile function of the user class 
  returns true for users with a profile and false for users without one."""
  # setup users with and without a profile and test checkprofile function
  minimal_user = User('user1', 'firstname', 'lastname')
  profile_user = User('user2', 'firstname', 'lastname', Profile=profile())
  assert minimal_user.checkProfile() == False
  assert profile_user.checkProfile() == True


def test_integrated_check_profile(system_instance, clear_restore_db):
  """Checks that user's check profile function operates correctly during a simulated user interaction"""
  # register a user in the system
  inputs = TEST_USER[0]
  inputs.append(TEST_USER[0][-1]) # duplicate password  for pass check input
  with mock.patch('builtins.input', side_effect=inputs):
    system_instance.register()
  # login user
  inputs = [TEST_USER[0][0], TEST_USER[0][-1]]
  with mock.patch('builtins.input', side_effect=inputs):
    system_instance.login()
  # check that new test user does not have profile
  assert system_instance.user.checkProfile() == False
  # trigger the user profile menu and select to create profile
  inputs = ['1','0','0']
  with mock.patch('builtins.input', side_effect=inputs):
    system_instance.user_profile_menu()
  # check that the user now has a profile
  system_instance.user.checkProfile() == True
  # ensure the profile is cleaned up on logout
  system_instance.user.logout()
  system_instance.user.checkProfile() == False


def test_display_profile():
  """
  Tests the output of the user's display profile function in both limited and full modes.
  The test user information used in this function was generated with the assistance of ChatGPT.
  """
  # basic user info
  username, fName, lName = 'user1', 'Emily', 'Johnson'
  # profile info
  headline = "Computer Science Student | University of Cambridge | Passionate about Problem-Solving and Innovation"
  about = """I am Emily Johnson, a passionate computer science student at the University of Cambridge. With a strong interest in problem-solving and innovation, I constantly strive to explore the endless possibilities offered by the world of technology. Throughout my three years at university, I have gained a solid foundation in programming languages, algorithms, and software development methodologies. I am always eager to expand my knowledge and keep up with the latest advancements in the field. My goal is to contribute to the development of cutting-edge solutions that positively impact people's lives and revolutionize the way we interact with technology."""
  # education info
  uni, major, years_attended = 'University of Cambridge', 'Computer Science', 3
  edu = education(uni, major, years_attended)
  # experience 1 info
  experiences = []
  exp = {'id': 1,
          'title': 'Software Engineering Intern',
          'emp': 'XYZ Tech Solutions',
          'start': '2022-06-30',
          'end': '2022-09-01',
          'loc': 'London, United Kingdom',
          'desc': """As a software engineering intern at XYZ Tech Solutions, I collaborated with a team of developers to design and implement new features for a web-based application. I participated in agile development processes, conducted code reviews, and contributed to troubleshooting and debugging tasks. Additionally, I gained hands-on experience in utilizing various programming languages and frameworks, enhancing my skills in software development and problem-solving."""
        }
  experiences.append(experience(exp['id'], exp['title'], exp['emp'], exp['start'], exp['end'], exp['loc'], exp['desc']))
  # experience 2 info
  exp = {'id': 2,
          'title': 'Research Assistant',
          'emp': 'University of Cambridge, Department of Computer Science',
          'start': '2022-01-01',
          'end': '2022-06-01',
          'loc': 'Cambridge, United Kingdom',
          'desc': """During my role as a research assistant at the University of Cambridge, Department of Computer Science, I worked closely with a professor on a project focusing on artificial intelligence and machine learning. I conducted extensive literature reviews, gathered and analyzed data, and assisted in developing algorithms and models. I also collaborated with other team members to prepare research papers for publication, gaining valuable insights into the research process and enhancing my analytical and critical thinking skills."""
        }
  experiences.append(experience(exp['id'], exp['title'], exp['emp'], exp['start'], exp['end'], exp['loc'], exp['desc']))
  # experience 3 info
  exp = {'id': 3,
          'title': 'Software Development Intern',
          'emp': 'ABC Software Solutions',
          'start': '2021-06-01',
          'end': '2021-08-31',
          'loc': 'San Francisco, California, United States',
          'desc': """As a software development intern at ABC Software Solutions, I had the opportunity to work on a cross-functional team to develop and test software applications. I assisted in the implementation of new features, performed software testing and debugging, and collaborated with designers and product managers to ensure smooth functionality and user experience. This experience allowed me to deepen my understanding of the software development lifecycle and refine my coding and problem-solving skills."""
        }
  experiences.append(experience(exp['id'], exp['title'], exp['emp'], exp['start'], exp['end'], exp['loc'], exp['desc']))
  # initialize a complete user profile
  full_profile = profile(headline, about, edu, experiences)
  # test display for a user with no profile
  user = User(username, fName, lName)
  # assert user.displayProfile('part') == f"Name: {fName} {lName}"
  # assert user.displayProfile('full') == f"Name: {fName} {lName}"
  # test display for a user with empty profile
  user = User(username, fName, lName, Profile=profile())
  # assert user.displayProfile('part') == f"Name: {fName} {lName}"
  # assert user.displayProfile('full') == f"Name: {fName} {lName}"
  # test display for a user with complete profile
  user = User(username, fName, lName, Profile=full_profile)
  # assert user.displayProfile('part') == f"Name: {fName} {lName}"
  # assert user.displayProfile('full') == f"Name: {fName} {lName}"
  print(user.displayProfile('full'))

  