#Story 2 As a developer I want to modify the database to support expanded user accounts and friend’s lists
import pytest
from unittest import mock
from system import System
import sqlite3

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

@pytest.fixture #Creates an account to test with in the database (modular)
def three_users(system_instance, temp_remove_accounts, capsys):
  inputs1 = ['2', 'ahmad', 'ah', 'mad','usf','cs', 'Asibai1$', 'Asibai1$', 'ahmad', 'Asibai1$', '0', '0']
  inputs2 = ['2', 'makdoodie', 'mahmood', 'sales','usf','cs', 'Test123!', 'Test123!', 'makdoodie', 'Test123!', '0', '0']
  inputs3 = ['2', 'testuser', 'mark', 'smith','usf','cs', 'Test123!', 'Test123!', 'testuser', 'Test123!', '0', '0']
  allInputs = [inputs1, inputs2, inputs3]
  for inputs in allInputs:
    with mock.patch('builtins.input', side_effect=inputs):
      system_instance.home_page()
    captured = capsys.readouterr()
    output = captured.out
    assert  'Account created successfully.' in output  
  yield

#Subask 1: Modify the accounts table to include university and major fields(text)
def test_accounts_table_creation_withFields(system_instance, name_register):
    # Get the column names of the accounts table
    system_instance.cursor.execute("PRAGMA table_info(accounts)")
    columns = system_instance.cursor.fetchall()
    column_names = [column[1] for column in columns]
    # Define the expected column names
    expected_columns = [
        'username', 
        'password', 
        'fName', 
        'lName',
        'university',
        'major'
    ]
    # Assert that the column names match the expected column names
    assert column_names == expected_columns

#Subtask 2: Add a deletion trigger on the account table to remove associated records from an accounts table when an account is deleted

def test_deletion_trigger(system_instance, three_users):
    query = "INSERT OR IGNORE INTO friends (sender, receiver, status) VALUES (?,?,?) RETURNING rowid"
    values = ('makdoodie', 'ahmad', 'pending')
    system_instance.cursor.execute(query, values)
    query = "INSERT OR IGNORE INTO friends (sender, receiver, status) VALUES (?,?,?) RETURNING rowid"
    values = ('ahmad', 'testuser', 'pending')
    system_instance.cursor.execute(query, values)
    system_instance.cursor.execute("SELECT count(*) FROM friends")
    friends_count = system_instance.cursor.fetchone()
    assert friends_count[0] == 2
    system_instance.cursor.execute("DELETE FROM accounts WHERE username = 'makdoodie'")
    system_instance.cursor.execute("SELECT * FROM friends")
    friends_table = system_instance.cursor.fetchall()
    assert len(friends_table) == 1
    assert friends_table[0] == values


#Subtask 3: Create friend’s table with 3 fields: sender (fk accounts), receiver (fk accounts) and status (pending, accepted) Primary Key (sender, receiver)

#Ensure that the 'friends' table is created with the correct attributes and schema
def test_friends_table_creation_withFields(system_instance): 
    # Get the column names of the friends table
    system_instance.cursor.execute("PRAGMA table_info(friends)")
    columns = system_instance.cursor.fetchall()
    column_names = [column[1] for column in columns]
    # Define the expected column names
    expected_columns = [
        'sender',
        'receiver',
        'status'
    ]
    # Assert that the column names match the expected column names
    assert column_names == expected_columns

#Subtask 4: Add insert trigger on friend table to enforce unique combinations of sender and receiver.
def test_unique_requests(system_instance, temp_remove_accounts, capsys, name_register ,name_register_1):
    query = "INSERT OR IGNORE INTO friends (sender, receiver, status) VALUES (?,?,?) RETURNING rowid"
    values = ('makdoodie', 'mad', 'pending')
    system_instance.cursor.execute(query, values)
    query = "INSERT OR IGNORE INTO friends (sender, receiver, status) VALUES (?,?,?) RETURNING rowid"
    values = ('mad', 'makdoodie', 'pending')
    try:
      system_instance.cursor.execute(query, values)
      assert False
    except sqlite3.IntegrityError:
      assert True
    system_instance.cursor.execute("SELECT COUNT(*) FROM friends")
    row_count = system_instance.cursor.fetchone()[0]
    assert row_count == 1
