import sqlite3
import re

class MenuMediator:
    def __init__(self):
      self.selections = {}
    ## Set Each Menu Item for the  
    def setSelection(self,hotKey,selection):
      self.selections[hotKey] = selection
    ## Displays Each Set Menu Item System Class performs the action  
    def displayMainMenu(self):
      for hotKey,selection in self.selections:
        print("["+hotKey+"] "+ selection['label'])
      print("[0] Exit")
      
    def startEnviroment(self):
      while True:
        self.displayMainMenu()
        selection = input("Please, make a selection")
        if(selection == '0'):
          print("Logging Out...")
          print("Exiting")
          break
        if selection in self.selections:
          thisSelection = self.selections[selection]
          menuItem = thisSelection['action']
          menuItem()
        else:
          print("Invalid Selection! Please Try Again")
          
class System:
  def __init__(self,loggedOn): #create and connect to db
    self.conn = sqlite3.connect("accounts.db") #establishes connection to SQLite database called accounts
    self.cursor = self.conn.cursor() #creates cursor object which is later used to execute SQL queries
    self.cursor.execute("CREATE TABLE IF NOT EXISTS accounts (username varchar2(25), password varchar2(12))") #execute method and cursor object are used to create table if one does not exist
    self.conn.commit() #commit method used to save changes
    self.loggedOn = loggedOn
    self.mediator = MenuMediator()
    
  def __del__(self,loggedOn): #closes connection to db
    self.conn.close() #closes connection to database

  def validatePassword(self, password,password_check): #validate password
    if(password != password_check):
      print("Passwords must match")
      return False
    if len(password) < 8 or len(password) > 12:
      print("Password must be 8-12 Characters in Length")
      return False
    if not re.search("[A-Z]", password):
      print("Password must contain at least one upper case letter")
      return False
    if not re.search("\d", password):
      print("Password must contain at least one number")
      return False 
    if not re.search("[!@#$%^&*()_+]", password):
      print("Password must contain at least one special character")
      return False
    return True
    
  def validateUserName(self, userName): #validate Username
      self.cursor.execute("SELECT * FROM accounts WHERE username=?", (userName,))
      exists_user = self.cursor.fetchone()
      if exists_user:
        print("Username has been taken.")
        return False
      if len(userName) > 25:
        print("Username must be less than 25 Characters in Length")
        return False
      return True

  def login(self, username, password): #login check
      self.cursor.execute("SELECT * FROM accounts WHERE username = ?", (username,)) 
      #? is placeholder for username
      account = self.cursor.fetchone() #fetches first row which query returns
      if account: #if the username exists, then we check that the password in the database matches the password the user inputted
        # Password needs encrypted/decrypted here
        if account[2] == password:
          print("You have successfully logged in!")
          return True
        else:
          print("Invalid username/password, try again!")
      else:
        print("Account not found, check credentials.")
      return False
      
  def register(self, username, password, password_check):
    ## Validate Inputs
    if self.validatePassword(password,password_check) and self.validateUserName(username):
      #Encrypt Password here
      self.cursor.execute("INSERT INTO accounts (username, password) VALUES (?, ?)", (username, password))
      self.conn.commit() #saving new account to database
      print("Account created successfully.")
      return True
    return False
    
  def loginMenu(self):
    print("Welcome to the InCollege sign in page!\n")
    choice = input("[1] Login [2] Create Account [0] Exit\n")
    while(True):
        if(choice == '0'):
          print("Ciao")
          break
        if not(self.loggedOn):
          if(choice == "1"):
            print("Log In:\n")
            username = input("Enter Username: ")
            password = input("Enter Password: ")
            self.loggedOn = self.login(username, password)
          elif(choice == "2"):
            registered = False
            print("Account Creation:\n")
            username = input("Enter Username: ")
            password = input("Enter Password: ")
            passwordCheck = input("Confirm Password: ")
            registered = self.register(username, password, passwordCheck)
            if(registered == True):
              print("Log In:\n")
              self.loggedOn = self.login(username, password)
          else:
            print("Incorrect input. Please try again.")
            choice = input("[1] Login [2] Create Account [0] Exit\n")
        else:
          break
  def mainMenu(self):
      self.mediator.setSelection('1',{'label':'Jobs','action':self.jobsMenu})
      self.mediator.startEnviroment()
  def jobsMenu(self):
      print("Under Construction")
      
      