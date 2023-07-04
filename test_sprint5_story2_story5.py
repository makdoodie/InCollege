import sqlite3
from user import User
from user import experience
from user import profile
from user import education
import pytest
from unittest import mock
from system import System
# a list of test users with the attributes necessary for registration

@pytest.fixture
def test_instance_1():
  # Create an instance of the System class or initialize your system
  # delete the value of the table job to do the test 
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM accounts")
    conn.commit()
    conn.close()
    system = System()
    system.initMenu()
    # Perform any necessary setup or data insertion for the test
    # For example, insert test data into the database
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor() 
    cursor.execute("INSERT INTO accounts (username, password, fName, lName,university,major) VALUES (?, ?, ?, ?,?,?)", ('username', "Password123!", "Patrick","Shugerts","USF","CS"))
    conn.commit()
    cursor.execute("INSERT INTO accounts (username, password, fName, lName,university,major) VALUES (?, ?, ?, ?,?,?)", ('username1', "Password123!", "Test","Test","USF","CS"))
    conn.commit()
    cursor.execute("INSERT INTO accounts (username, password, fName, lName,university,major) VALUES (?, ?, ?, ?,?,?)", ('username2', "Password123!", "Testing","Away","USF","CS"))
    conn.commit()
    conn.close()
  ###### Log In a User #####
    system.user.login("username","Patrick","Shugerts","usf","cs",True,True,True,"English")
    # system.user.logout()
    # Return the system instance for the test
    return system
  
def test_profile_title_menu(test_instance_1,capsys):  #tests that signing up is not an option from the general option in useful links to logged in users
  input = ['1', '1','0','0','0']
  with mock.patch('builtins.input', side_effect=input):
    test_instance_1.home_page()
  captured = capsys.readouterr()
  output = captured.out
  assert "[1] Profile" in output
  assert "[1] Create Profile" in output
  assert "[1] Edit Profile" in output
  assert "[2] View Profile" in output
  
def test_profile_title_edit_menu(test_instance_1,capsys):  #tests that signing up is not an option from the general option in useful links to logged in users
  input = ['1', '1', '1', 'This is a Title' ,'0','1','','0','0','0','0']
  with mock.patch('builtins.input', side_effect=input):
    test_instance_1.home_page()
  captured = capsys.readouterr()
  output = captured.out
  assert "Title: This is a Title" in output
  assert "Successfully Added Title to Profile" in output

def test_profile_about_edit_menu(test_instance_1,capsys):  #tests that signing up is not an option from the general option in useful links to logged in users
  input = ['1', '1', '2', 'This is an about section' ,'0','2','','0','0','0','0']
  with mock.patch('builtins.input', side_effect=input):
    test_instance_1.home_page()
  captured = capsys.readouterr()
  output = captured.out
  assert "About: This is an about section" in output
  assert "Successfully Added About to Profile" in output

def test_profile_edu_edit_menu(test_instance_1,capsys):  #tests that signing up is not an option from the general option in useful links to logged in users
  input = ['1', '1', '3','1', 'FSU' ,'0','2','CS','0','3','4','0','0','0','0','0']
  with mock.patch('builtins.input', side_effect=input):
    test_instance_1.home_page()
  captured = capsys.readouterr()
  output = captured.out
  assert "Successfully Added University to Profile" in output
  assert "Successfully Added Degree to Profile" in output
  assert "Successfully Added Years Attended to Profile" in output
  assert "Successfully Added University to Profile" in output 
  
def test_profile_exp1_edit_menu(test_instance_1,capsys):  #tests that signing up is not an option from the general option in useful links to logged in users
  input = ['1', '1', '4','1', 'My first job' ,'0','2','My first employer','0','3','2021-05-27','0','4','2023-05-27','0','5','Somewhere, Florida','0','6','Flipping Burgers','0','0','0','0','0']
  with mock.patch('builtins.input', side_effect=input):
    test_instance_1.home_page()
  captured = capsys.readouterr()
  output = captured.out
  assert "Successfully Added Title to Profile" in output
  assert "Successfully Added Start Date to Profile" in output
  assert "Successfully Added End Date to Profile" in output
  assert "Successfully Added Location to Profile" in output
  assert "Successfully Added Description to Profile" in output 
  
def test_profile_exp2_edit_menu(test_instance_1,capsys):  #tests that signing up is not an option from the general option in useful links to logged in users
  input = ['1', '1', '5','1', 'My second job' ,'0','2','My second employer','0','3','2021-05-27','0','4','2023-05-27','0','5','Somewhere Else, Florida','0','6','Flipping Burgers','0','0','0','0','0']
  with mock.patch('builtins.input', side_effect=input):
    test_instance_1.home_page()
  captured = capsys.readouterr()
  output = captured.out
  assert "Successfully Added Title to Profile" in output
  assert "Successfully Added Start Date to Profile" in output
  assert "Successfully Added End Date to Profile" in output
  assert "Successfully Added Location to Profile" in output
  assert "Successfully Added Description to Profile" in output   

def test_profile_exp3_edit_menu(test_instance_1,capsys):  #tests that signing up is not an option from the general option in useful links to logged in users
  input = ['1', '1', '6','1', 'My third job' ,'0','2','My third employer','0','3','2021-05-27','0','4','2023-05-27','0','5','Somewhere Else Not there, Florida','0','6','Flipping Burgers','0','0','0','0','0']
  with mock.patch('builtins.input', side_effect=input):
    test_instance_1.home_page()
  captured = capsys.readouterr()
  output = captured.out
  assert "Successfully Added Title to Profile" in output
  assert "Successfully Added Start Date to Profile" in output
  assert "Successfully Added End Date to Profile" in output
  assert "Successfully Added Location to Profile" in output
  assert "Successfully Added Description to Profile" in output 

def test_profile_friend_name_menu_name_only(test_instance_1,capsys):  
  #tests that signing up is not an option from the general option in useful links to logged in users
  field = "university"
  value = "USF"
  query = f"""
  SELECT username, fName, lName, university, major FROM accounts WHERE {field} LIKE ? COLLATE NOCASE and username != ?"""
  test_instance_1.cursor.execute(query, (f"%{value}%", test_instance_1.user.userName))
  results = [
    User(uname, fname, lname, university=uni, major=maj) for uname, fname, lname, uni, maj in test_instance_1.cursor.fetchall()
  ]
  for friend in results:
    test_instance_1.sendFriendRequest(friend)
  test_instance_1.user.login("username1","Test","Test","usf","cs",True,True,True,"English")
  test_instance_1.loadAllFriends()
  for uname, friend in test_instance_1.user.receivedRequests.items():
     test_instance_1.acceptFriendRequest(friend)
  test_instance_1.loadAllFriends() 
  test_instance_1.user.login("username","Patrick","Shugerts","usf","cs",True,True,True,"English")
  ################################################################################################
  input = ['3','2','1','0','0','0','0']
  with mock.patch('builtins.input', side_effect=input):
    test_instance_1.home_page()
  captured = capsys.readouterr()
  output = captured.out
  assert "Name: Test Test" in output
 
def test_profile_friend_pending_menu_name_only(test_instance_1,capsys):  
  #tests that signing up is not an option from the general option in useful links to logged in users
  field = "university"
  value = "USF"
  query = f"""
  SELECT username, fName, lName, university, major FROM accounts WHERE {field} LIKE ? COLLATE NOCASE and username != ?"""
  test_instance_1.cursor.execute(query, (f"%{value}%", test_instance_1.user.userName))
  results = [
    User(uname, fname, lname, university=uni, major=maj) for uname, fname, lname, uni, maj in test_instance_1.cursor.fetchall()
  ]
  for friend in results:
    test_instance_1.sendFriendRequest(friend)
  test_instance_1.user.login("username1","Test","Test","usf","cs",True,True,True,"English")
  test_instance_1.loadAllFriends()
  ################################################################################################
  input = ['3','3','1','0','0','0','0','0','0']
  with mock.patch('builtins.input', side_effect=input):
    test_instance_1.home_page()
  captured = capsys.readouterr()
  output = captured.out
  assert "Name: Patrick Shugerts" in output  

def test_view_profile(test_instance_1,capsys):
  test_instance_1.user.login("username","Patrick","Shugerts","usf","cs",True,True,True,"English")
  input = ['1', '1', '1', 'This is a Title' ,'0','1','','0','0','0','0']
  with mock.patch('builtins.input', side_effect=input):
    test_instance_1.home_page()
    test_instance_1.user.login("username","Patrick","Shugerts","usf","cs",True,True,True,"English")
  input = ['1', '1', '2', 'This is an about section' ,'0','2','','0','0','0','0']
  with mock.patch('builtins.input', side_effect=input):
    test_instance_1.home_page()
    test_instance_1.user.login("username","Patrick","Shugerts","usf","cs",True,True,True,"English")
  input = ['1', '1', '3','1', 'FSU' ,'0','2','CS','0','3','4','0','0','0','0','0']
  with mock.patch('builtins.input', side_effect=input):
    test_instance_1.home_page()
  test_instance_1.user.login("username","Patrick","Shugerts","usf","cs",True,True,True,"English")
  input = ['1', '1', '6','1', 'My third job' ,'0','2','My third employer','0','3','2021-05-27','0','4','2023-05-27','0','5','Somewhere Else Not there, Florida','0','6','Flipping Burgers','0','0','0','0','1','2','0','0','0']
  with mock.patch('builtins.input', side_effect=input):
    test_instance_1.home_page()
  captured = capsys.readouterr()
  output = captured.out
  query = """
---------------
Viewing Profile
---------------

Name: Patrick Shugerts
Title: This is a Title
About: This is an about section
"""
  query2 = """
Education
..........

 University: Fsu
 Degree: Cs
 Years Attended: 4
"""
  query3 = """
Experience 1
.............

 Title: My first job
 Employer: My first employer
 Start Date: 2021-05-27
 End Date: 2023-05-27
 Location: Somewhere, Florida
 Description: Flipping Burgers
"""
  query4 = """
Experience 2
.............

 Title: My second job
 Employer: My second employer
 Start Date: 2021-05-27
 End Date: 2023-05-27
 Location: Somewhere Else, Florida
 Description: Flipping Burgers
"""
  query5 = """
Experience 3
.............

 Title: My third job
 Employer: My third employer
 Start Date: 2021-05-27
 End Date: 2023-05-27
 Location: Somewhere Else Not there, Florida
 Description: Flipping Burgers
"""
  assert query in output
  assert query2 in output
  assert query3 in output
  assert query4 in output
  assert query5 in output

def test_view_friend_profile(test_instance_1,capsys):

#tests that signing up is not an option from the general option in useful links to logged in users
  field = "university"
  value = "USF"
  query = f"""
  SELECT username, fName, lName, university, major FROM accounts WHERE {field} LIKE ? COLLATE NOCASE and username != ?"""
  test_instance_1.cursor.execute(query, (f"%{value}%", test_instance_1.user.userName))
  results = [
    User(uname, fname, lname, university=uni, major=maj) for uname, fname, lname, uni, maj in test_instance_1.cursor.fetchall()
  ]
  for friend in results:
    test_instance_1.sendFriendRequest(friend)
  test_instance_1.user.login("username1","Test","Test","usf","cs",True,True,True,"English")
  test_instance_1.loadAllFriends()
  for uname, friend in test_instance_1.user.receivedRequests.items():
     test_instance_1.acceptFriendRequest(friend)
  test_instance_1.loadAllFriends() 
  
  test_instance_1.user.login("username","Patrick","Shugerts","usf","cs",True,True,True,"English")
  input = ['1', '1', '1', 'This is a Title' ,'0','1','','0','0','0','0']
  with mock.patch('builtins.input', side_effect=input):
    test_instance_1.home_page()
    test_instance_1.user.login("username","Patrick","Shugerts","usf","cs",True,True,True,"English")
  input = ['1', '1', '2', 'This is an about section' ,'0','2','','0','0','0','0']
  with mock.patch('builtins.input', side_effect=input):
    test_instance_1.home_page()
    test_instance_1.user.login("username","Patrick","Shugerts","usf","cs",True,True,True,"English")
  input = ['1', '1', '3','1', 'FSU' ,'0','2','CS','0','3','4','0','0','0','0','0']
  with mock.patch('builtins.input', side_effect=input):
    test_instance_1.home_page()
  test_instance_1.user.login("username","Patrick","Shugerts","usf","cs",True,True,True,"English")
  input = ['1', '1', '6','1', 'My third job' ,'0','2','My third employer','0','3','2021-05-27','0','4','2023-05-27','0','5','Somewhere Else Not there, Florida','0','6','Flipping Burgers','0','0','0','0','1','2','0','0','0']
  with mock.patch('builtins.input', side_effect=input):
    test_instance_1.home_page()
    test_instance_1.user.login("username1","Test","Test","usf","cs",True,True,True,"English")
  input = ['3','2','1','1','0','0','0','0','0','0','0']
  with mock.patch('builtins.input', side_effect=input):
    test_instance_1.home_page()
  captured = capsys.readouterr()
  output = captured.out
  query = """
---------------
Viewing Profile
---------------

Name: Patrick Shugerts
Title: This is a Title
About: This is an about section
"""
  query2 = """
Education
..........

 University: Fsu
 Degree: Cs
 Years Attended: 4
"""
  query3 = """
Experience 1
.............

 Title: My first job
 Employer: My first employer
 Start Date: 2021-05-27
 End Date: 2023-05-27
 Location: Somewhere, Florida
 Description: Flipping Burgers
"""
  query4 = """
Experience 2
.............

 Title: My second job
 Employer: My second employer
 Start Date: 2021-05-27
 End Date: 2023-05-27
 Location: Somewhere Else, Florida
 Description: Flipping Burgers
"""
  query5 = """
Experience 3
.............

 Title: My third job
 Employer: My third employer
 Start Date: 2021-05-27
 End Date: 2023-05-27
 Location: Somewhere Else Not there, Florida
 Description: Flipping Burgers
"""
  assert query in output
  assert query2 in output
  assert query3 in output
  assert query4 in output
  assert query5 in output


  