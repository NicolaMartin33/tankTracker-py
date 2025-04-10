import datetime as dt
from datetime import timedelta
from sqlite3 import OperationalError

from backend.config import connection_db, csr_object


class Configuration:

  def __init__(self):
    self.weekly_sent_last = {'weekly': (dt.date.today() - timedelta(days=7))} #sets last date to a week ago
    
    self.fortnight_sent_last =  {'fortnight': (dt.date.today() - timedelta(days=14))} #sets last date to a fortnight ago
    
    self.monthly_sent_last = {'monthly': (dt.date.today() - timedelta(days=30))} #sets last date to a month ago

  @classmethod #can be called outwith the class instance
  def create_tbl(cls):
    try:
      tblConfiguration = """CREATE TABLE configuration (
          configID INT PRIMARY KEY,
          weekly_sent_last TIMESTAMP,
          fortnight_sent_last TIMESTAMP,
          monthly_sent_last TIMESTAMP
      ); """

      csr_object.execute(tblConfiguration)  #maps class to db
      print('table configuration created')
    except OperationalError as e: #printing statement to show user table already exists
      
      print('table configuration was not made as it already exists')

  
  #saves the data into the table
   #only called on once to initalise
  def save(self):
    save_configuration = """
        INSERT INTO configuration (weekly_sent_last, fortnight_sent_last, monthly_sent_last)
        VALUES (?,?,?)
    """
    csr_object.execute(save_configuration, (self.weekly_sent_last['weekly'], self.fortnight_sent_last['fortnight'], self.monthly_sent_last['monthly'])) 
    connection_db.commit()
    
    #inserting









