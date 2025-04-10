
import tkinter as tk
import tkinter.ttk as ttk


class parameter_set:
  def __init__(self, menu):
    self.M = menu
    
  #lets user checkbox which parameters they would like to track and set upper and lower boundaries for them
  def parameter_gui(self):
    
    #creating window
    param_win = self.M.new_window()
    tankcode = self.M.TL.tankcode
    #labels
    heading = ttk.Label(param_win,
                        text = 'Select Parameters',
                        background = self.M.dflt_bg,
                        font = self.M.title_font)
    
    title = ttk.Label(param_win,
                      text = 'Set the upper and lower bounds of your chosen parameters:',
                      background = self.M.dflt_bg,
                      font = self.M.reg_font)
    #entries
    UB_calcium = ttk.Entry(param_win, width = 8)
    LB_calcium = ttk.Entry(param_win, width = 8)

    UB_alk= ttk.Entry(param_win, width = 8)
    LB_alk = ttk.Entry(param_win, width = 8)

    UB_mag = ttk.Entry(param_win, width = 8)
    LB_mag = ttk.Entry(param_win, width = 8)

    UB_am = ttk.Entry(param_win, width = 8)
    LB_am = ttk.Entry(param_win, width = 8)

    UB_rate = ttk.Entry(param_win, width = 8)
    LB_rate = ttk.Entry(param_win, width = 8)

    UB_rite = ttk.Entry(param_win, width = 8)
    LB_rite = ttk.Entry(param_win, width = 8)

    UB_ph = ttk.Entry(param_win, width = 8)
    LB_ph = ttk.Entry(param_win, width = 8)
    
    #checkboxes
    cvar = tk.IntVar(param_win) #holds 1 or 0 dependent on if it is clicked or not, 1 for clicked
    calcium_ck = tk.Checkbutton(param_win,
                                 text = 'Calcium Levels',
                                 bg = self.M.dflt_bg, 
                                 font = self.M.reg_font,
                                 variable= cvar)
    
    alkvar = tk.IntVar(param_win)
    alkalinity_ck= tk.Checkbutton(param_win,
                                text = 'Alkalinity Levels',
                                bg = self.M.dflt_bg,
                                font = self.M.reg_font,
                                variable= alkvar)

    mgvar = tk.IntVar(param_win) 
    magnesium_ck = tk.Checkbutton(param_win,
                                  text = 'Magnesium Levels',
                                  background = self.M.dflt_bg,
                                  font = self.M.reg_font,
                                  variable= mgvar)

    amvar = tk.IntVar(param_win)
    ammonia_ck = tk.Checkbutton(param_win,
                                text = 'Ammonia Levels',
                                background = self.M.dflt_bg,
                                font = self.M.reg_font,
                                variable= amvar)

    atevar = tk.IntVar(param_win)
    nitrate_ck = tk.Checkbutton(param_win,
                                text = 'Nitrate Levels',
                                background = self.M.dflt_bg,
                                font = self.M.reg_font,
                                variable= atevar)
    
    itevar = tk.IntVar(param_win)
    nitrite_ck = tk.Checkbutton(param_win,
                                text = 'Nitrite Levels',
                                background = self.M.dflt_bg,
                                font = self.M.reg_font,
                                variable= itevar)

    phvar =tk.IntVar(param_win)
    pH_ck = tk.Checkbutton(param_win,
                           text = 'pH Levels',
                           background = self.M.dflt_bg,
                           font = self.M.reg_font,
                           variable = phvar)

    #validating the params and saving them
    choose = ttk.Button(param_win,
      text = 'Choose',
      style = self.M.dflt_btn,
      width= 7,
      command=lambda: self.M.V.param_selection(param_win, tankcode, cvar.get(), alkvar.get(),
                                                mgvar.get(), amvar.get(), atevar.get(),
                                                itevar.get(), phvar.get(),
                                                UB_calcium.get(), UB_alk.get(),
                                                UB_mag.get(), UB_am.get(),
                                                UB_rate.get(), UB_rite.get(),
                                                UB_ph.get(), LB_calcium.get(),
                                                LB_alk.get(), LB_mag.get(),
                                                LB_am.get(), LB_rate.get(),
                                                LB_rite.get(), LB_ph.get()
                                              )) 
    
    #placing elements
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

    
    choose.place(x=0, y=250)
    
  
    