import pytest
from unittest import mock
from system import System

@pytest.fixture #creates instance of System and calls Main Menu
def system_instance():
  s1 = System()
  s1.initMenu()
  return s1

@pytest.fixture #removes existing accounts from db while testing
def temp_remove_accounts(system_instance): 
  system_instance.cursor.execute("SELECT * FROM accounts")
  saved_accounts = system_instance.cursor.fetchall()
  if len(saved_accounts) > 0:
    system_instance.cursor.execute("DELETE FROM accounts")
    system_instance.conn.commit()
  yield
  system_instance.cursor.execute("DELETE FROM accounts")
  if len(saved_accounts) > 0:
    system_instance.cursor.executemany(
      "INSERT INTO accounts (username, password, fName, lName) VALUES (?, ?, ?, ?)",
      saved_accounts)
  system_instance.conn.commit()

@pytest.fixture
#test that user can input first and last name when registering
def name_register(system_instance, temp_remove_accounts, capsys):
  # username = "test"
  # fName = "unit"
  # lName = "tests"
  # password = "Testing2$"
  # passwordCheck = "Testing2$"
  inputs = ['2', 'tester', 'unit', 'tests', 'Testing3!', 'Testing3!', 'tester', 'Testing3!', '0', '0']
  with mock.patch('builtins.input', side_effect=inputs):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  assert output[21] == 'Account created successfully.'#22nd line of ouput from the program should be Account created successfully
  yield

#@pytest.fixture#test that user can input first and last name when registering
def test_register(system_instance, capsys, temp_remove_accounts):
  inputs = ['2', 'tester', 'unit', 'tests', 'Testing3!', 'Testing3!', 'tester', 'Testing3!', '0', '0']
  with mock.patch('builtins.input', side_effect=inputs):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  assert output[16] == 'Enter Username: '
  assert output[17] == 'Enter First Name: '
  assert output[18] == 'Enter Last Name: '
  assert output[19] == 'Enter Password: '
  assert output[20] == 'Confirm Password: '
  assert output[21] == 'Account created successfully.'

def test_login(system_instance, capsys, name_register):
  inputs = ['1', 'tester', 'Testing3!', '1', '0', '2', '0', '3', '0', '0', '0']
  with mock.patch('builtins.input', side_effect=inputs):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  assert output[16] == 'Log In:'
  assert output[18] == 'Enter Username: '
  assert output[19] == 'Enter Password: '
  assert output[20] == 'You Have Successfully Logged In!'
  assert output[21] == 'Welcome User!'
  assert output[22] == '[1] Job/Internship Search'
  assert output[23] == '[2] Find A Friend'
  assert output[24] == '[3] Learn A Skill'
  assert output[25] == '[0] Log Out'
  assert output[26] == 'Welcome to the Job Postings Page'
  assert output[27] == '[1] Post Job'
  assert output[28] == '[0] Return To Main Menu'
  assert output[30] == 'Welcome User!'
  assert output[31] == '[1] Job/Internship Search'
  assert output[32] == '[2] Find A Friend'
  assert output[33] == '[3] Learn A Skill'
  assert output[34] == '[0] Log Out'
  assert output[36] == '[0] Exit'
  assert output[38] == 'Welcome User!'
  assert output[39] == '[1] Job/Internship Search'
  assert output[40] == '[2] Find A Friend'
  assert output[41] == '[3] Learn A Skill'
  assert output[42] == '[0] Log Out'
  assert output[43] == 'Please Select a Skill:'
  assert output[44] == '[1] Project Management'
  assert output[45] == '[2] Networking'
  assert output[46] == '[3] System Design'
  assert output[47] == '[4] Coding'
  assert output[48] == '[5] Professional Communication'
  assert output[49] == '[0] Return To Main Menu'

def test_findpeople(system_instance, capsys, name_register):
  inputs = ['3', 'unit', 'tests', '0', '0']
  with mock.patch('builtins.input', side_effect=inputs):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  assert output[16] == 'Enter First Name: '
  assert output[17] == 'Enter Last Name: '
  assert output[18] == 'They Are Part Of The InCollege System.'
  assert output[19] == 'Would You Like To Join Your Friends On InCollege?'
  assert output[20] == '[1] Login'
  assert output[21] == '[2] Register'
  assert output[22] == '[0] Return To Home Page'

def test_success_video(system_instance, capsys):
  inputs = ['4', '0', '0']
  with mock.patch('builtins.input', side_effect=inputs):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  assert output[16] == 'See Our Success Story:'
  assert output[17] == '(Playing Video)'
  assert output[19] == '[0] Exit'