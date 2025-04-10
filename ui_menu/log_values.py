import tkinter as tk
import tkinter.ttk as ttk

from backend.config import csr_object, connection_db


class log:
  def __init__(self, menu):
    self.M = menu
    self.paramids = []
    self.__lvl_id_dict = {} #stores levels against param ids
    self.__dsg_id_dict = {} #stores dosage against param ids

  #gets email from login entry
  def get_email(self, email_entry):
    #in case they entered UserID and not their email
    csr_object.execute(f"SELECT email FROM user WHERE (email = '{email_entry}' OR UserID = '{email_entry}')")
    email = csr_object.fetchone()
    
    if email: #if there was a result found 
      email = str(email).strip('(,)')
      return email

  #places tank name buttons for users to click
  def choose_tank(self):
    self.M.TPB.get_tank(self.log_gui) #if button is clicked log_gui is called
    
  #gets params from db tbl parameter selection with specified tankcode and positive bool value
  def get_params(self):
    query = 'SELECT ParameterID FROM parameterSelection WHERE (tank_code = ? AND is_Selected = 1)'
    csr_object.execute(query, (self.M.tank_code,))
    self.paramids = csr_object.fetchall()
    

   #setting the send_email parameters for boundary alert emails
  def param_emails(self, levels_dict):
    subject = 'Boundary Alert'
    user = self.get_email(self.M.UserID)
   
    print(self.paramids)
    
    for ID in self.paramids: 
      csr_object.execute(f'SELECT upperBound FROM parameterSelection WHERE (tank_code = {self.M.tank_code} AND ParameterID = {ID[0]})')
      UB = csr_object.fetchone() #getting upper boundary
      

      
      csr_object.execute(f'SELECT lowerBound FROM parameterSelection WHERE (tank_code = {self.M.tank_code} AND ParameterID = {ID[0]})')
      LB = csr_object.fetchone() #getting lower boundary
      
      
      param_name = self.M.flipped_params[ID[0]] #get param name from id

      print(param_name)
      print(levels_dict)
      print(str(levels_dict[ID[0]].get()))
      
      link = ''
      #comparing Levels entries with boundaries
      if str(levels_dict[ID[0]].get()) > str(UB).strip("'(,)'") and str(levels_dict[ID[0]].get()) != '' and str(levels_dict[ID[0]].get()).isalpha() == False: #if level_dict value is higher than boundary, and it hasnt been left blank and it isnt letters
        csr_object.execute(f'SELECT Upper_web FROM parameters WHERE  ParameterID = {ID[0]}')
        web = csr_object.fetchone()
        print('upper boundary broken')
        link = str(web).strip("'(,)'")
        
      elif str(levels_dict[ID[0]].get()) < str(LB).strip("'(,)'") and str(levels_dict[ID[0]].get()) != '' and str(levels_dict[ID[0]].get()).isalpha() == False: #if level_dict value is lower than boundary, and it hasnt been left blank and it isnt letters
        csr_object.execute(f'SELECT Lower_web FROM parameters WHERE  ParameterID = {ID[0]}') 
        web = csr_object.fetchone()
        print('lower boundary broken')
        link = str(web).strip("'(,)'")
        
      else: #entries dont fall out of boundaries
        print('no boundaries breached ')
        link=''
        continue

      try:
        body = (f"Your most recent update of {param_name}'s Level is outside of your specified Boundaries. \n This a webpage that could help you fix this: {link}. \n If you would like to edit your Parameter Boundaries, you can do so in settings!") #setting the message body value
        print(link)
        if link == '':
          print('error link empty')
        else: #only sent email if link has a value
          self.M.E.send_email(user, body, subject) 
          link = ''
      except Exception as e:
        print(f'error sending email: {e}')
    
  def log_gui(self):
    
    win = self.M.new_window()
    #list of parameterIDs that the tank selected
    self.get_params()
    print(self.paramids)
    #labels
    heading = ttk.Label(win,
                        text = 'Log Dosage and Levels',
                        background = self.M.dflt_bg,
                        font = self.M.title_font)

    #buttons
    
    
    back = ttk.Button(win,
                      text = 'back',
                      style = self.M.dflt_btn,
                      width= 7,
                      command=lambda: win.destroy())
    
    self.display(win, back)
    
    heading.place(x=0,y=1)
    back.place(x=500, y=350)

      
  def display(self, win, back_btn):
    
    xval = 0
    yval = 40
    error_lbl = tk.Label(win,
                         text = '',
                         bg = self.M.dflt_bg,
                         font = self.M.reg_font)
    for param in self.paramids:
      #reversing which thing is the key, ID vs paramName
      self.M.flip_dict(self.M.Param.parameter_name_dict)
      name = self.M.flipped_params[param[0]]
      
      # stop it from going off the page while placing
      if xval >= 480:
        xval = 0 
        yval= 150
      else:
        yval = yval
        
      # placing elements
      param_lbl = tk.Label(win,
                           text = name,
                           bg = self.M.dflt_bg,
                           font = self.M.reg_font)
      param_lbl.place(x=xval+20, y= yval)

      level_lbl = ttk.Label(win,
                          text = 'Level:',
                          background = self.M.dflt_bg,
                          font = self.M.reg_font)
      level_lbl.place(x=xval, y= yval+25)

      dosage_lbl = ttk.Label(win,
                          text = 'Dosage:',
                          background = self.M.dflt_bg,
                          font = self.M.reg_font)
      dosage_lbl.place(x=xval+40, y= yval+25)
      
      level_e = ttk.Entry(win, width = 4)
      level_e.place(x=xval, y= yval+45)
      self.__lvl_id_dict[param[0]] = level_e
      
      dosage_e = ttk.Entry(win, width = 4) 
      dosage_e.place(x=xval+45, y= yval+45)
      self.__dsg_id_dict[param[0]] = dosage_e #setting entry as value in dictionary
      
      xval = xval+120

    enter = ttk.Button(win,
                       text = 'enter',
                       style = self.M.dflt_btn,
                       width= 7,
                       command=lambda: self.M.G.get_values(self.paramids, self.M.tank_code, self.__dsg_id_dict, self.__lvl_id_dict, back_btn, error_lbl)) #calls get values passing in the dictionaries with entries 
    
    print(self.__dsg_id_dict, self.__lvl_id_dict)
    enter.place(x=0, y=250)
    back_btn.place(x=500, y=350)

    