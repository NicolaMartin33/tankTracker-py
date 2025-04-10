from sqlite3 import OperationalError

from backend.config import csr_object, connection_db


#class that maps to a table in the database
class Tanktbl:
  def __init__(self):
    self._tankcode = None
    self._userID = None
    self._Capacity = None
    self._NumFish = None
    self._Length = None
    self._Depth = None
    self._Width = None
    self._Name = None

  @classmethod #can be called outwith an instance being made
  def create_tbl(cls):
    try:
      tblTank = """ CREATE TABLE tank(
          tank_code INTEGER PRIMARY KEY,
          UserID INT,
          capacity INT NOT NULL,
          numfish INT NOT NULL,
          length INT NOT NULL,
          depth INT NOT NULL,
          width INT NOT NULL,
          name VARCHAR(25) NOT NULL,
          FOREIGN KEY (UserID) REFERENCES user(UserID)
      ); """
      
      csr_object.execute(tblTank) #maps class to db
      connection_db.commit()
      
      print('table tank created')
      
    except OperationalError: #printing statement to show user table already exists
      print('table tank was not made as it already exists')

  def set_capacity(self, capacity):
    valid_cap = False
    try:
      self.Capacity = capacity.get()
      valid_cap = self.Capacity.isdigit()
    except Exception as e:
      print(e)
    return valid_cap

  def set_NumFish(self, fishnum):
    valid_fish = False
    try:
      self.NumFish = fishnum.get()
      valid_fish = self.NumFish.isdigit()
    except Exception as e:
      print(e)
    return valid_fish
    
  def set_length(self, len):
    valid_len = False
    try:
      self.Length = len.get()
      valid_len = self.Length.isdigit()
    except Exception as e:
      print(e)
    return valid_len

  def set_depth(self, dep):
    valid_dep = False
    try:
      self.Depth = dep.get()
      valid_dep = self.Depth.isdigit()
    except Exception as e:
      print(e)
    return valid_dep

  def set_width(self, width):
    valid_wid = False
    try:
      self.Width = width.get()
      valid_wid = self.Width.isdigit()
    except Exception as e:
      print(e)
    return valid_wid

  def set_name(self, name):
    try:
      self.Name = name.get()
      print(self.Name)
    except Exception as e:
      print(e)
    
  #saves the data into the table    
  def save(self, userID): 
    try:
      
    
      save_tank = """
          INSERT INTO tank (UserID, capacity, numfish, length, depth, width, name)
          VALUES (?,?,?,?,?,?,?)
      """
      csr_object.execute(save_tank, (userID, 
                                     self.Capacity,
                                     self.NumFish,
                                     self.Length,
                                     self.Depth,
                                     self.Width,
                                     self.Name))
      
      self.tankcode = csr_object.lastrowid
      connection_db.commit()
      
      return True
    except Exception as e: #if save fails
      print()
      print('there was an error', e)
      return False

