#Epic 5, Story 4: I want to be able to see the profile of any friend I have.
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

#Subtask 1: In Show my Network, you may click on any connection and have the option to view their profile in addition to the already created disconnect and exit options, this is only an option if the connection has created a profile
def test_friend_profile(system_instance, clear_restore_db, capsys, name_register ,name_register_1):
  #adds a friendship between the users
  system_instance.cursor.execute('INSERT INTO friends (sender, receiver, status) VALUES ("ahmad", "makdoodie", "accepted");')
  #makes sure there's no view profile option
  input = ['1', 'ahmad', 'Asibai1$', '3', '2', '1', '0' '0', '0','0', '0','0']
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out
  assert '[1] View Profile' not in output
  #logs in and adds things to profile
  input = ['1', 'makdoodie', 'Test123!', '1', '1','1', 'placeholder title', '0', '0', '0','0', '0']
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  #now that profile options are added, checks that view profile button is present
  input = ['1', 'ahmad', 'Asibai1$', '3', '2', '1', '0' '0', '0','0', '0', '0']
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out
  assert '[1] View Profile' in output
    
#Subtask 2: Clicking on a connection should not display the user’s profile automatically
def test_display_profile(system_instance, clear_restore_db, capsys, name_register ,name_register_1):
  #adds a friendship between the users
  system_instance.cursor.execute('INSERT INTO friends (sender, receiver, status) VALUES ("ahmad", "makdoodie", "accepted");')
  #logs in and adds things to profile
  input = ['1', 'makdoodie', 'Test123!', '1', '1','1', 'placeholder title', '0', '0', '0','0', '0']
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
    input = ['1', 'ahmad', 'Asibai1$', '3', '2', '1', '0' '0', '0','0', '0', '0']
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out
  assert 'placeholder title' not in output

#Subtask 3: Once view profile is pressed, that connection’s profile will be displayed and so 0 (an exit) will take you back to the previous menu
def test_view_friend(system_instance, clear_restore_db, capsys, name_register ,name_register_1):
  #adds a friendship between the users
  system_instance.cursor.execute('INSERT INTO friends (sender, receiver, status) VALUES ("ahmad", "makdoodie", "accepted");')
  #adds some sample data to the user's profile
  sql = "UPDATE accounts SET yearsAttended=5, title='Software Engineer Intern', infoAbout='Just a bit about me', profile = True WHERE username='makdoodie';"
  system_instance.cursor.execute(sql)
  input = ['1', 'ahmad', 'Asibai1$', '3', '2', '1', '1', '0', '0' '0', '0','0', '0', '0']
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split("\n")
  with open("out.txt", 'w') as f:
    for line in output:
      f.write(f"{line}\n")
  
  assert output[55] == 'Title: Software Engineer Intern'
  assert output[56] == 'About: Just a bit about me'
  assert output[63] == ' Years Attended: 5'
  #Makes sure exit will take you back to the previous menu
  assert output[78] == 'Exiting'