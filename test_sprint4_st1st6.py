import pytest
import string
import random
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
      "INSERT INTO accounts (username, password, fName, lName, university, major) VALUES (?, ?, ?, ?, ?, ?)",
      saved_accounts)
  system_instance.conn.commit()

# generates a random string based on the provided parameters
def generate_random_string(length, num_upper, num_digits, num_special):
  special = '!@#$%^&*()_+-=[]{}|;:,.<>/?`~\'\"\\'
  selected_chars = []
  # exception sum of number of uppercase, digits, and specials must not exceed string length
  if length < (num_upper + num_digits + num_special):
    raise Exception(
      "Total number of uppercase, digits, and special characters exceeds length."
    )
  # add special characters
  for i in range(num_special):
    selected_chars.append(random.choice(special))
  # add digits
  for i in range(num_digits):
    selected_chars.append(random.choice(string.digits))
  # add uppercase letter
  for i in range(num_upper):
    selected_chars.append(random.choice(string.ascii_uppercase))
  # add remaining lowercase letters
  length = length - num_digits - num_special - num_upper
  for i in range(length):
    selected_chars.append(random.choice(string.ascii_lowercase))
  # shuffle password and return as string
  random.shuffle(selected_chars)
  return ''.join(selected_chars)

@pytest.fixture #test that user can input first and last name when registering
def name_register(system_instance, temp_remove_accounts, capsys):
  inputs = ['2', 'ahmad', 'ah', 'mad', 'usf', 'cs', 'Asibai1$', 'Asibai1$', 'ahmad', 'Asibai1$', '0', '0']
  with mock.patch('builtins.input', side_effect=inputs):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out
  assert 'Account created successfully.' in output
  yield

def test_register_success(system_instance, capfd, temp_remove_accounts):
  system_instance.initMenu()
  account_limit = 10
  msg_max_accounts = "Maximum Number Of Accounts Created!"
  msg_reg_success = "Account created successfully."
  # register max number of accounts
  temp_accounts = []
  for i in range(account_limit):
    length = random.randint(5, 25)
    username = generate_random_string(length, 1, 1, 0)
    length = random.randint(8, 12)
    password = generate_random_string(length, 1, 1, 1)
    fName = generate_random_string(8, 1, 0, 0)
    lName = generate_random_string(8, 1, 0, 0)
    university = 'usf'
    major = 'cs'
    # simulate 5 users creating an account
    with mock.patch('builtins.input', side_effect=['2', username, fName, lName,university,major,password, password, username, password, '0', '0']):
      system_instance.home_page()
    std = capfd.readouterr()
    assert msg_reg_success in std.out.strip()
    password = system_instance.encryption(password)
    temp_accounts.append((username, password))
  # account limit reached, registering next account must fail
  length = random.randint(5, 25)
  username = generate_random_string(length, 1, 1, 0)
  length = random.randint(8, 12)
  password = generate_random_string(length, 1, 1, 1)
  fName = generate_random_string(8, 1, 0, 0)
  lName = generate_random_string(8, 1, 0, 0)
  # simulate 11th user creating an account 
  with mock.patch('builtins.input', side_effect=['2', username, fName, lName, university, major, password, password, username, password, '0', '0']):
      system_instance.home_page() 
  std = capfd.readouterr()
  user_query = "SELECT * FROM accounts WHERE (username, password) = (?, ?)"
  system_instance.cursor.execute(
    user_query, (username, system_instance.encryption(password)))
  account = system_instance.cursor.fetchone()
  assert msg_max_accounts in std.out.strip() and account is None

def test_findfriend(system_instance, capsys, name_register): #tests that show my network is an option, then checks that the first and last name is displayed in show my network for all friends of the user, then connects with a friend and checks that once disconnected with that same friend, the former friend does not appear in show my network
  inputs = ['2', 'james', 'sm', 'ith', 'usf', 'cs', 'Jsmith1!', 'Jsmith1!', 'james', 'Jsmith1!', '2', '1', '1', 'mad', '1', '1', '0', '0', '0', '0', '0', '1', 'ahmad', 'Asibai1$', '2', '3', '1', '1', '0', '0', '2', '1', '1', '0', '0', '0', '0', '0']
  with mock.patch('builtins.input', side_effect=inputs):
    system_instance.home_page()
  captured = capsys.readouterr()
  output = captured.out
  assert '[2] Show My Network' in output
  assert '[1] sm ith' in output
  assert 'Name: sm ith\nUsername: james\nUniversity: usf\nMajor: cs\n\n[1] Disconnect' in output
  assert 'You Have Disconnected From This User' in output
  assert 'You Have No Connections.' in output