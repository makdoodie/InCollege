# import pytest
# from unittest import mock
# from system import System
import sqlite3
from test_sprint5 import *

TEST_USER = [ 
  ['user1', 'hank', 'hill', 'uni1', 'major1', 'Password1!'],
  ['user2', 'bobby', 'hill', 'uni2', 'major2', 'Password2@'],
  ['user3', 'dale', 'gribble', 'uni3', 'major3', 'Password3#'],
  ['user4', 'john', 'redcorn', 'uni4', 'major4', 'Password4$'],
  ['user5', 'khan', 'souphanousinph', 'uni5', 'major5', 'Password5%'],
]

TEST_USER_SETTINGS = [['user1', False, False, True, 'English'],
                      ['user2', False, True, False, 'Spanish'],
                      ['user3', True, True, False, 'English'],
                      ['user4', False, False, True, 'Spanish'],
                      ['user5', True, False, False, 'English'],
                     ]

TEST_FRIENDS = [[TEST_USER[0][0], TEST_USER[1][0], 'pending'],
                [TEST_USER[1][0], TEST_USER[2][0], 'accepted'],
                [TEST_USER[3][0], TEST_USER[2][0], 'pending'],
                [TEST_USER[4][0], TEST_USER[3][0], 'accepted'],
                [TEST_USER[4][0], TEST_USER[0][0], 'pending'],
               ]

TEST_JOBS = [['job1', 'description1', 'employer1', 'location1', 1000, 'first1', 'last1'],
             ['job2', 'description2', 'employer2', 'location2', 2000, 'first2', 'last2'],
            ]

TEST_EXPERIENCES = [['user1', 'title1', 'employer1', '1111-11-10', '1111-11-11', 'location1', 'description1'],
                    ['user1', 'title2', 'employer2', '1111-11-12', '1111-11-13', 'location2', 'description2'],
                    ['user4', 'title4', 'employer4', '4444-44-40', '4444-44-41', 'location4', 'description4'],
                   ]

LOGIN_SUCCESS = "You Have Successfully Logged In!"
REGISTER_SUCCESS = "Account created successfully."

# @pytest.fixture
# def system_instance():
#   """Creates and instance of the system performs some menu initialization."""
#   s1 = System()
#   s1.initMenu()
#   return s1

# @pytest.fixture
# def clear_restore_db(system_instance): 
#   """Sets up the database for testing by saving and clearing any persistent records, 
#   after a test finishes test records are cleared and saved records are restored."""
#   data = {}
#   # tables with FKs referencing other tables should come after the referenced table
#   tables = ['accounts', 'friends', 'experiences', 'jobs']
#   # store each of the tables into a dictionary
#   for table in tables:
#     system_instance.cursor.execute(f"SELECT * FROM {table}")
#     data[table] = system_instance.cursor.fetchall()

#   # delete all records from the the accounts table, 
#   # and should auto delete all records from tables with FK to accounts
#   if len(data[tables[0]]):
#     system_instance.cursor.execute("DELETE FROM accounts")
#     system_instance.conn.commit()
#   # delete all records from the jobs table
#   if len(data[tables[-1]]):
#     system_instance.cursor.execute("DELETE FROM jobs")
#   system_instance.conn.commit()
    
#   yield
#   # delete any testing records from the database 
#   system_instance.cursor.execute("DELETE FROM accounts")
#   # restore saved records to all tables 
#   for table in tables:
#     if len(data[table]):
#       # add a ? to the list of parameters for each column in the table
#       parameters = f"({','.join('?' for col in data[table][0])})"
#       query = f"INSERT INTO {table} VALUES {parameters}"
#       system_instance.cursor.executemany(query, data[table])
#   system_instance.conn.commit()


# tests the clear setup part of clear_restore_db
def test_clear(system_instance, clear_restore_db):
  # tables with FKs referencing other tables should come after the referenced table
  tables = ['accounts', 'friends', 'experiences', 'jobs']
  print()
  for table in tables:
    system_instance.cursor.execute(f"SELECT * FROM {table}")
    result = system_instance.cursor.fetchall()
    print(table + "============================")
    for row in result:
      print(row)

# tests the teardown part of clear_restore_db
def test_restore(system_instance):
  # tables with FKs referencing other tables should come after the referenced table
  tables = ['accounts', 'friends', 'experiences', 'jobs']
  print()
  for table in tables:
    system_instance.cursor.execute(f"SELECT * FROM {table}")
    result = system_instance.cursor.fetchall()
    print(table + "============================")
    for row in result:
      print(row)

# PERSISTENT USERS + ASSOCIATED RECORDS ===============================================================

# not a test or fixture, registers persistent users
def persistent_registration(system_instance, capsys):
  for user in TEST_USER:
    inputs = list(user)
    inputs.append(user[-1]) # additional copy of password for the check
    with mock.patch('builtins.input', side_effect=inputs):
      system_instance.register()
    output = capsys.readouterr().out
    assert REGISTER_SUCCESS in output

# not a test or fixture, populates jobs table with persistent records
def persistent_jobs(system_instance):
  fields = "(title, description, employer, location salary, posterFirstName, posterLastName)"
  for job in TEST_JOBS:
    system_instance.cursor.execute("INSERT INTO jobs VALUES (?,?,?,?,?,?,?)", tuple(job))
  system_instance.conn.commit()
  system_instance.cursor.execute("SELECT * FROM jobs")
  result = system_instance.cursor.fetchall()
  for row in result:
    print(row)

# not a test or fixture, populates experiences table with persistent records
def persistent_experiences(system_instance):
  fields = "(username, title, employer, dateStarted, dateEnded, location, description)"
  for exp in TEST_EXPERIENCES:
    system_instance.cursor.execute(f"INSERT INTO experiences {fields} VALUES (?,?,?,?,?,?,?)", tuple(exp))
  system_instance.conn.commit()
  system_instance.cursor.execute("SELECT * FROM experiences")
  result = system_instance.cursor.fetchall()
  for row in result:
    print(row)

# not a test or fixture, populates friends table with persistent records
def persistent_friends(system_instance):
  fields = "(sender, receiver, status)"
  for relation in TEST_FRIENDS:
    system_instance.cursor.execute("INSERT INTO friends VALUES (?,?,?)", tuple(relation))
  system_instance.conn.commit()
  system_instance.cursor.execute("SELECT * FROM friends")
  result = system_instance.cursor.fetchall()
  for row in result:
    print(row)


# START STORY 1 TESTS ==================================================================================

def test_accounts_schema(system_instance):
  # retreive experiences table schema from database
  query = 'PRAGMA table_info(accounts)'
  system_instance.cursor.execute(query)
  result = [(row[0], row[1], row[2], row[3], row[5]) for row in system_instance.cursor.fetchall()]
  # columns: col num, name, type, not null, primary key
  # note: the not null column is only 1 for explicit not null constraints
  expected = [(0, 'username', 'varchar2(25)', 0, 1),
              (1, 'password', 'varchar2(12)', 0, 0),
              (2, 'fName', 'varchar2(25)', 0, 0),
              (3, 'lName', 'varchar2(25)', 0, 0),
              (4, 'university', 'TEXT', 0, 0),
              (5, 'major', 'TEXT', 0, 0),
              (6, 'yearsAttended', 'INT', 0, 0),
              (7, 'title', 'varchar2(50)', 0, 0),
              (8, 'infoAbout', 'TEXT', 0, 0),
              (9, 'profile', 'BOOLEAN', 0, 0),
             ]
  # compare against expected schema
  assert result == expected


def test_experiences_schema(system_instance):
  # retreive experiences table schema from database
  query = 'PRAGMA table_info(experiences)'
  system_instance.cursor.execute(query)
  result = [(row[0], row[1], row[2], row[3], row[5]) for row in system_instance.cursor.fetchall()]
  # columns: col num, name, type, not null, primary key
  # note: the not null column is only 1 for explicit not null constraints
  expected = [(0, 'expID', 'INTEGER', 0, 1),
              (1, 'username', 'VARCHAR(25)', 0, 0),
              (2, 'title', 'TEXT', 0, 0),
              (3, 'employer', 'TEXT', 0, 0),
              (4, 'dateStarted', 'TEXT', 0, 0),
              (5, 'dateEnded', 'TEXT', 0, 0),
              (6, 'location', 'TEXT', 0, 0),
              (7, 'description', 'TEXT', 0, 0),
             ]
  # compare against expected schema
  assert result == expected


def test_experiences_FK(system_instance, clear_restore_db):
  # insert 2 test users into accounts table
  validUsers = [('user1',), ('user2',)]
  tables = ['accounts', 'experiences']
  query = f"INSERT INTO {tables[0]} (username) VALUES (?)"
  system_instance.cursor.executemany(query, validUsers)
  system_instance.conn.commit()
  # insert same 2 test users into the experiences table
  table = 'experiences'
  query = f"INSERT INTO {tables[1]} (username) VALUES (?)"
  print(query)
  system_instance.cursor.executemany(query, validUsers)
  system_instance.conn.commit()
  # insert invalid test user into experiences table expecting integrity error
  try:
    system_instance.cursor.execute(query, ('userINVALID',))
    system_instance.conn.commit()
    assert False
  except sqlite3.IntegrityError as e:
    assert str(e) == 'FOREIGN KEY constraint failed'
  # delete 1 test user from accounts and check for correct FK cleanup
  query = f"DELETE FROM {tables[0]} WHERE username = ? RETURNING username"
  system_instance.cursor.execute(query, validUsers[0])
  result = system_instance.cursor.fetchone()
  assert result == validUsers[0] # result should match deleted test user
  query = f"SELECT username FROM {tables[1]}"
  system_instance.cursor.execute(query)
  result = system_instance.cursor.fetchall()
  system_instance.conn.commit()
  assert len(result) == 1 and result[0] == validUsers[1] # result should match remaining test user
  