import pytest
from system import Jobs
import sqlite3
from system import System
from system import Menu
from unittest.mock import Mock
from unittest.mock import patch
import os
from unittest import mock


#story: As a developer, I want to add support for jobs to the DB and app, so that the "Post A Job" feature can be implemented.
#task 1: test this function: Create a jobs class with members: title, description, employer, location, salary, poster first name and last name.
def test_job_creation_with_description():
    job = Jobs(title="Software Engineer", employer="ABC Company", location="New York", salary=100000,
               posterFirstName="John", posterLastName="Doe", description="Job description")

    assert job.title == "Software Engineer"
    assert job.employer == "ABC Company"
    assert job.location == "New York"
    assert job.salary == 100000
    assert job.posterFirstName == "John"
    assert job.posterLastName == "Doe"
    assert job.description == "Job description"


def test_job_creation_with_default_values():
    job = Jobs(title="", employer="", location="", salary=0, posterFirstName="", posterLastName="")

    assert job.title == ""
    assert job.employer == ""
    assert job.location == ""
    assert job.salary == 0
    assert job.posterFirstName == ""
    assert job.posterLastName == ""
    assert job.description is None

#Create a jobs table in the database with fields: title, description, employer, location, salary, poster (first and last name). 

# # this method  verify if the 'jobs' table is successfully created in the database.
def test_jobs_table_creation(): 
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    # Check if the 'jobs' table exists in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='jobs'")
    table_exists = cursor.fetchone()
    conn.close()
    # Assert that the 'jobs' table exists
    assert table_exists is not None

# # this method is to ensure that the 'jobs' table is created with the correct attributes and schema.

def test_jobs_table_creation_withFields(): 
    # Connect to the database
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    # Get the column names of the jobs table
    cursor.execute("PRAGMA table_info(jobs)")
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]
    # Define the expected column names
    expected_columns = [
        'title',
        'description',
        'employer',
        'location',
        'salary',
        'posterFirstName',
        'posterLastName'
    ]
    # Assert that the column names match the expected column names
    assert column_names == expected_columns
    # Cleanup: Close the connection
    conn.close()

#Test that includes checking the field types and primary keys of the jobs table:

def test_jobs_table_schema():
    # Connect to the database
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    # Get the column information of the jobs table
    cursor.execute("PRAGMA table_info(jobs)")
    columns = cursor.fetchall()
    # Define the expected field types and primary keys
   #A value of 1 means the column does not allow NULL values, and 0 means NULL values are allowed.
    expected_schema = {
        'title': ('VARCHAR(128)', 0, None, 1),
        'description': ('TEXT', 0, None, 0),
        'employer': ('VARCHAR(128)', 1, None, 0),
        'location': ('VARCHAR(128)', 1, None, 0),
        'salary': ('DECIMAL(10, 2)', 1, None, 0),
        'posterFirstName': ('VARCHAR(128)', 0, None, 0),
        'posterLastName': ('VARCHAR(128)', 0, None, 0)
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

#story: As I developer, I want to fix outstanding issues from previous sprint, so that the product owner is satisfied.

# Replace Skill A-E placeholders with actual skill names.

def test_skillA(capsys):
  system = System()
  system.skillA()
  captured = capsys.readouterr()
  assert "Project Managment" in captured.out
  assert "Under Construction" in captured.out


def test_skillB(capsys):
  system = System()
  system.skillB()
  captured = capsys.readouterr()
  assert "Networking" in captured.out
  assert "Under Construction" in captured.out


def test_skillC(capsys):
  system = System()
  system.skillC()
  captured = capsys.readouterr()
  assert "System Design" in captured.out
  assert "Under Construction" in captured.out


def test_skillD(capsys):
  system = System()
  system.skillD()
  captured = capsys.readouterr()
  assert "Coding" in captured.out
  assert "Under Construction" in captured.out


def test_skillE(capsys):
  system = System()
  system.skillE()
  captured = capsys.readouterr()
  assert "Professional Communication" in captured.out
  assert "Under Construction" in captured.out

  def test_guestSearch(capsys):
    system = System()
    system.guestSearch()
    captured = capsys.readouterr()
    assert "Professional Communication" in captured.out
    assert "Under Construction" in captured.out

#Convert all prompts to title case
def is_title_case(string):
     return string.istitle()

@pytest.mark.parametrize("prompt", [
     "Welcome To The Incollege Home Page!",
      
     "The Place Where Students Take The Next Big Step.",

      ])
def test_prompt_title_case(prompt):
    assert is_title_case(prompt), f"Prompt '{prompt}' is not in title case"

#Clear the console each time before a new menu is displayed.
def test_clear_console_before_menu_display():
    # Instantiate the Menu class
    menu = Menu()
    
    # Mock the os.system method to capture the console clear command
    with mock.patch('os.system') as mock_system:
        # Call the displaySelections method
        menu.clear()
        
        # Assert that the os.system method was called with the clear command
        mock_system.assert_called_with('clear' if os.name != 'nt' else 'cls')

# #story: As a signed in user, I want to be able to post a job including details about the title, description, employer, location, and salary.
# Task 1: Add a "Post A Job" option to the "Job Search/Internship" menu.
def test_addPostJobOption():
  #istance of the class system
  system=System()
  # initialize menu options
  system.initMenu()

  # access main menu attribute
  mainmenu =system.mainMenu
  #acces job menu attribute 
  jobmenu =system.jobsMenu
  #check if the job/searchInsership is in the main menu
  assert '1' in mainmenu.selections, "Selection '1' not found in jobs menu options"
  assert mainmenu.selections['1'] == {
    'label': 'Job/Internship Search',
    'action': system.jobs_menu
  }
  #check that the Post Job option is in the menu under job/search
  assert jobmenu.opening == "Welcome to the Job Postings Page"
  assert jobmenu.selections['1'] == {
    'label': 'Post Job',
    'action': system.postJob
  }
  assert jobmenu.exitStatement == "Return To Main Menu"

 #task 2: 
# When the user selects "Post A Job" they should be prompted for a title, description, employer, location, and salary.

def test_post_job_prompt(monkeypatch, capsys):
    system_instance =System()
  # Prepare inputs for the postJob function
    monkeypatch.setattr('builtins.input', lambda : '')
    monkeypatch.setattr('builtins.input', lambda : '')
    monkeypatch.setattr('builtins.input', lambda : '')
    monkeypatch.setattr('builtins.input', lambda : '')
    monkeypatch.setattr('builtins.input', lambda : '')

    # Call the postJob function
    system_instance.postJob()

    # Capture the output
    captured = capsys.readouterr()

    # Assert the expected output
    assert "Enter Title: " in captured.out
    assert "Enter Description: " in captured.out
    assert "Enter Employer: " in captured.out
    assert "Enter Location: " in captured.out
    assert "Enter Salary: " in captured.out

# #The system will permit up to 5 jobs to be posted.
# #this function is to test if the system limit the user to post more than 5 jobs. 
def test_postJobLimitReached(capsys):
    # Create an instance of the System class or a mock object if available
    system = System()
    # Mock the countRows method to return a value equal to the job post limit (5)
    system.countRows = Mock(return_value=5)
    # Call the postJob method
    result = system.postJob()
    # Assert that the maximum jobs limit message is printed
    captured = capsys.readouterr()
    assert captured.out.strip() == "Maximum Number Of Jobs Posts Created!"
    # Assert that the method returns None
    assert result is None

# task 3: test to check that the Job is saved into the data base correctly

@pytest.fixture
def system_instance():
    # Create an instance of the System class or initialize your system
  # delete the value of the table job to do the test 
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM jobs")
    conn.commit()
    conn.close()
  
    system = System()

    # Perform any necessary setup or data insertion for the test
    # For example, insert test data into the database
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO jobs (title, description, employer, location, salary, posterFirstName, posterLastName) VALUES (?, ?, ?, ?, ?, ?, ?)", ('Test Job Title', 'Test Job Description', 'Test Employer', 'Test Location', 50000.00, 'John', 'Doe'))
    conn.commit()
    conn.close()

    # Return the system instance for the test
    return system

# this test check that the job was posted correctly into the data base . 
def test_job_created_correctlyInDataBase(system_instance):
    # Retrieve the inserted job data from the database
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE title=?", ('Test Job Title',))
    result = cursor.fetchone()
    conn.close()

    # Assert that the job data matches the expected values
    assert result[0] == "Test Job Title"
    assert result[1] == "Test Job Description"
    assert result[2] == "Test Employer"
    assert result[3] == "Test Location"
    assert result[4] == 50000.00
    assert result[5] == "John"
    assert result[6] == "Doe"

# this test make sure a valid salary when post a job 
def test_post_job_with_invalid_salary():
    system = System()
    # Define the invalid salary input
    invalid_salary = "Invalid Salary"
    
    # Use patch to mock the behavior of input() and provide the input values
    with patch('builtins.input', side_effect=['Title', 'Description', 'Employer', 'Location', invalid_salary]):
        # Call the postJob function
        result = system.postJob()
        
    # Perform assertions on the result
    assert result is None
   