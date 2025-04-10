import tkinter as tk
import tkinter.ttk as ttk

from backend.config import connection_db, csr_object
from backend.queue import Queue

class settings:
  def __init__(self, menu):
    self.M = menu 
    self.__ub_q = Queue()
    self.__lb_q = Queue()
    self.__param_name_Q = Queue()
    self.__boolQueue = Queue()
    
  #displays all the options of settings in button form for the user to select
  def mainpage_gui(self):
    mainset_win = self.M.new_window()
    UserID = self.M.UserID
    #labels
    heading = ttk.Label(mainset_win, 
                       text = 'Settings',
                       background = self.M.dflt_bg,
                       font = self.M.title_font)

    lbl = ttk.Label(mainset_win, 
                        text = '',
                        background = self.M.dflt_bg,
                        font = self.M.reg_font)
    
    #buttons
    email = ttk.Button(mainset_win,
                      text = 'Change Email',
                      style = self.M.dflt_btn,
                      width= 20,
                      command=lambda: self.email_gui(UserID)) #lets user change their email
    
    password = ttk.Button(mainset_win,
                       text = 'Change Password',
                       style = self.M.dflt_btn,
                       width= 20,
                       command=lambda: self.pass_gui(UserID)) #lets user change their password
    
    dimensions = ttk.Button(mainset_win,
                          text = 'Change Dimensions',
                          style = self.M.dflt_btn,
                          width= 20,
                          command=lambda: self.gettank('dimensions', UserID, lbl)) #lets user change their dimensions of a specific tank 

    home = ttk.Button(mainset_win,
                      text = 'home',
                      style = self.M.dflt_btn,
                      width = 10,
                      command= lambda: mainset_win.destroy()) #takes them baack to homepage
    
    params = ttk.Button(mainset_win,
                            text = 'Change Parameters',
                            style = self.M.dflt_btn,
                            width= 20,
                            command=lambda: self.gettank('parameters', UserID, lbl)) #lets user change their parameters and boundaries of a specific tank

    delete_tank = ttk.Button(mainset_win,
                        text = 'Delete a Tank',
                        style = self.M.dflt_btn,
                        width= 20,
                        command=lambda: self.gettank('tank', UserID, lbl)) #lets user delete a specific tank

    delete_acc = ttk.Button(mainset_win,
                            text = 'Delete Account',
                            style = self.M.dflt_btn,
                            width= 20,
                            command=lambda: self.M.deleteAccount(UserID, lbl)) #lets user delete account

    #placing
    heading.place(x=0,y=0)
    email.place(x=100,y=60)
    password.place(x=100,y=100)
    dimensions.place(x=100,y=140)
    params.place(x=100,y=180)
    delete_tank.place(x=100,y=220)
    delete_acc.place(x=100,y=260)
    home.place(x=475, y=350)

  #get tank more specific outcome than tcb get tank
  def gettank(self, value, UserID, lbl):
    # makes new win 
    win = self.M.new_window()
    heading = ttk.Label(win,
                       text = 'pick the tank you would like to edit',
                       font  = self.M.title_font,
                       background = self.M.dflt_bg)
    
    no_tank = ttk.Label(win,
                       text = 'You have no tanks',
                       font = self.M.reg_font,
                       background = self.M.dflt_bg)
    
    back = ttk.Button(win,
                      text = 'back to log in page',
                      style = self.M.dflt_btn,
                      width= 4,
                      command=lambda: win.destroy())
    # placing
    heading.place(x=0, y=0)
    back.place(x=400, y=350)

    # gets tank names based of userid
    query = f'SELECT name FROM tank WHERE UserID = ?'  #getting tank name
    csr_object.execute(query, (UserID,))
    results = csr_object.fetchall()
    connection_db.close()
    print(results)
    yval=[100] #sets y coord
    
    #if they have no tanks error is displayed
    if len(results) == 0:
      no_tank.place(x=300,y=200) #error label placed
    else:
      for result in results:
        print(result[0])
        self.make_button(result[0], win, value, yval, UserID, lbl) #place button for each tank  name
      win.mainloop()

  #make button for each tank
  def make_button(self, name, win, value, yaxis, UserID, lbl):
    print(f"Creating button '{name}' at Y Position = {yaxis}")
    button = ttk.Button(win,
                        text = name,
                        style = self.M.dflt_btn,
                        command=lambda name=name:  self.button_click(win, value, name, UserID, lbl)) 
    #name=name makes sure the value of name is the one captured at the time of definition not click
    
    button.place(x=100,y= yaxis[0])
    print(f"Placed button '{name}' at Y Position = {yaxis}") 
    yaxis[0] += 50 #incrementing  y coord
    
  def button_click(self, win, value, text_result, userid, lbl):
    if value == 'dimensions': #calls dimensions specific code
      self.change_dimensions_gui(text_result, userid)
      win.destroy()
    elif value == 'parameters': #calls parameter specific code
      self.change_parameters_gui(text_result, userid)
      win.destroy()
    elif value == 'tank': #tank specific code
      win.destroy()
      valid= self.M.delete_tank(text_result, userid) #attempts to delete tank
      if valid is True: 
        lbl.config(text = 'tank was succesfully deleted')
        lbl.pack(side = tk.BOTTOM)
      else:
        lbl.config(text = 'tank deletion failed, please retry')
        lbl.pack(side = tk.BOTTOM)
        
    
  #new email
  def email_gui(self, UserID):
    email_win = self.M.new_window()
    #labels
    new_email_lbl = ttk.Label(email_win,
                              text = 'Enter your new email:',
                              font = self.M.reg_font,
                              background = self.M.dflt_bg)
    
  
    password_lbl = ttk.Label(email_win,
                             text = 'Enter your password:',
                             font = self.M.reg_font,
                             background = self.M.dflt_bg)
    
    error_lbl = ttk.Label(email_win,
                               text = '',
                               font = self.M.reg_font,
                               background = self.M.dflt_bg)

    
    #entries
    new_email = ttk.Entry(email_win,
                          width = 25) 
    
    password = ttk.Entry(email_win,
                         width = 25,
                         show = '*')
    #buttons
    show_password = ttk.Button(email_win,
                               text = 'show',
                               style = self.M.dflt_btn,
                               width= 4,
                               command=lambda: self.M.password_show(password)) #toggle password show on and off
    

    save = ttk.Button(email_win,
                      text = 'save',
                      style = self.M.dflt_btn,
                      width= 4,
                      command=lambda: self.update_email(UserID, new_email, password, error_lbl, email_win)) #attempts to update email
   
    back = ttk.Button(email_win,
                      text = 'back',
                      style = self.M.dflt_btn,
                      width = 10,
                      command= lambda: email_win.destroy()) #return to settings
    #place
    new_email_lbl.place(x=0, y=70)
    new_email.place(x=0, y=90)

    password_lbl.place(x=0, y=130)
    password.place(x=0, y=150)

    show_password.place(x=210, y=145)
    save.place(x=0, y=170)
    back.place(x=450, y=350)
    
    email_win.mainloop()

  #validates and attempts to update emai
  def update_email(self, UserID, new_email, password, errorlbl, email_win):
    
    query = 'SELECT password FROM user WHERE UserID =?'
    csr_object.execute(query, (UserID,))
    result = csr_object.fetchone()
    connection_db.close()

    result = str(result).strip("'(,)'")
    email_valid, email_vaild1 = self.M.U.set_user_email(new_email) #passing details to be vaildated
    
    if email_valid is True and email_vaild1 is True and self.M.U.set_user_pass(result, password) is True: #validates entries against systems rules
    
      try:  #attempts to save new email
        
        query = 'UPDATE user SET email = ? WHERE UserID = ?'
        csr_object.execute(query, (new_email.get(), UserID,))
        connection_db.commit()
        connection_db.close()

        
        print(f'email updated to {new_email.get()}')
        email_win.destroy() #back to settings
        
      except Exception as e:
        print('error:', e)
    else:
      if self.M.U.set_user_pass(result, password) is not True: #if email wasnt correct
        errorlbl.place_forget() #removes other label if placed
        errorlbl.config(text = 'Incorrect password.')
        errorlbl.place(x=200, y=350)
      else:#if there was a different error
        errorlbl.place_forget()
        errorlbl.config(text ='Error updating email. Please try again.')
        errorlbl.place(x=200, y=370)

  #update password gui    
  def pass_gui(self, UserID):
    
    pass_win = self.M.new_window()
    
    #labels
    new_pass1_lbl = ttk.Label(pass_win,
                              text = 'Enter your new password:',
                              font = self.M.reg_font,
                              background = self.M.dflt_bg)

    new_pass2_lbl = ttk.Label(pass_win,
                              text = 'Re-Enter your new password:',
                              font = self.M.reg_font,
                              background = self.M.dflt_bg)
    
    password_lbl = ttk.Label(pass_win,
                             text = 'Enter your current password:',
                             font = self.M.reg_font,
                             background = self.M.dflt_bg)

    error_lbl = ttk.Label(pass_win,
                               text = '',
                               font = self.M.reg_font,
                               background = self.M.dflt_bg)


    #entries
    new_pass1 = ttk.Entry(pass_win,
                          width = 25) #new password
    
    new_pass2 = ttk.Entry(pass_win,
                          width = 25)
    
    password = ttk.Entry(pass_win,
                         width = 25,
                         show = '*') #old password
    #buttons
    show_password = ttk.Button(pass_win,
                               text = 'show',
                               style = self.M.dflt_btn,
                               width= 4,
                               command=lambda: self.M.password_show(password)) #toggle password off and on


    save = ttk.Button(pass_win,
                      text = 'save',
                      style = self.M.dflt_btn,
                      width= 4,
                      command=lambda: self.update_pass(UserID, new_pass1, new_pass2, password, error_lbl, pass_win)) #passes entries to update_pass func

    back = ttk.Button(pass_win,
                      text = 'back',
                      style = self.M.dflt_btn,
                      width = 10,
                      command= lambda: pass_win.destroy()) #back to settings
    #placing
    new_pass1_lbl.place(x=0, y=70)
    new_pass1.place(x=0, y=90)

    new_pass2_lbl.place(x=200, y=70)
    new_pass2.place(x=200, y=90)
    
    password_lbl.place(x=0, y=130)
    password.place(x=0, y=150)

    show_password.place(x=210, y=145)
    save.place(x=0, y=170)
    back.place(x=450, y=350)

    pass_win.mainloop()
    
  # attemps to update pass word and passes it to be validated
  def update_pass(self, UserID, pass1, pass2, current_pass, errorlbl, win):

    #gets current password
    query = 'SELECT password FROM user WHERE UserID =?'
    csr_object.execute(query, (UserID,))
    result = csr_object.fetchone()
    connection_db.close()
    result = str(result).strip("'(,)'")
    
    if self.M.U.set_user_pass(result, current_pass) is True and self.M.U.set_user_pass(pass1, pass2): #checks current password and old password match and validates password against system rules
      try:  #attempts to save
        query = 'UPDATE user SET password = ? WHERE UserID = ?'
        csr_object.execute(query, (pass1.get(), UserID,)) #updates password
        connection_db.commit()
        connection_db.close()
        print(f'password updated to {pass1.get()}')
        win.destroy()
        
      except Exception as e: #if it fails 
        errorlbl.config(text= 'Error Updating Password. Please try again later')
        errorlbl.place(x=200,y=350)
        print(f'an error occured updating password: {e}')
    else: #seperating errors in entries 
        if self.M.U.set_user_pass(result, current_pass) is not True: #if current and old dont match
          errorlbl.place_forget() #removes other label if placed
          errorlbl.config(text = 'Incorrect password.')
          errorlbl.place(x=200, y=350)
        else: #is passwords dont match
          errorlbl.place_forget()
          errorlbl.config(text ='Passwords do not match.')
          errorlbl.place(x=200, y=370)

  #change the dimensions gui
  def change_dimensions_gui(self, tankname, UserID):

  #sign up window
    new_dimensions_win = self.M.new_window()

  #create labels
    heading = ttk.Label(new_dimensions_win,
                        text = 'Enter your new dimensions.',
                        background = self.M.dflt_bg,
                        font = self.M.title_font)

    capac_lbl = ttk.Label(new_dimensions_win,
                          text = "Enter your Tank's capacity (L cubed):",
                          background = self.M.dflt_bg,
                          font = self.M.reg_font)

    FishNo_lbl = ttk.Label(new_dimensions_win,
                            text = 'Enter the number of fish:', 
                            background = self.M.dflt_bg,
                            font = self.M.reg_font)

    length_lbl = ttk.Label(new_dimensions_win,
                            text = 'Enter the length of your tank (cm):',
                            background = self.M.dflt_bg,
                            font = self.M.reg_font)

    depth_lbl = ttk.Label(new_dimensions_win,
                      text = 'Enter the depth of your tank (cm):',
                      background = self.M.dflt_bg,
                      font = self.M.reg_font)

    width_lbl = ttk.Label(new_dimensions_win,
                      text = 'Enter the width of your tank (cm):',
                      background = self.M.dflt_bg,
                      font = self.M.reg_font)
    name_lbl = ttk.Label(new_dimensions_win,
                         text = 'Enter the name of your tank:',
                         background = self.M.dflt_bg,
                         font = self.M.reg_font)

    error_lbl = ttk.Label(new_dimensions_win,
                          text = "Please only enter numbers!",
                          background = self.M.dflt_bg,
                          font = self.M.reg_font)

  #entries
    capacity = ttk.Entry(new_dimensions_win, width = 25)
    NumFish = ttk.Entry(new_dimensions_win, width = 25)
    length = ttk.Entry(new_dimensions_win, width = 25)
    depth = ttk.Entry(new_dimensions_win, width = 25)
    width = ttk.Entry(new_dimensions_win, width = 25)  
    name = ttk.Entry(new_dimensions_win, width = 25)

    back = ttk.Button(new_dimensions_win,
                      text = 'back',
                      style = self.M.dflt_btn,
                      width= 4,
                      command=lambda:
                      new_dimensions_win.destroy()) #back to settings

    save = ttk.Button(new_dimensions_win,
                      text = 'save',
                      style = self.M.dflt_btn,
                      width= 4,
                      command=lambda: self.dimension_buttonclick(UserID, tankname, capacity, NumFish, length, depth, width, name, error_lbl, new_dimensions_win)) #calls the code for updating dimensions

  #placing elements
    heading.place(x=0, y=1)
    capac_lbl.place(x=0, y=70)
    capacity.place(x=5, y=88)
    FishNo_lbl.place(x=0, y=120)
    NumFish.place(x=5, y=138)
    length_lbl.place(x=243,y=70)
    length.place(x=243,y=88)
    depth_lbl.place(x=243,y=120)
    depth.place(x=243, y=138)
    width_lbl.place(x=243, y=170)
    width.place(x=243, y=188)
    name_lbl.place(x=0, y=220)
    name.place(x=0, y=238)
    back.place(x=0, y=265)
    save.place(x=140, y=265)

  #validates and attempts to save dimensions
  def dimension_buttonclick(self, UserID, currentname, capacity, num_fish, length, depth, width, name, error_lbl, win):
    #validating entries
    capac = self.M.TL.set_capacity(capacity) 
    fishnum = self.M.TL.set_NumFish(num_fish)
    len = self.M.TL.set_length(length)
    dep = self.M.TL.set_depth(depth)
    wid = self.M.TL.set_width(width)
    tank_name = self.M.TL.set_name(name)
  
    if (capac is False or fishnum is False or len is False or dep is False or wid is False): #if any of the validations fail
      error_lbl.place(x=300, y=230)
      print('wrong')
    else: #if they are all valid
      try: 
        #using join to simplify the multiple sql statements into one
        query = 'UPDATE tank JOIN(SELECT tank_code FROM tank WHERE (UserID = ? AND name =?) AS tank ON tank.tank_code = tank.tank.code SET tank.capacity = ?, tank.numfish = ?, tank.length = ?, tank.depth = ?, tank.width = ?, tank.name = ?' 
        csr_object.execute(query, (capacity.get(), num_fish.get(), length.get(),
          depth.get(), width.get(), name.get(), UserID, currentname,))
        connection_db.commit() 
        connection_db.close()
        print(f'dimensions updated to capacity: {capacity.get()}, Num_Fish: {num_fish.get()}, length: {length.get()}, depth: {depth.get()}, width: {width.get()}, name: {name.get()}')
        win.destroy()
      except Exception as e:
        connection_db.rollback() #undo anything before commit is called
        error_lbl.config(text = 'Error Updating Dimensions')
        error_lbl.pack(side = tk.BOTTOM)
        print(f'an error occured updating Dimensions: {e}')
      



  # gui for changing parameters
  def change_parameters_gui(self, tankname, UserID):
    parameter_win = self.M.new_window()
    
    #getting tank code
    query = 'SELECT tank_code FROM tank WHERE (UserID = ? AND name =?)'
    csr_object.execute(query, (UserID, tankname,))
    tankcode = csr_object.fetchone()
    connection_db.close()
    
    #labels
    heading = ttk.Label(parameter_win,
                        text = 'Select Parameters',
                        background = self.M.dflt_bg,
                        font = self.M.title_font)

    title = ttk.Label(parameter_win,
                      text = 'Set the upper and lower bounds of your chosen parameters:',
                      background = self.M.dflt_bg,
                      font = self.M.reg_font)

    error_lbl = ttk.Label(parameter_win,
                      text = '',
                      background = self.M.dflt_bg,
                      font = self.M.reg_font)
    
    #entries
    UB_calcium = ttk.Entry(parameter_win, width = 8)
    LB_calcium = ttk.Entry(parameter_win, width = 8)

    UB_alk = ttk.Entry(parameter_win, width = 8)
    LB_alk = ttk.Entry(parameter_win, width = 8)

    UB_mag = ttk.Entry(parameter_win, width = 8)
    LB_mag = ttk.Entry(parameter_win, width = 8)

    UB_am = ttk.Entry(parameter_win, width = 8)
    LB_am = ttk.Entry(parameter_win, width = 8)

    UB_rate = ttk.Entry(parameter_win, width = 8)
    LB_rate = ttk.Entry(parameter_win, width = 8)

    UB_rite = ttk.Entry(parameter_win, width = 8)
    LB_rite = ttk.Entry(parameter_win, width = 8)

    UB_ph = ttk.Entry(parameter_win, width = 8)
    LB_ph = ttk.Entry(parameter_win, width = 8)

    #checkboxes
    cvar = tk.IntVar(parameter_win) #variable that stores the boolean
    calcium_ck = tk.Checkbutton(parameter_win,
                                 text = 'Calcium Levels',
                                 bg = self.M.dflt_bg, 
                                 font = self.M.reg_font,
                                 variable= cvar)
    alkvar = tk.IntVar(parameter_win)
    alkalinity_ck= tk.Checkbutton(parameter_win,
                                text = 'Alkalinity',
                                bg = self.M.dflt_bg,
                                font = self.M.reg_font,
                                variable= alkvar)

    magvar = tk.IntVar(parameter_win) 
    magnesium_ck = tk.Checkbutton(parameter_win,
                                  text = 'Magnesium Levels',
                                  background = self.M.dflt_bg,
                                  font = self.M.reg_font,
                                  variable= magvar)

    amvar = tk.IntVar(parameter_win)
    ammonia_ck = tk.Checkbutton(parameter_win,
                                text = 'Ammonia Levels',
                                background = self.M.dflt_bg,
                                font = self.M.reg_font,
                                variable= amvar)

    atevar = tk.IntVar(parameter_win)
    nitrate_ck = tk.Checkbutton(parameter_win,
                                text = 'Nitrate Levels',
                                background = self.M.dflt_bg,
                                font = self.M.reg_font,
                                variable= atevar)

    itevar = tk.IntVar(parameter_win)
    nitrite_ck = tk.Checkbutton(parameter_win,
                                text = 'Nitrite Levels',
                                background = self.M.dflt_bg,
                                font = self.M.reg_font,
                                variable= itevar)

    pcvar =tk.IntVar(parameter_win)
    pH_ck = tk.Checkbutton(parameter_win,
                           text = 'pH Levels',
                           background = self.M.dflt_bg,
                           font = self.M.reg_font,
                           variable = pcvar)

    next = ttk.Button(parameter_win,
      text = 'Choose',
      style = self.M.dflt_btn,
      width= 7,
      command=lambda: self.param_buttonclick(error_lbl, tankcode, cvar.get(), alkvar.get(),
                                                magvar.get(), amvar.get(), atevar.get(),
                                                itevar.get(), pcvar.get(),
                                                UB_calcium.get(), UB_alk.get(),
                                                UB_mag.get(), UB_am.get(),
                                                UB_rate.get(), UB_rite.get(),
                                                UB_ph.get(), LB_calcium.get(),
                                                LB_alk.get(), UB_mag.get(),
                                                LB_am.get(), LB_rate.get(),
                                                LB_rite.get(), LB_ph.get()
                                              )) #passing all the values
    back = ttk.Button(parameter_win,
                      text = 'back',
                      style = self.M.dflt_btn,
                      width= 7,
                      command=lambda: parameter_win.destroy()) #back to settings
    
    #placing
    heading.place(x=0,y=1)
    title.place(x=80,y=20)

    calcium_ck.place(x=0,y=70)
    UB_calcium.place(x=0,y=100)
    LB_calcium.place(x=70,y=100)

    alkalinity_ck.place(x=0,y=130)
    UB_alk.place(x=0,y=160)
    LB_alk.place(x=70,y=160)

    magnesium_ck.place(x=270,y=250)
    UB_mag.place(x=270,y=280)
    LB_mag.place(x=340,y=280)

    ammonia_ck.place(x=270,y=70)
    UB_am.place(x=270,y=100)
    LB_am.place(x=340,y=100)

    nitrate_ck.place(x=270,y=130)
    UB_rate.place(x=270,y=160)
    LB_rate.place(x=340,y=160)

    nitrite_ck.place(x=270,y=190)
    UB_rite.place(x=270,y=220)
    LB_rite.place(x=340,y=220)

    pH_ck.place(x=0,y=190)
    UB_ph.place(x=0,y=220)
    LB_ph.place(x=70,y=220)

    next.place(x=0, y=250)
    back.place(x=500, y=350)

  #making queue
  def set_Q(self, list, var):
    for item in list: #enqueuing list making queue
      var.enqueue(item[0])
      
  #attempts to save and validates entries
  def param_buttonclick(self, error_lbl, tankcode, calcium, alkalinity, magnesium, ammonia, nitrate, nitrite, pH, UB_calcium, UB_alk, UB_mag, UB_am, UB_rate, UB_rite, UB_ph, LB_calcium, LB_alk, LB_mag, LB_am, LB_rate, LB_rite, LB_ph):

    try:
      ub_l = [UB_calcium,
                    UB_mag,
                    UB_alk,
                    UB_am,
                    UB_rate,
                    UB_rite,
                    UB_ph] #upper bounds list
      self.set_Q(ub_l, self.__ub_q)#making queue
      
      lb_l = [LB_calcium,
                    LB_mag, 
                    LB_alk,
                    LB_am,
                    LB_rate,
                    LB_rite,
                    LB_ph] #lower bounds list
      self.set_Q(lb_l, self.__lb_q) #making queue
      
      boollist = [calcium,
                         magnesium,
                         alkalinity,
                         ammonia,
                         nitrate,
                         nitrite,
                         pH] #boolean linked to list of params
      self.set_Q(boollist, self.__boolQueue) #making queue
      
      param_name_L = ['calcium','magnesium', 'alkalinity',
         'ammonia', 'nitrate', 'nitrite', 'pH']#the list of param names
      self.set_Q(param_name_L, self.__param_name_Q) #making queue
      
      paramID_Name_D = self.M.Param.parameter_name_dict #short var name
      
      print(paramID_Name_D)
      print(self.__ub_q)
      print(self.__lb_q)
      while not self.__param_name_Q.is_empty(): #if empty it will = false
        try:
          param_names = self.__param_name_Q.dequeue()
          ID = paramID_Name_D[param_names]
          
          if not self.__ub_q.is_empty() and not self.__lb_q.is_empty() and self.__boolQueue: #still have elements 
            UB_top = self.__ub_q.dequeue() #removes first element and returns it
            LB_top = self.__lb_q.dequeue() #removes first element and returns it
            boolparam = self.__boolQueue.dequeue() #removes first element and returns it
            
            if UB_top.isalpha() is True or LB_top.isalpha() is True:
              print('Boundaries are not valid entries')
              error_lbl.config(text= 'entries are not valid')
              error_lbl.place(x=250, y=350)
            else:
              query = 'UPDATE parameterSelection SET is_Selected = ?, upperBound = ?, lowerBound = ? WHERE (ParameterID = ? AND tank_code =?)' #attempts to save
              csr_object.execute(query, (boolparam, UB_top, LB_top, ID, str(tankcode).strip("'(,)'"),))
              connection_db.commit()
              print('entries are valid and was saved')
              error_lbl.config(text= 'entries are valid')
              error_lbl.place(x=250, y=300)
            
          else: 
            print('nothing in queues')
            
        except Exception as e: #if while loop fails
          print(f'error occurred: {e}')
          error_lbl.forget() #if label already placed removed
          error_lbl.config(text='there was an error, please retry')
          error_lbl.place(x=250, y=55)
          break
          
    except Exception as e: #if everything in func fails
      print(f'error occurred: {e}')
      error_lbl.forget()
      error_lbl.config(text='there was an error, please retry')
      error_lbl.place(x=250, y=55)
        