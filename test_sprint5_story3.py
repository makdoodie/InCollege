from test_sprint5 import *
from user import User, experience, education, profile
import inspect
import re

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


def test_basic_has_profile():
  """Checks that boolean hasProfile function of the user class 
  returns true for users with a profile and false for users without one."""
  # setup users with and without a profile and test checkprofile function
  minimal_user = User('user1', 'firstname', 'lastname')
  profile_user = User('user2', 'firstname', 'lastname', Profile=profile())
  assert minimal_user.hasProfile() == False
  assert profile_user.hasProfile() == True


def test_integrated_has_profile(system_instance, clear_restore_db):
  """Checks that user's has profile function operates correctly during a simulated user interaction"""
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
  assert system_instance.user.hasProfile() == False
  # trigger the user profile menu and select to create profile
  inputs = ['1','0','0']
  with mock.patch('builtins.input', side_effect=inputs):
    system_instance.user_profile_menu()
  # check that the user now has a profile
  system_instance.user.hasProfile() == True
  # ensure the profile is cleaned up on logout
  system_instance.user.logout()
  system_instance.user.hasProfile() == False


def test_display_profile():
  """
  Tests the output of the user's display profile function in both partial and full modes.
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
  exp_fields = ['Title', 'Employer', 'Start Date', 'End Date', 'Location', 'Description']
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
  # setup the expected output starting with base fields that will be displayed in every user profile
  # note: the user is not required to enter all of these fields so some may be N/A
  expected_base = {"Viewing Profile",
                    "Education",
                    f"Name: {fName} {lName}",
                    f"Title: {headline}",
                    "Title: N/A",
                    f"About: {about}",
                    "About: N/A",
                    f"University: {uni.title()}",
                    "University: N/A",
                    f"Degree: {major.title()}",
                    "Degree: N/A",
                    f"Years Attended: {years_attended}",
                    "Years Attended: N/A"
}
  # setup the expected experiences output for each of the 3 experiences
  expected_exp = [] # list of 3 sets, 1 for each of the experiences above
  for n, exper in enumerate(experiences, start=1):
    expi = set() # holds output for each attribute of the current experience
    # add the expected output for each attribute to the set
    expi.add(f"Experience {n}")
    i = 0
    expi.add(f"{exp_fields[i]}: {exper.title}")
    i = i + 1
    expi.add(f"{exp_fields[i]}: {exper.employer}")
    i = i + 1
    expi.add(f"{exp_fields[i]}: {exper.startDate}")
    i = i + 1
    expi.add(f"{exp_fields[i]}: {exper.endDate}")
    i = i + 1
    expi.add(f"{exp_fields[i]}: {exper.location}")
    i = i + 1
    expi.add(f"{exp_fields[i]}: {exper.description}")
    expected_exp.append(expi) # append the expected output for the current experience to the list

  # List of users with different profile states ranging from no profile to a full profile.
  # Users are packed in tuples with the number of lines expected to be displayed in full mode for said user.
  # This number refers to the number of lines expected to be matched from the expected_base and
  # expected_exp sets, it does not include formatting lines matched by the regex below.
  users = [(User(username, fName, lName), 2),
           (User(username, fName, lName, Profile=profile()), 4),
           (User(username, fName, lName, Profile=profile(headline)), 4),
           (User(username, fName, lName, Profile=profile(about=about)), 4),
           (User(username, fName, lName, Profile=profile(headline, education=edu)), 8),
           (User(username, fName, lName, Profile=profile(about=about, education=edu)), 8),
           (User(username, fName, lName, Profile=profile(headline, about, edu)), 8),
           (User(username, fName, lName, Profile=profile(headline, about, edu, experiences[0:1])), 15),
           (User(username, fName, lName, Profile=profile(headline, about, edu, experiences[0:2])), 22),
           (User(username, fName, lName, Profile=profile(headline, about, edu, experiences)), 29),]

  # test the outputs of the partial and full profile displays for each user in the list
  for user, num_lines in users:
    # partial profile display should only ever include the first and last name
    assert user.displayProfile('part') == f"Name: {fName} {lName}"
    # output of full profile display depends on the contents of the profile
    result = [line.strip() for line in user.displayProfile('full').split('\n')]
    expected = expected_base
    # union the current user's experiences to the set of expected outputs
    if user.Profile and user.Profile.experiences and len(user.Profile.experiences):
      expected = expected | set.union(*expected_exp[0:len(user.Profile.experiences)])
    # create a dictionary from the set of expected output lines,
    # key: line, value: number of lines matched in result (initially 0)
    expected = dict.fromkeys(expected, 0)
    # Each line of the result should match one of the expected outputs or a formatting line matched by the regex.
    # The regex matches lines that exclusively contain 1 of the following options:
    # no characters, only periods, only whitespaces, only hyphens.
    for line in result:
      if line in expected:
        # expected output lines should only be matched once per result
        expected[line] += 1
        assert line in expected and expected[line] == 1
      else:
        assert re.match(r'^[\.]+$|^[\s]*$|^[-]+$|', line)
    # number of matching lines in result should equal the number of matches expected for the user
    assert sum(expected.values()) == num_lines
  