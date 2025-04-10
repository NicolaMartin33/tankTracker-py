import tkinter.ttk as ttk

import matplotlib.pyplot as plt
import numpy as np

from backend.config import csr_object, connection_db

class Graphing:
  def __init__(self, menu):
    self.M = menu
    self.param_names = [] #stores param names
    

  def make_graph(self, name, ID):
    dates, dosages, levels = self.get_graph_values(ID) #gets values for date, dosage, and level
    
    #dates need to be formatted as a string
    dates_list = [str(date) for date in dates]
    
#without conversion to list pulls up error but only way you can get it to convert is to first convert it to np.array
    levels_arr = np.array(levels)
    levels_list = levels_arr.tolist()
    dosages_arr = np.array(dosages) 
    dosages_list = dosages_arr.tolist()
    
    #setting up graph 
    plt.figure(figsize=(12, 8)) #graph size
    plt.plot(dates_list, dosages_list, marker= 'o', linestyle ='-', label = 'Dosage') #setting new line
    plt.plot(dates_list, levels_list, marker= 'x', linestyle = ':', label = 'Levels') #setting new line
    plt.xlabel('Time/Date') #x axis label
    plt.ylabel('Values') #y axis label
    plt.title(f'Dosage and Levels of {name} vs Time') #title of graph
    plt.grid(True) #show grid
    plt.legend() #displays labels
    plt.show() #show qraph

  def get_graph_values(self, ID):
    csr_object.execute(f'SELECT timestamp, dosage, level FROM graph WHERE (tank_code = {self.M.tank_code} AND ParameterID = {ID})')
    data = csr_object.fetchall() #row by row
    
    dates = [value[0] for value in data] #seperating columns in a row
    dosages = [value[1] for value in data] 
    levels = [value[2] for value in data]
    print(dates, dosages, levels)
    return dates, dosages, levels
    
    
  #places buttons for each parameter name to display their graph 
  def get_param_name(self):
    win = self.M.new_window()
    heading = ttk.Label(win,
                        text = 'Parameter Selection Page',
                        font = self.M.title_font,
                        background = self.M.dflt_bg)
    heading.place(x=0,y=0)
    
    back = ttk.Button(win,
                        text = 'back',
                        width = 10,
                        style = self.M.dflt_btn,
                        command=lambda : win.destroy()) 
    back.place(x=300, y=200)
    
    #putting variable assignments before the colon means the values at the time of assignment are passed rather than the value at time of click
    #list of select parameter ids
    self.M.LOG.get_params()
    paramids = self.M.LOG.paramids
    print(paramids)
    #flipped dict of param names and ids
    param_dict = self.M.flip_dict(self.M.Param.parameter_name_dict)
    #seperate names and ids
    for ID in paramids:
      self.param_names.append(param_dict[ID[0]])
    if bool(self.param_names) is True: #chechks it isnt empty
      xval =10
      yval =50
      for i, pname in enumerate(self.param_names): #i is the counter
        if xval >= 480: #making sure the button stay on the window
          xval=0
          yval = 150
        else:
          xval = xval
        button = ttk.Button(win,
                            text = pname,
                            width = 10,
                            style = self.M.dflt_btn,
                            command=lambda name = pname, ID = paramids[i][0]: self.make_graph(name, ID)) 
        #putting variable assignments before the colon means the values at the time of assignment are passed rather than the value at time of click
        button.place(x=xval, y=yval)
        xval += 120

    else:
      print('no values')
      
  #places buttons for each tank to let su know which tank the user wants to see the parameters' graph   
  def choose_tank(self):
    self.M.TPB.get_tank(self.get_param_name) 
      



  