import tkinter.ttk as ttk

from backend.config import csr_object, connection_db


class tank_page_buttons:
  def __init__(self, menu):
    self.M = menu
    
  #pulls all their tank names if no tanks are saved to their userid an error is placed
  def get_tank(self, next_function): #next_function lets you call an outside function 
    
    #placing elements
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

    heading.place(x=0, y=0)
    back.place(x=400, y=350)
    print(self.M.UserID)
    
    #gets all tank names for user
    query = 'SELECT name FROM tank WHERE UserID = ?'
    csr_object.execute(query, (self.M.UserID,))
    tanks = csr_object.fetchall()
    

    yval=[100]
    #if they have no tanks error is displayed
    if len(tanks) == 0:
      no_tank.place(x=300,y=200)
    else:
      for tank in tanks:
        print(tank[0])
        self.make_button(tank[0], win, yval, next_function) #for tank name in tanknames place a button
      win.mainloop()
    

  #create tank buttons
  def make_button(self, name, win, yaxis, next_function):
    print(f"Creating button '{name}' at Y Position = {yaxis}")
    button = ttk.Button(win,
                        text = name,
                        style = self.M.dflt_btn,
                        command=lambda name=name:  self.button_click(name, next_function)) 
    #name=name makes sure the value of name is the one captured at the time of definition

    button.place(x=100,y= yaxis[0])
    print(f"Placed button '{name}' at Y Position = {yaxis}") 
    yaxis[0] += 50 #places tank buttons further down the page each time

  #if button is clicked the passed necxt function is called
  def button_click(self, tank_name, next_function):
 
    query = 'SELECT tank_code FROM tank WHERE (UserID = ? AND name = ?)'
    csr_object.execute(query, (self.M.UserID, tank_name,))
    tankcode = csr_object.fetchone()
    
    self.M.tank_code = str(tankcode).strip('(,)') #sets tank code in menu file
    self.M.tank_name = tank_name #sets tank name in menu file
    next_function() #calls passed function
    