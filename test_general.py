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

@pytest.fixture #test that user can input first and last name when registering
def name_register(system_instance, temp_remove_accounts, capsys):
  inputs = ['2', 'ahmad', 'ah', 'mad', 'Asibai1$', 'Asibai1$', 'ahmad', 'Asibai1$', '0', '0']
  with mock.patch('builtins.input', side_effect=inputs):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  assert output[24] == 'Account created successfully.'#22nd line of ouput from the program should be Account created successfully
  yield

def test_loggedin(system_instance, temp_remove_accounts, capsys): #tests that signing up from the general option in useful links can only be accessed when a user is not logged in
  input = ['5', '1', '0', '0', '0']
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  assert output[28] == '[1] Sign Up'

def test_notloggedin(system_instance, name_register, capsys):  #tests that signing up is not an option from the general option in useful links to logged in users
  input = ['1', 'ahmad', 'Asibai1$', '4', '1', '0', '0', '0', '0']
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  assert output[41] == '[1] Help Center'

def test_signup1(system_instance, temp_remove_accounts, capsys): #tests that registering from the signup general option is valid and saves the new users information in the db
  input = ['5', '1', '1', '2', 'ahmad', 'ah', 'mad', 'Asibai1$', 'Asibai1$', 'ahmad', 'Asibai1$', '0', '0', '0', '0', '0']
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  assert output[39] == '[2] Register'
  assert output[41] == 'Enter Username: '
  assert output[42] == 'Enter First Name: '
  assert output[43] == 'Enter Last Name: '
  assert output[44] == 'Enter Password: '
  assert output[45] == 'Confirm Password: '
  assert output[46] == 'Account created successfully.'
  assert output[51] == 'You Have Successfully Logged In!'
  username = "ahmad"
  cursor = system_instance.conn.cursor()
  cursor.execute('Select * From accounts where username = (?);', (username,))
  result = cursor.fetchone()
  assert type(result) == tuple
  assert result[0] == 'ahmad' and result[1] == system_instance.encryption('Asibai1$') and result[2] == 'ah' and result[3] == 'mad'

def test_signup2(system_instance, name_register, capsys): #tests that a registered  user can login from the general signup option
  input = ['5', '1', '1', '1', 'ahmad', 'Asibai1$', '0', '0', '0', '0', '0']
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  assert output[38] == '[1] Login'
  assert output[43] == 'Enter Username: '
  assert output[44] == 'Enter Password: '
  assert output[45] == 'You Have Successfully Logged In!'

def test_helpcenter(system_instance, temp_remove_accounts, capsys): #tests that the help center can be accessed from the general useful links option
  input = ['5', '1', '2', '0', '0', '0', '0']
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  assert output[37] == "We're here to help"

def test_about(system_instance, temp_remove_accounts, capsys): #tests that about can be accessed from the general useful links option
  input = ['5', '1', '3', '0', '0', '0', '0']
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  assert output[37] == "In College: Welcome to In College, the world's largest college student"

def test_press(system_instance, temp_remove_accounts, capsys): #tests that the press can be accessed from the general useful links option
  input = ['5', '1', '4', '0', '0', '0', '0']
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  assert output[37] == 'In College Pressroom: Stay on top of the latest news, updates, and reports'

def test_blog(system_instance, temp_remove_accounts, capsys): #tests that the blog can be accessed from the general useful links option
  input = ['5', '1', '5', '0', '0', '0', '0']
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  assert output[36] == 'Under Construction'
  
def test_careers(system_instance, temp_remove_accounts, capsys): #tests that the careers section can be accessed from the general useful links option
  input = ['5', '1', '6', '0', '0', '0', '0']
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  assert output[36] == 'Under Construction'
  
def test_developers(system_instance, temp_remove_accounts, capsys): #tests that the developers section can be accessed from the general useful links option
  input = ['5', '1', '7', '0', '0', '0', '0']
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  assert output[36] == 'Under Construction'