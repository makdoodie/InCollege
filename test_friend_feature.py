#Story 3 As a user, I want to have access to a friend feature in the main menu
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
def temp_remove_accounts(system_instance):
  # save and remove all existing accounts
  system_instance.cursor.execute("SELECT * FROM accounts")
  saved_accounts = system_instance.cursor.fetchall()
  if len(saved_accounts) > 0:
    system_instance.cursor.execute("DELETE FROM accounts")
    system_instance.conn.commit()
  yield
  # remove any test accounts and restore saved accounts
  system_instance.cursor.execute("DELETE FROM accounts")
  if len(saved_accounts) > 0:
    system_instance.cursor.executemany(
      "INSERT INTO accounts (username, password, fName, lName,university,major) VALUES (?, ?, ?, ?,?,?)",
      saved_accounts)
  system_instance.conn.commit()

@pytest.fixture #Creates an account to test with in the database
def name_register(system_instance, temp_remove_accounts, capsys):
  inputs = ['2', 'ahmad', 'ah', 'mad','usf','cs', 'Asibai1$', 'Asibai1$', 'ahmad', 'Asibai1$', '0', '0']
  with mock.patch('builtins.input', side_effect=inputs):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out
  assert  'Account created successfully.' in output
  
  yield

@pytest.fixture #Creates a second account to test with in the database
def name_register_1(system_instance, temp_remove_accounts, capsys):
  inputs = ['2', 'makdoodie', 'mahmood', 'sales','usf','cs', 'Test123!', 'Test123!', 'makdoodie', 'Test123!', '0', '0']
  with mock.patch('builtins.input', side_effect=inputs):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out
  assert  'Account created successfully.' in output
  
  yield

#Subtask 1: To notify the user of pending/received friend requests
#Tests the notification system on the main menu once a user signs in
def test_signup1(system_instance, temp_remove_accounts, capsys, name_register ,name_register_1): 
  input = ['1', 'makdoodie', 'Test123!', '2', '1', '1', 'mad', '1', '1', '0', '0', '0', '0', '0', '0',]
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  input = ['1', 'ahmad', 'Asibai1$', '0', '0']
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out
  assert 'You Have 1 Pending Friend Requests!' in output
  
#Subtask 2: Add a friend’s option to the main menu
#Test the friend's option shows up
def test_freind_option(system_instance, capsys, name_register):
  inputs = ['1', 'ahmad', 'Asibai1$', '0', '0']
  with mock.patch('builtins.input', side_effect=inputs):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out
  assert '[2] Friends' in output

#Subtask 3: Move the find a friend option from the main menu to the friends menu
#Test the friend's option shows up
def test_find_friends_moved(system_instance, capsys, name_register):
  inputs = ['1', 'ahmad', 'Asibai1$', '0', '0']
  with mock.patch('builtins.input', side_effect=inputs):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out
  assert "Find A Friend" not in output

#Test the friend's option shows up
def test_find_friends(system_instance, capsys, name_register):
  inputs = ['1', 'ahmad', 'Asibai1$', '2', '0', '0', '0']
  with mock.patch('builtins.input', side_effect=inputs):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out
  assert "Find A Friend" in output