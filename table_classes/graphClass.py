import datetime as dt
from sqlite3 import OperationalError

from backend.config import connection_db, csr_object


class Graph:
  def __init__(self, menu):
    self.M = menu


  @classmethod #can be called outwith the class instance
  def create_tbl(cls):
    try:
      tblGraph = """
          CREATE TABLE graph (
              graphID INT PRIMARY KEY,
              ParameterID INT,
              tank_code INT,
              timestamp DATE,
              dosage INT,
              level INT,
              FOREIGN KEY (tank_code) REFERENCES tank(tank_code),
              FOREIGN KEY (ParameterID) REFERENCES parameters(ParameterID)
          ); """

      csr_object.execute(tblGraph) #maps class to db
      print('table graph created')
      connection_db.commit()
      

    except OperationalError: #printing statement to show user table already exists
      print('table graph was not made as it already exists')

  def get_values(self, paramIDs, tankcode, dosage_dict, level_dict, back_btn,lbl): 
    back_btn.place(x=500, y=350)
    date = dt.date.today() #retrieves todays date 
    valid = True
    try:
      for id in paramIDs: #setting each variable
        ParamID = id[0]
        dosage = dosage_dict[id[0]]
        level  = level_dict[id[0]]
        print(ParamID, tankcode, date, dosage.get(), level.get())
    
        #if entry is empty ('') or not a number/decimal, it will not be saved to the table
        try:
          if dosage.get() == ''  or not float(dosage.get()) or \
              level.get() == '' or not float(level.get()) : 
            valid = False
            print(f'no valid values to save for {self.M.flipped_params[id[0]]}')
        except ValueError:
          print(f'no valid values to save for {self.M.flipped_params[id[0]]}')
          valid = False
          lbl.config('no valid values entered')
          lbl.place(x=50, y=300)

          
        if valid is True: #if entries are valid
          if self.save(ParamID, tankcode, date, dosage.get(), level.get()) is True:
            print('saved succesfully')
            lbl.forget()
            lbl.config(text= 'save was successful')
            lbl.place(x=50, y=300)
      self.M.LOG.param_emails(level_dict) #checks values against parameter boundaries
    
    except Exception as e: #places error label and returns the error emsssage
      print(f'error occured: {e}')
      lbl.forget()
      lbl.config(text = 'an error occured, please recheck you have only entered numbers')
      lbl.place(x=50, y=300)

  #saves details
  def save(self, paramID, tankcode, date, dosage, level):
    try:
      #saving values into table graph
      save_log = """
          INSERT INTO graph (ParameterID, tank_code, timestamp, dosage, level)
          VALUES (?,?,?,?,?)
      """
      csr_object.execute(save_log,(paramID,
                                   tankcode,
                                   date,
                                   dosage,
                                   level))
      connection_db.commit()
      print('worked')
      #inserting
      return True
    except Exception as e:
      print()
      print(f'there was an error: {e}') # describes error
      return False