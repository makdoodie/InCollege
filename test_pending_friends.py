#Story 7 As a user I want to be able to manage a friend request send to me by  other users
import pytest
from unittest import mock
from system import System
from user import User

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

#Subask 1: Add a 'pending requests' option to the friends menu that displays the first & last names from the user's received friend list
def test_pending(system_instance, temp_remove_accounts, capsys, name_register ,name_register_1): 
  input = ['1', 'makdoodie', 'Test123!', '2', '1', '1', 'mad', '1', '1', '0', '0', '0', '0', '0', '0',]
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  input = ['1', 'ahmad', 'Asibai1$', '2', '3', '0', '0', '0', '0']
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out
  assert '[3] Pending Requests (1)' in output
  assert '[1] mahmood sales' in output
  
#Subask 2: Clicking on a request should allow the user to view the other users information and accept or reject the request.
def test_accept_choice(system_instance, temp_remove_accounts, capsys, name_register ,name_register_1): 
  input = ['1', 'makdoodie', 'Test123!', '2', '1', '1', 'mad', '1', '1', '0', '0', '0', '0', '0', '0',]
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  input = ['1', 'ahmad', 'Asibai1$', '2', '3', '1', '0', '0', '0', '0', '0']
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  #nakes sure the name, university, and major are displayed
  for line in output[156:161]:
    if "Name" in line:
        found_name = True
    if "University" in line:
        found_uni = True
    if "Major" in line:
        found_major = True
  assert found_name and found_uni and found_major
  #make sure accept and reject options are present
  assert output[164] == '[1] Accept'
  assert output[165] == '[2] Reject'

#Subtask 3: If the user accepts the request, the user object and the friends table should be updated to reflect the accepted friend status.
def test_accepted(system_instance, temp_remove_accounts, capsys, name_register ,name_register_1):
  input = ['1', 'makdoodie', 'Test123!', '2', '1', '1', 'mad', '1', '1', '0', '0', '0', '0', '0', '0',]
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  input = ['1', 'ahmad', 'Asibai1$', '2', '3', '1', '1', '0', '0', '0', '0', '0', '0']
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  sender = "makdoodie"
  receiver = "ahmad" 
  cursor = system_instance.conn.cursor()
  cursor.execute('SELECT * FROM friends WHERE sender = ? AND receiver = ?;', (sender, receiver))
  result = cursor.fetchone()
  assert type(result) == tuple
  assert result[2] == 'accepted'
  with mock.patch('builtins.input', side_effect=['ahmad', 'Asibai1$', '0']):
    system_instance.login()
    system_instance.friend_menu()
  assert len(system_instance.user.receivedRequests) == 0
  assert len(system_instance.user.acceptedRequests) == 1

#Subtask 4: If the user rejects the request, the friend record should be removed from the user class and friends table in the database.
def test_rejected(system_instance, temp_remove_accounts, capsys, name_register ,name_register_1):
  input = ['1', 'makdoodie', 'Test123!', '2', '1', '1', 'mad', '1', '1', '0', '0', '0', '0', '0', '0',]
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  input = ['1', 'ahmad', 'Asibai1$', '2', '3', '1', '2', '0', '0', '0', '0', '0', '0']
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  sender = "makdoodie"
  receiver = "ahmad" 
  cursor = system_instance.conn.cursor()
  cursor.execute('SELECT * FROM friends WHERE sender = ? AND receiver = ?;', (sender, receiver))
  assert cursor.fetchone() is None
  with mock.patch('builtins.input', side_effect=['ahmad', 'Asibai1$', '0']):
    system_instance.login()
    system_instance.friend_menu()
  assert len(system_instance.user.receivedRequests) == 0
  assert len(system_instance.user.acceptedRequests) == 0


#Subtask 5: After an accept/reject, the friend should not appear in 'pending requests'.
def test_pending_gone(system_instance, temp_remove_accounts, capsys, name_register ,name_register_1):
  input = ['1', 'makdoodie', 'Test123!', '2', '1', '1', 'mad', '1', '1', '0', '0', '0', '0', '0', '0',]
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  input = ['1', 'ahmad', 'Asibai1$', '2', '3', '1', '1', '0', '0', '0', '0', '0', '0']
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split("\n")
  #Makes sure the pending requests menu now says 0 
  assert output[177] == 'You Have Received Friend Requests From 0 Users.'
  #Makes sure the user's name is not still in the pending request menu
  request_pending = False
  for line in output[177:181]:
    if "[1] mahmood sales" in line:
        request_pending = True
  # Assert that request_pending is False, indicating no pending request
  assert not request_pending