import sqlite3
import re

class System:
  def __init__(self): #create and connect to db
    self.conn = sqlite3.connect("accounts.db") #establishes connection to SQLite database called accounts
    self.cursor = self.conn.cursor() #creates cursor object which is later used to execute SQL queries
    self.cursor.execute("CREATE TABLE IF NOT EXISTS accounts (id INT, username TEXT, password TEXT)") #execute method and cursor object are used to create table if one does not exist
    self.conn.commit() #commit method used to save changes
    
  def __del__(self): #closes connection to db
    self.conn.close() #closes connection to database

  def validate(self, password): #validate password
    if len(password) < 8 or len(password) > 12:
      return False
    if not re.search("[A-Z]", password):
      return False
    if not re.search("\d", password):
      return False 
    if not re.search("[!@#$%^&*()_+]", password):
      return False
    return True

  def login(self, username, password): #login check
    while True:
      self.cursor.execute("SELECT * FROM accounts WHERE username = ?", (username)) #? is placeholder for username
      account = self.cursor.fetchone() #fetches first row which query returns
      if account: #if the username exists, then we check that the password in the database matches the password the user inputted
        if account[2] == password:
          print("You have successfully logged in!")
          break
        else:
          print("Incorrect password.")
      else:
        print("Account not found, check credentials.")
        break
      password = input("Enter password again: ")
      
def register(self, username, password, password_check): #register check
  if password != password_check:
    print("Password and Password Check do not match.")
    return
  if not self.validate(password):
    print("Password must have 8-12 characters, at least one capital letter, one digit, and one special character!")
    return
  while True:
    self.cursor.execute("SELECT * FROM accounts WHERE username=?",(username,))
    exists_user = self.cursor.fetchone()
    if exists_user:
      print("Username exists already")
    else:
      self.cursor.execute("INSERT INTO accounts (username, password) VALUES (?, ?)", (username, password))
      self.conn.commit() #saving new account to database
      print("Account created successfully.")
  username = input("Enter another username: ")

class Student:
  def __init__(self, id, username, password):
    self.id = id #change 
    self.username = username
    self.password = password
    
system = System() #creating instance of System

def main():
  print("Welcome to the InCollege login page!\n")
  choice = int(input("Enter 1 to login or 2 to create an account: "))
  while(choice != 1 and choice != 2):
    choice = int(input("Enter 1 to login or 2 to create an account: "))
  if(choice == 1):
    username = input("Enter username: ")
    password = input("Enter password: ")
    system.login(username, password)
  else:
    username = input("Enter username: ")
    password = input("Enter password: ")
    password_check = input("Enter password again: ")
    system.create(username, password, password_check)
main()   