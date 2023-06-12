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

#@pytest.fixture#test that user can input first and last name when registering
def test_register(system_instance, capsys, temp_remove_accounts):
  inputs = ['2', 'tester', 'unit', 'tests', 'Testing3!', 'Testing3!', 'tester', 'Testing3!', '0', '0']
  with mock.patch('builtins.input', side_effect=inputs):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  assert output[17] == 'Enter Username: '
  assert output[18] == 'Enter First Name: '
  assert output[19] == 'Enter Last Name: '
  assert output[20] == 'Enter Password: '
  assert output[21] == 'Confirm Password: '
  assert output[22] == 'Account created successfully.'

def test_login(system_instance, capsys):
  inputs = ['1', 'tester', 'Testing3!', '1', '0', '2', '0', '3', '0', '0', '0']
  with mock.patch('builtins.input', side_effect=inputs):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  assert output[17] == 'Log In:'
  assert output[19] == 'Enter Username: '
  assert output[20] == 'Enter Password: '
  assert output[21] == 'You Have Successfully Logged In!'
  assert output[22] == 'Welcome User!'
  assert output[23] == '[1] Job/Internship Search'
  assert output[24] == '[2] Find A Friend'
  assert output[25] == '[3] Learn A Skill'
  assert output[26] == '[0] Log Out'
  assert output[27] == 'Welcome to the Job Postings Page'
  assert output[28] == '[1] Post Job'
  assert output[29] == '[0] Return To Main Menu'
  assert output[31] == 'Welcome User!'
  assert output[32] == '[1] Job/Internship Search'
  assert output[33] == '[2] Find A Friend'
  assert output[34] == '[3] Learn A Skill'
  assert output[35] == '[0] Log Out'
  assert output[37] == '[0] Exit'
  assert output[39] == 'Welcome User!'
  assert output[40] == '[1] Job/Internship Search'
  assert output[41] == '[2] Find A Friend'
  assert output[42] == '[3] Learn A Skill'
  assert output[43] == '[0] Log Out'
  assert output[44] == 'Please Select a Skill:'
  assert output[45] == '[1] Project Management'
  assert output[46] == '[2] Networking'
  assert output[47] == '[3] System Design'
  assert output[48] == '[4] Coding'
  assert output[49] == '[5] Professional Communication'
  assert output[50] == '[0] Return To Main Menu'

def test_findpeople(system_instance, capsys):
  inputs = ['3', 'unit', 'tests', '0', '0']
  with mock.patch('builtins.input', side_effect=inputs):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  assert output[17] == 'Enter First Name: '
  assert output[18] == 'Enter Last Name: '
  assert output[19] == 'They Are Part Of The InCollege System.'
  assert output[20] == 'Would You Like To Join Your Friends On InCollege?'
  assert output[21] == '[1] Login'
  assert output[22] == '[2] Register'
  assert output[23] == '[0] Return To Home Page'

def test_success_video(system_instance, capsys):
  inputs = ['5', '0', '0']
  with mock.patch('builtins.input', side_effect=inputs):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  assert output[17] == 'See Our Success Story:'
  assert output[18] == '(Playing Video)'
  assert output[20] == '[0] Exit'