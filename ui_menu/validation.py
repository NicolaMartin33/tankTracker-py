import tkinter as tk
import tkinter.ttk as ttk

from backend.config import connection_db, csr_object
from backend.queue import Queue


class validation:

  def __init__(self, menu):
    self.M = menu
    self.__lb_q = Queue()
    self.__ub_q = Queue()
    self.__boolQueue = Queue()
    self.__param_name_Q = Queue()
    
  #signup validation
  def new_validation(self, firstnm, lastnm, email, password1, password2, window, error_lbl):
    #calling userClass validations
    fNAME = self.M.U.set_fname(firstnm) 
    lNAME = self.M.U.set_lname(lastnm)
    uEMAIL1, uEMAIL2 = self.M.U.set_user_email(email)
    uPASS = self.M.U.set_user_pass(password1, password2)
    
    if (fNAME is False or lNAME is False or uEMAIL1 is False or uEMAIL2 is False or uPASS is False): #if any validation returns false
      error_lbl.config(text= 'please enter valid details') #error label placed
      error_lbl.place(x=150, y=200)
      print('signup entries invalid')
    else:
      print('right')
      if self.M.U.save() is True: #attempts save
        error_lbl.config(text= 'succesful, redirecting you to log in') #error label placed
        error_lbl.place(x=150, y=200)
        window.after(5000, window.destroy) # destroys sign up page after 5 seconds (5000 milliseconds)
        window.mainloop()
        self.M.L.login_gui() #takes user to login
      else:
        self.M.S.signup_gui() #reloads page
        error_lbl.config(text= 'error saving your details')
        error_lbl.place(x=150, y=200)
        print('save failed')
      
  #login validation
  def current_validation(self, userentry, passwordentry, error_label, login):
    email = userentry.get()
    password = passwordentry.get()
    table = 'user'
    
    #check values against table
    query = f'SELECT * FROM {table} WHERE (email = ? OR UserID = ?) AND password = ?'
    
    csr_object.execute(query, (email, email, password))
    result = csr_object.fetchone()
    self.M.get_userID(userentry)
    

    
    if bool(result) is True: #checks if anything was retrieved
      print('login succesful')
      login.destroy() #destroys login win
      self.M.H.home_gui() #logs user into the homepage
      
      
    else: #if false
      print('login failed')
      error_label.place(x=210, y=120)
      

      
  #validate dimension
  def tank_validation(self, capacity, num_fish, length, depth, width, name, error, win):
    #passes to table tank validation
    capac = self.M.TL.set_capacity(capacity) 
    fishnum = self.M.TL.set_NumFish(num_fish)
    len = self.M.TL.set_length(length)
    dep = self.M.TL.set_depth(depth)
    wid = self.M.TL.set_width(width)
    tank_name = self.M.TL.set_name(name)
    
    if (capac is False or fishnum is False or len is False or dep is False or wid is False or tank_name is False): #if anything fails
      error.place(x=300, y=230) #placec error label
      print('wrong')
    else: #if they are all valid
      print('right')
      validsave = self.M.TL.save(self.M.UserID) #attempts to save
      if validsave is True: #if it saves
        print('true')
        win.destroy()
        self.M.ParamPage.parameter_gui() #takes user to choose parameters
      else: #if save fails
        error.config(text = 'issue when saving, please double check entries')
        error.place(x=300, y=200)
        print('couldnt save dimensions')
        return False
        
  # validates parameter and boundaries
  def param_selection(self, win, tankcode, calcium, alkalinity, magnesium, ammonia, nitrate, nitrite, pH, UB_calcium,
                      UB_alk, UB_mag, UB_am, UB_rate, UB_rite, UB_ph,
                      LB_calcium, LB_alk, LB_mag, LB_am, LB_rate, LB_rite, LB_ph):
    
  
    #error label
    error_lbl = ttk.Label(win, text = 'save failed, please check your entries', font = self.M.reg_font, background = self.M.dflt_bg)
    
    ub_l = [UB_calcium,
      UB_mag,
      UB_alk,
      UB_am,
      UB_rate,
      UB_rite,
      UB_ph] #upper bounds list
    self.M.set_Q(ub_l, self.__ub_q)#making queue

    lb_l = [LB_calcium,
      LB_mag, 
      LB_alk,
      LB_am,
      LB_rate,
      LB_rite,
      LB_ph] #lower bounds list
    self.M.set_Q(lb_l, self.__lb_q) #making queue

    boollist = [calcium,
           magnesium,
           alkalinity,
           ammonia,
           nitrate,
           nitrite,
           pH] #boolean linked to list of params
    self.M.set_Q(boollist, self.__boolQueue) #making queue

    param_name_L = ['calcium','magnesium', 'alkalinity',
    'ammonia', 'nitrate', 'nitrite', 'pH']#the list of param names
    self.M.set_Q(param_name_L, self.__param_name_Q) #making queue

    paramID_Name_D = self.M.Param.parameter_name_dict #short var name

    print(paramID_Name_D)
    print(self.__lb_q.is_empty())
    print(self.__lb_q.is_empty())
    while not self.__param_name_Q.is_empty(): #if empty it will = false
      try:
        param_names = self.__param_name_Q.dequeue()
        ID = paramID_Name_D[param_names]
        while not self.__param_name_Q.is_empty():  #while there is something in the name queue
          try:
            param_names = self.__param_name_Q.dequeue() #takes first queue name
            ID = paramID_Name_D[param_names] #extracts parameter id position
            print(ID)
            UB_top = self.__ub_q.dequeue() #takes first upper boundary queue position
            print(UB_top)
            LB_top = self.__lb_q.dequeue() #takes first lower boundary queue position
            print(UB_top)
            boolparam = self.__boolQueue.dequeue() #takes the first selected(1 or 0) queue position
            print(boolparam)
            if self.M.PSelect.save(ID, tankcode, boolparam, UB_top, LB_top) is True: #if save works
              print('worked')
              valid= True
            else: #if save fails
              valid = False
              #placing error label
              error_lbl.pack(side = tk.BOTTOM)
          except Exception as e:
            error_lbl.pack(side = tk.BOTTOM) #placing error label
            print(e)
        win.destroy()
      except Exception as e: 
        print(f'error occurred: {e}')
        error_lbl = ttk.Label(win, text = 'save failed, please check your entries', font = self.M.reg_font, background = self.M.dflt_bg)
