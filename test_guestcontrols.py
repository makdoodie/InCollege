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

def test_guestnotloggedin(system_instance, temp_remove_accounts, capsys): #tests that guest controls cannot be accessed without being logged in
  input = ['6', '5', '0', '0', '0']
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  assert output[47] == '[0] Exit'

def test_guestloggedin(system_instance, name_register, capsys):  #tests that guest controls can be accessed when a user is logged in
  input = ['1', 'ahmad', 'Asibai1$', '5', '5', '0', '0', '0', '0']
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  assert output[61] == '[1] Guest Controls'

def test_controlsoff(system_instance, name_register, capsys):  #tests that guest controls are all off
  input = ['1', 'ahmad', 'Asibai1$', '5', '5', '1', '1', '2', '3', '0', '0', '0', '0', '0']
  with mock.patch('builtins.input', side_effect=input):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  assert output[73] == '[1] Email [OFF]'
  assert output[81] == '[2] SMS [OFF]'
  assert output[89] == '[3] Targeted Advertising [OFF]'
  username = 'ahmad'
  cursor = system_instance.conn.cursor()
  cursor.execute('Select * From account_settings where username = (?);', (username,))
  result = cursor.fetchone()
  assert type(result) == tuple
  assert result[1] == 0 and result[2] == 0 and result[3] == 0