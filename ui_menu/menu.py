
import tkinter as tk
from tkinter.font import *

#importing other classes for composition model
from backend.queue import Queue
from backend.apiquestions import apiQuestion_retrevial
from backend.config import connection_db, csr_object
from backend.emailreminders import emails
from table_classes.graphClass import Graph
from table_classes.parameter_SelectionClass import Parameter_Selection
from table_classes.parametersClass import Parameters
from table_classes.questionClass import Question
from table_classes.tankClass import Tanktbl
from table_classes.userClass import User
from ui_menu.display_questions import question_display
from ui_menu.graphing import Graphing
from ui_menu.home_page import home
from ui_menu.log_values import log
from ui_menu.login import login
from ui_menu.make_tank_choose import tank_page_buttons
from ui_menu.new_tank import tank
from ui_menu.parameter_page import parameter_set
from ui_menu.settings import settings
from ui_menu.signup import signup
from ui_menu.validation import validation


class menu:
  # setting class level variables 
  title_font = ('Veranda',
                12,
                BOLD) #default title font
  dflt_bg = '#FFFFFE' #default background 
  reg_font = ('Gotham',
              9) #default text font
  lbl_font = ('Nunito',
              10)  #default label font 
  dflt_btn = 'TButton'
  tk_bg = '#B4C3C7'   #used for the blue buttons in homepage
  toggle_count = 0 # used for show password function
  

  def __init__(self):
    # using composistion but to avoid circular imports made an instance of menu and made the classes attributes of the menu class so every class that passes menu can access every class defined within menu
    self.UserID = None
    self.user_password = None
    self.tank_code = None
    self.tank_name = None
    self.flipped_params = {}
    self.U = User() #user doesnt need to access only needs to be accessed by other classes
    self.L = login(self) #passing self, allows an instance of the class menu to be passed to the class of login
    self.S = signup(self)
    self.V = validation(self)
    self.H = home(self)
    self.T = tank(self)
    self.TL = Tanktbl()
    self.set = settings(self)
    self.ParamPage = parameter_set(self)
    self.Param = Parameters()
    self.PSelect = Parameter_Selection()
    self.Q = Question()
    self.LOG = log(self)
    self.E = emails()
    self.G = Graph(self)
    self.GING = Graphing(self)
    self.api = apiQuestion_retrevial(self)
    self.QD = question_display(self)
    self.TPB = tank_page_buttons(self)

  #makes a new window titled fish fundamentals and of the size 600x400
  def new_window(self):
    win= tk.Tk()
    win.minsize(600,400)
    win.title('FishFundamentals')
    win.configure(borderwidth= 9,
                  bg= self.dflt_bg)
    return win
    
  #retrieves userid from table by passing what the user entered when logging in, this could be their userid or their email so we pass both to retrieve only userid
  def get_userID(self, email):
    query = ("SELECT UserID FROM user WHERE (UserID = ? OR email = ?)") #sql statement that gets passed to get userid
    id = (csr_object.execute(query, (email.get(), email.get(),))).fetchone()
    
    self.UserID = str(id).strip('(,)') #removes the characters inside the brackets from the result

  #changes key into value and value into key
  def flip_dict(self, dict):
    self.flipped_params = {value: key for key, value in dict.items()} # if your dictionary looked like {'key' : 'fire'} it will now look like {'fire' : 'key'} which means you can pass fire to get the key value
    return self.flipped_params

  
  def deleteAccount(self, lbl):
    try:
      #deleting user details
      csr_object.execute(f"DELETE FROM user WHERE UserID = {self.UserID}")
      
      
      #getting user's tankcodes
      csr_object.execute(f"SELECT tank_code FROM tank WHERE UserID = {self.UserID}")
      tank_codes = csr_object.fetchall()
      
      
      #deleting rows where ever tankcodes are present
      for tankcode in tank_codes:
        tankcode = str(tankcode).strip('(,)')
        
        #deleting for tables where tankcode is a fk
        csr_object.execute(f"DELETE parameterSelection, graph FROM parameterSelection JOIN graph ON parameterSelection.tank_code = graph.tank_code WHERE parameterSelection.tank_code = {tankcode}") 
        
        
      #deleting tank table rows
      csr_object.execute(f"DELETE FROM tank WHERE UserID = {self.UserID}")
      connection_db.commit()
      
      
      #configuring the success label
      lbl.config(text = 'User Deletion was Successful, please log out')
      lbl.pack(side = tk.BOTTOM)
    
    except Exception as e:
      #no changes are applied
      print(f'error deleting user: {e}')
      
      #if error flags the data wont get saved, after commit() is called it cant undo anything
      connection_db.rollback()
      lbl.config(text = 'User Deletion was Unsuccessful, please retry')
      lbl.pack(side = tk.BOTTOM)

  
  def delete_tank(self, tankname, user):
    try:
      #gets tank code from table where the userid is the users and where the tankanem matches what the user selects
      csr_object.execute(f"SELECT tank_code FROM tank WHERE (UserID = {user} AND name = '{tankname}')")
      result = csr_object.fetchone()
      
      tankcode = str(result).strip('(,)') #removes specified characters from result makes it just 3 not (3,)
      
      #deleting other locations of tank_code, only tables where tankcode is a fk (foreign key)
      csr_object.execute(f"DELETE parameterSelection, graph FROM parameterSelection JOIN graph ON parameterSelection.tank_code = graph.tank_code WHERE parameterSelection.tank_code = {tankcode}") 
      
      
      
      #deleting tank table rows
      csr_object.execute(f"DELETE FROM tank WHERE tank_code = {tankcode}")
      connection_db.commit()
      
      return True
        
    except Exception as e:
      print(f'error deleting tank {e}')
      
      #no changes are applied
      connection_db.rollback() #error would break before commit so any changes would be reversed
      return False

  
  def password_show(self, password):
    self.toggle_count += 1 #allows for there to be an off/on state
    if self.toggle_count % 2 == 1:
      password.config(show='') #if it has been pressed an odd number of times button turns * to text
    else: #if even goes back to *
      password.config(show='*')

  
  #making queue
  def set_Q(self, list_to_queue, var):
    for item in list_to_queue: #enqueuing list making queue
      print(item)
      if var.enqueue(item):
        print('enqueued')
      else:
        print('failed to queue')

  
  def merge_sort(self, data_list, key='score'):
    if len(data_list) <= 1:
      return data_list

    mid = len(data_list) // 2
    left_half = self.merge_sort(data_list[:mid], key) #splitting based on score 
    right_half = self.merge_sort(data_list[mid:], key) #calls itself until base case (len ≤ 1) is true

    return self.QD.merge(left_half, right_half, key) #calls question display merge, if the merge sort was used more
 
    
  def startup(self):
    #api question only needs called once so gets turned into a comment after
    #self.api.get_question()
    print('hoorah') 
    self.Param.save() #saves parameter table 
    #self.E.datecheck() #checks last date email reminder was sent 
    self.L.login_gui() #calls login func

  

