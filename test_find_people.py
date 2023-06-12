import pytest
from system import System
from unittest import mock


@pytest.fixture
def system_instance():
  return System()


# Austin's fixture from Sprint 1
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
      "INSERT INTO accounts (username, password, fName, lName) VALUES (?, ?, ?, ?)",
      saved_accounts)
  system_instance.conn.commit()


# Check for Find People I Know Option
def test_find_people(system_instance):
  # initialize menu options
  system_instance.initMenu()

  # access homePage attribute
  home_page = system_instance.homePage

  # check if the Find People I Know option is available
  assert '3' in home_page.selections, "Selection '3' not found in home page options"
  assert home_page.selections['3'] == {
    'label': 'Find People I Know',
    'action': system_instance.findUser
  }


# Check for first and last name prompts
def test_name_prompt(system_instance, capsys):
  # initialize menu options
  system_instance.initMenu()

  # simulate user choosing Find People I Know Option
  with mock.patch('builtins.input', side_effect=['3', 'John', 'Doe', '0', '0']):
    system_instance.home_page()

  # capture output
  captured = capsys.readouterr()

  # assert user is prompted for first and last name
  assert "Enter First Name:" in captured.out
  assert "Enter Last Name:" in captured.out

# Query accounts table for matching first and last name
@pytest.mark.usefixtures("temp_remove_accounts")
def test_query_names(system_instance, capsys):
  # initialize menu options
  system_instance.initMenu()

  first_name = "jane"
  last_name = "smith"

  # simulate creating an account and then simulate user searching for that person
  with mock.patch('builtins.input', side_effect=['2', 'Jane35', first_name, last_name, 'Testing12*', 'Testing12*', 'Jane35', 'Testing12*', '0', '0']):
    system_instance.home_page()

  system_instance.cursor.execute(
    "SELECT * FROM accounts WHERE UPPER(fName) = UPPER(?) AND UPPER(lName) = UPPER(?)",
    (first_name, last_name))

  result_lower = system_instance.cursor.fetchall()

  assert len(result_lower) > 0

  system_instance.cursor.execute(
    "SELECT * FROM accounts WHERE UPPER(fName) = UPPER(?) AND UPPER(lName) = UPPER(?)",
    (first_name.capitalize(), last_name.capitalize()))

  result_capital = system_instance.cursor.fetchall()

  assert len(result_capital) > 0


# Check for message when user is located
@pytest.mark.usefixtures("temp_remove_accounts")
def test_user_located(system_instance, capsys):
  # initialize menu options
  system_instance.initMenu()

  # simulate creating an account and then simulate user searching for that person
  with mock.patch('builtins.input', side_effect=['2', 'Jane35', 'Jane', 'Smith', 'Testing12*', 'Testing12*','Jane35', 'Testing12*', '0', '3', 'Jane', 'Smith', '0', '0']):
    system_instance.home_page()

  # capture output
  captured = capsys.readouterr()

  assert "They Are Part Of The InCollege System." in captured.out


# Check for message when user not in system
def test_user_not_located(system_instance, capsys):
  # initialize menu options
  system_instance.initMenu()

  # simulate user choosing Find People I Know Option
  with mock.patch('builtins.input', side_effect=['3', 'John', 'Doe', '0',
                                                 '0']):
    system_instance.home_page()

  # capture output
  captured = capsys.readouterr()

  # assert user is prompted for first and last name
  assert "They Are Not Yet A Part Of The InCollege System." in captured.out


