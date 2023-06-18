import os
import pytest
import sqlite3
from unittest import mock
from unittest.mock import Mock
from unittest.mock import patch
from system import Menu, Jobs, System


@pytest.fixture #creates instance of System and calls Main Menu
def system_instance():
  s1 = System()
  s1.initMenu()
  return s1
  
@pytest.fixture
def account_settings():
    # Create an instance of the System class or initialize your system
  # delete the value of the table job to do the test 
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM accounts")
    conn.commit()
    conn.close()
    system = System()
    # Perform any necessary setup or data insertion for the test
    # For example, insert test data into the database
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO accounts (username, password, fName, lName) VALUES (?, ?, ?, ?)", ('username', "Password123!", "Patrick","Shugerts"))
    conn.commit()
    conn.close()

    # Return the system instance for the test
    return system
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
  
def test_menu_navigation_to_useful_links(system_instance,capsys):
    # Create an instance of the System class
    # Mock the user input for menu navigation tests all routes
    with mock.patch('builtins.input', side_effect=['5','1','0','2','0','3','0','4','0','0']):
        # Call the menu navigation function
        system_instance.useful_links()
    # Capture the standard output
    captured = capsys.readouterr()
    # Assert that the captured output contains the expected text
    # This in combination with the patch
    assert 'Useful Links' in captured.out
    assert 'General' in captured.out
    assert 'Browse InCollege' in captured.out
    assert 'Business Solutions' in captured.out
    assert 'Directories' in captured.out
    assert 'Exit' in captured.out
     
def test_user_setting_init(system_instance):
    # Test Initial Settings in Guest User
    assert system_instance.user.sms == True
    assert system_instance.user.email == True
    assert system_instance.user.targetedAds == True
    assert system_instance.user.language == "English"
  
def test_account_settings_table_schema():
    # Connect to the database
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    # Get the column information of the jobs table
    cursor.execute("PRAGMA table_info(account_settings)")
    columns = cursor.fetchall()
    # Define the expected field types and primary keys
   #A value of 1 means the column does not allow NULL values, and 0 means NULL values are allowed.
    expected_schema = {
        'username': ('VARCHAR(25)', 0, None, 1),
        'email': ('BOOLEAN', 0, None, 0),
        'sms': ('BOOLEAN', 1, None, 0),
        'targetedAds': ('BOOLEAN', 1, None, 0),
        'language': ('VARCHAR(12)', 1, None, 0)
    }
 # Iterate over the columns and compare with expected schema
    for column in columns:
        column_name = column[1]
        field_type = column[2]
        is_primary_key = column[5]
        # Assert field type
        assert field_type == expected_schema[column_name][0]
        # Assert primary key
        assert is_primary_key == expected_schema[column_name][3]
    # Cleanup: Close the connection
    conn.close()

def test_set_sms(account_settings):
  # Ensure the user's SMS setting is initially True
  assert account_settings.user.sms == True
  # Perform the test by calling the relevant method on account_settings
  account_settings.setUserSMS()
  # Grab the user's SMS setting toconfirm update
  conn = sqlite3.connect("accounts.db")
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM account_settings WHERE username=?", ('username',))
  result = cursor.fetchone()
  conn.close()
  print(result)
  assert result[0] == "username"
  assert result[2] ==  0
  
def test_set_targetedAds(account_settings):
  # Ensure the user's SMS setting is initially True
  assert account_settings.user.targetedAds == True
  # Perform the test by calling the relevant method on account_settings
  account_settings.setUserTargetedAds()
  # Grab the user's SMS setting toconfirm update
  conn = sqlite3.connect("accounts.db")
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM account_settings WHERE username=?", ('username',))
  result = cursor.fetchone()
  conn.close()
  print(result)
  assert result[0] == "username"
  assert result[3] ==  0
  
def test_set_email(account_settings):
  # Ensure the user's SMS setting is initially True
  assert account_settings.user.email == True
  # Perform the test by calling the relevant method on account_settings
  account_settings.setUserEmail()
  # Grab the user's setting to confirm update
  conn = sqlite3.connect("accounts.db")
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM account_settings WHERE username=?", ('username',))
  result = cursor.fetchone()
  conn.close()
  print(result)
  assert result[0] == "username"
  assert result[1] ==  0
  

    
  

    




