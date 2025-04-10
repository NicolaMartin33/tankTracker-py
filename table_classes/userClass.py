import re
from sqlite3 import OperationalError

from backend.config import connection_db, csr_object


#class that maps to a table in the database
class User:
  def __init__(self):
    self.__first_name = None
    self.__last_name = None
    self.__email = None
    self.__password = None
    

  @classmethod #can be called outwith the class instance
  def create_tbl(cls):
    try:
      tblUser = """
          CREATE TABLE user (
              UserID INTEGER PRIMARY KEY,
              first_name CHAR(25) NOT NULL,
              last_name CHAR(25) NOT NULL,
              email VARCHAR(255) NOT NULL,
              password VARCHAR(25) NOT NULL
          ); """

      csr_object.execute(tblUser) #maps class to db
      print('table user created')
      connection_db.commit()
      

    except OperationalError: #printing statement to show user table already exists
      print('table user was not made as it already exists')
      
  
  #setting first name 
  def set_fname(self, firstname):
    valid_fname = False
    try:
      self.__first_name = firstname.get() #gets entry value
      valid_fname = self.__first_name.isalpha() #checks it is all letters if true valid_fname is set to true
      self.__first_name= self.__first_name.capitalize() #capitalises the first letter
      print('first name is valid')
    except Exception as e:
      print(f'error occurred: {e}') #means they didnt enter just letters so valid stays false
    return valid_fname

  #setting last name
  def set_lname(self, lastname):
    valid_lname = False
    try:  
      self.__last_name = lastname.get() #gets entry value
      valid_lname = self.__last_name.isalpha() #checks it is all letters if true valid_fname is set to true
      self.__last_name = self.__last_name.capitalize() #capitalises the first letter
      print('last name is valid')
    except Exception as e:
      print(f'error occurred: {e}') #means they didnt enter just letters so valid stays false
    return valid_lname
    
  def set_user_email(self, useremail):
    valid_email = False
    avlble_email = False
    
    try:
      self.__email = useremail.get() #gets entry
      valid_syntax = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b' #checks against re email skin
      if re.match(valid_syntax, self.__email): #if it matches the skin
          valid_email = True
      else: #if it doesnt
          valid_email = False
        
      table = 'user'
      query = f'SELECT * FROM {table} WHERE email = ?' #getting every email used in table user
      csr_object.execute(query, (self.__email,))
      result = csr_object.fetchone()
      if result: #checking if email has been used before
        avlble_email = False
        print('email used')
      else:
        avlble_email = True
        print('email not used')
    except Exception as e: 
      print(f'error occurred: {e}')
    print(valid_email, avlble_email)  
    return valid_email, avlble_email
    
  def set_user_pass(self, password1, password2):
    valid_pass = False
    digit_true = False
    try:
      try: #comparing passwords
        pass1 = password1.get()
      except AttributeError: #if entry has already been extracted
        pass1 = password1 
      pass2 = password2.get()
      if pass1 == pass2: #if they are the same
        self.__password = pass1
        valid_pass = True
        print('passwords match')
      else: #if they arent 
        valid_pass = False 
        
        return valid_pass
      if len(self.__password) < 20 and len(self.__password ) > 8 and valid_pass is True: #checks length of password
         for i in self.__password: #checks each index to see if it is a digit
          digit_true = i.isdigit()
          if digit_true is not False: #if it is true
            print('password contains a number')
            valid_pass = True
            break #only need one number so can break from loop
          else:
            valid_pass = False
            print('password doesnt contain a number')
      else: #if the len isnt within bounds
        valid_pass = False
        print('password doesnt fit length requirements')
    except Exception as e:
      print(f'error occured: {e}') 
      valid_pass = False
    return valid_pass #returns true or false
  
  #saves the data into the table    
  def save(self): 
    try:
      save_user = """
          INSERT INTO user ( first_name, last_name, email, password)
          VALUES (?,?,?,?)
      """
      csr_object.execute(save_user,(self.__first_name,
                                    self.__last_name,
                                    self.__email,
                                    self.__password))
      connection_db.commit()
     
      #inserting
      return True
    except Exception as e:
      print()
      print('there was an error', e) # describes error
      return False
      
