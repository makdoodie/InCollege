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

@pytest.fixture#test that user can input first and last name when registering
def test_name_register(system_instance, temp_remove_accounts, capsys):
  # username = "test"
  # fName = "unit"
  # lName = "tests"
  # password = "Testing2$"
  # passwordCheck = "Testing2$"
  inputs = ['2', 'test', 'unit', 'tests', 'Testing2!', 'Testing2!', 'test', 'Testing2!', '0', '0']
  with mock.patch('builtins.input', side_effect=inputs):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out.split('\n')
  assert output[22] == 'Account created successfully.'#22nd line of ouput from the program should be Account created successfully

def test_name_db(system_instance, temp_remove_accounts, test_name_register):
  fName = "unit"
  cursor = system_instance.conn.cursor()
  cursor.execute('Select * From accounts where fName = (?);', (fName,))
  result = cursor.fetchone()
  assert result[2] == 'unit' and result[3] == 'tests' 