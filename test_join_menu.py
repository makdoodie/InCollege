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
      "INSERT INTO accounts (username, password) VALUES (?, ?)",
      saved_accounts)
  system_instance.conn.commit()


@pytest.mark.usefixtures("temp_remove_accounts")
def test_join_menu(system_instance, capsys):
  # initialize menu options
  system_instance.initMenu()

  join_msg = "Would You Like To Join Your Friends On InCollege?"
  join_menu = ["Login", "Register", "Return To Home Page"]

  # simulate creating an account and then simulate user searching for that person
  with mock.patch('builtins.input', side_effect=['2', 'Jane35', 'Jane', 'Smith', 'Testing12*', 'Testing12*', 'Jane35', 'Testing12*', '0', '3', 'Jane', 'Smith', '0', '0']):
    system_instance.home_page()

  # capture output
  captured = capsys.readouterr()

  assert join_msg in captured.out
  for item in join_menu:
    assert item in captured.out