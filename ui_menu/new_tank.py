import tkinter.ttk as ttk



class tank:
  def __init__(self, menu):
    self.M = menu

  #lest user make a new tank setting the dimensions of it
  def new_tank_page(self):
    

    tank_win = self.M.new_window()
    

  #labels
    heading = ttk.Label(tank_win,
                        text = 'Create Tank',
                        background = self.M.dflt_bg,
                        font = self.M.title_font)

    capac_lbl = ttk.Label(tank_win,
                          text = "Enter your Tank's capacity (L cubed):",
                          background = self.M.dflt_bg,
                          font = self.M.reg_font)
    
    FishNo_lbl = ttk.Label(tank_win,
                            text = 'Enter the number of fish:', 
                            background = self.M.dflt_bg,
                            font = self.M.reg_font)
    
    length_lbl = ttk.Label(tank_win,
                            text = 'Enter the length of your tank (cm):',
                            background = self.M.dflt_bg,
                            font = self.M.reg_font)
    
    depth_lbl = ttk.Label(tank_win,
                      text = 'Enter the depth of your tank (cm):',
                      background = self.M.dflt_bg,
                      font = self.M.reg_font)

    width_lbl = ttk.Label(tank_win,
                      text = 'Enter the width of your tank (cm):',
                      background = self.M.dflt_bg,
                      font = self.M.reg_font)
    name_lbl = ttk.Label(tank_win,
                         text = 'Enter the name of your tank:',
                         background = self.M.dflt_bg,
                         font = self.M.reg_font)
    
    error_lbl = ttk.Label(tank_win,
                          text = "Please only enter numbers!",
                          background = self.M.dflt_bg,
                          font = self.M.reg_font)
    
  #entries
    capacity = ttk.Entry(tank_win, width = 25)
    NumFish = ttk.Entry(tank_win, width = 25)
    length = ttk.Entry(tank_win, width = 25)
    depth = ttk.Entry(tank_win, width = 25)
    width = ttk.Entry(tank_win, width = 25)  
    name = ttk.Entry(tank_win, width = 25)

    back = ttk.Button(tank_win,
                      text = 'back to log in page',
                      style = self.M.dflt_btn,
                      width= 4,
                      command=lambda:
                      tank_win.destroy()) # back to home page

    next = ttk.Button(tank_win,
                      text = 'Next >',
                      style = self.M.dflt_btn,
                      width= 4,
                      command=lambda: self.M.V.tank_validation( capacity, NumFish, length, depth, width, name, error_lbl, tank_win)) #validates their entries 
    
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
    next.place(x=140, y=265)

    
 
    
  