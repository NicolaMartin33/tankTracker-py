import tkinter as tk
import tkinter.ttk as ttk

from backend.config import csr_object


class home: 
  def __init__(self, menu):
    self.M = menu

  def home_gui(self):
   
  #sign up window
    home_win = self.M.new_window()

  #get userid to display on homepage
  
    UserID = "{:04d}".format(int(self.M.UserID)) #displays in format 0000
    
  #creating labels
    
    heading = ttk.Label(home_win,
                        text = 'Home',
                        background = self.M.dflt_bg,
                        font = self.M.title_font)
    
    useridlbl = ttk.Label(home_win,
                          text = 'USER: '+ UserID,
                          background = self.M.dflt_bg,
                          font = self.M.lbl_font)
  #creating buttons
    logout = tk.Button(home_win,
                        text = 'Log Out',
                        bg = '#96B2C1',
                        width= 6,
                        command=lambda: [home_win.destroy(), self.M.L.login_gui()]) #destroys home window and then calls login window
    
    log = tk.Button(home_win,
                    text = 'Log Values',
                    bg = self.M.tk_bg,
                    width= 25,
                    command=lambda: self.M.LOG.choose_tank()) #calls log_values files choose_tank function
    
    create_tank = tk.Button(home_win,
                            text = 'Create New Tank',
                            bg = self.M.tk_bg,
                            width= 25,
                            command= lambda:
                            self.M.T.new_tank_page()) #lets you make a new tank
    
    common_qs = tk.Button(home_win,
                          text = 'Common Questions',
                          bg = self.M.tk_bg,
                          width= 25,
                          command=lambda: self.M.QD.question_gui()) #displays common questions
    
    settings = tk.Button(home_win,
                          text = 'Settings',
                          bg= self.M.tk_bg,
                          width= 25,
                          command=lambda: self.M.set.mainpage_gui()) #opens settings page

    graphs = tk.Button(home_win,
                       text = 'Display Graphs',
                       bg= self.M.tk_bg,
                       width= 25,
                       command=lambda: self.M.GING.choose_tank()) #calls log_values choose_tank func
    
    
    #placing elements
    heading.place(x=0, y=1)
    useridlbl.place(x=490, y=1)
    logout.place(x=500, y=350)
    log.place(x=100, y=99)
    create_tank.place(x=100, y=140)
    common_qs.place(x=100, y=180)
    graphs.place(x=100, y=220)
    settings.place(x=100, y=260)
    tk.mainloop()
    
    
    