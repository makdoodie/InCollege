# Epic 5, Story 6: Edit load process after a user log in
import sqlite3
from user import User
from user import experience
from user import profile
from user import education
import pytest
from unittest import mock
from system import System

@pytest.fixture #creates instance of System and calls Main Menu
def system_instance():
  s1 = System()
  s1.initMenu()
  return s1

# temporarily removes existing accounts from DB when testing
@pytest.fixture
def clear_restore_db(system_instance): 
  """Sets up the database for testing by saving and clearing any persistent records, 
  after a test finishes test records are cleared and saved records are restored."""
  data = {}
  # tables with FKs referencing other tables should come after the referenced table
  tables = ['accounts', 'friends', 'experiences', 'jobs']
  # store each of the tables into a dictionary
  for table in tables:
    system_instance.cursor.execute(f"SELECT * FROM {table}")
    data[table] = system_instance.cursor.fetchall()

  # delete all records from the the accounts table, 
  # and should auto delete all records from tables with FK to accounts
  if len(data[tables[0]]):
    system_instance.cursor.execute("DELETE FROM accounts")
    system_instance.conn.commit()
  # delete all records from the jobs table
  if len(data[tables[-1]]):
    system_instance.cursor.execute("DELETE FROM jobs")
  system_instance.conn.commit()
    
  yield
  # delete any testing records from the database 
  system_instance.cursor.execute("DELETE FROM accounts")
  system_instance.cursor.execute("DELETE FROM jobs")
  # restore saved records to all tables 
  for table in tables:
    if len(data[table]):
      # add a ? to the list of parameters for each column in the table
      parameters = f"({','.join('?' for col in data[table][0])})"
      query = f"INSERT INTO {table} VALUES {parameters}"
      system_instance.cursor.executemany(query, data[table])
  system_instance.conn.commit()

@pytest.fixture #test that user can input first and last name when registering
def name_register(system_instance, clear_restore_db, capsys):
  inputs = ['2', 'ahmad', 'ah', 'mad', 'usf', 'cs', 'Asibai1$', 'Asibai1$', 'ahmad', 'Asibai1$', '0', '0']
  with mock.patch('builtins.input', side_effect=inputs):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out
  assert 'Account created successfully.' in output
  yield

@pytest.fixture #Creates a second account to test with in the database
def name_register_1(system_instance, clear_restore_db, capsys):
  inputs = ['2', 'makdoodie', 'mahmood', 'sales','usf','cs', 'Test123!', 'Test123!', 'makdoodie', 'Test123!', '0', '0']
  with mock.patch('builtins.input', side_effect=inputs):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out
  assert  'Account created successfully.' in output
  
  yield

#Subtask 1: Load year attended (education: INT), title (varchar 50), info (text)) from the accounts table after a user log in
def test_loads_info(system_instance, name_register, capsys):
  #logs in and adds things to profile
  input = ['1', 'ahmad', 'Asibai1$', '1', '1','1', 'Software Engineer Intern', '0', '2', 'Just a bit about me', '0', '3','3','5','0', '0', '0','0', '0', '0']
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  #throwing away output so it doesn't make false positive later
  captured = capsys.readouterr()
  output = captured.out
  #logs in and views profile
  input = ['1', 'ahmad', 'Asibai1$', '1', '2', '0', '0','0', '0', '0']
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  #confirms all data in database is shown when user views profile
  captured = capsys.readouterr()
  output = captured.out
  assert 'Years Attended: 5' in output
  assert 'Software Engineer Intern' in output
  assert 'Just a bit about me' in output

#Subtask 2: Load all experiences (title, employer, date started, date ended, location, and then a description of what they did (text)) from the experience table
def test_load_experiences(system_instance, name_register, capsys):
  #Makes it so the user has a profile and adds an experience
  system_instance.cursor.execute("UPDATE accounts SET profile = True WHERE username='ahmad';")
  system_instance.cursor.execute("INSERT INTO experiences (expID, username, title, employer, dateStarted, dateEnded, location, description) VALUES (1, 'ahmad', 'Software Developer', 'ABC Corp', '2020-01-19', '2020-06-21', 'New York, NY', 'Developed and maintained software for a variety of corporate functions.');")
  #logs in and views profile
  input = ['1', 'ahmad', 'Asibai1$', '1', '2', '0', '0','0', '0', '0']
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  #confirms all data in database is shown when user views profile
  captured = capsys.readouterr()
  output = captured.out
  assert """Title: Software Developer
 Employer: ABC Corp
 Start Date: 2020-01-19
 End Date: 2020-06-21
 Location: New York, NY
 Description: Developed and maintained software for a variety of corporate functions.""" in output

#Subtask 3: Edit loadacceptedfriends to load all profile information
def test_loadacceptedfriends(system_instance, clear_restore_db, capsys, name_register ,name_register_1):
    #adds a friendship between the users
    system_instance.cursor.execute('INSERT INTO friends (sender, receiver, status) VALUES ("ahmad", "makdoodie", "accepted");')
    #inserts profile information for one user
    username = "makdoodie"
    sql = "UPDATE accounts SET yearsAttended=5, title='Software Engineer Intern', infoAbout='Just a bit about me', profile = True WHERE username=?;"
    system_instance.cursor.execute(sql, (username,))
    with mock.patch('builtins.input', side_effect=['ahmad', 'Asibai1$', '0']):
      system_instance.login()
    system_instance.loadAcceptedFriends()
    assert 'makdoodie' in system_instance.user.acceptedRequests
    makdoodie = system_instance.user.acceptedRequests['makdoodie']
    system_instance.loadFriendProfile(makdoodie)
    assert makdoodie.Profile.headline == "Software Engineer Intern"
    assert makdoodie.Profile.about == "Just a bit about me"
    assert makdoodie.Profile.education.yearsAttended == 5