from sqlite3 import OperationalError

from backend.config import csr_object, connection_db


#class that maps to a table in the database
class Parameter_Selection:
  def __init__(self):
    pass

  @classmethod #can be called outwith the class instance
  def create_tbl(cls):
    try:
      tblParameter_Selection = """
          CREATE TABLE parameterSelection (
              ParameterSelectionID INT PRIMARY KEY,
              ParameterID INT, 
              tank_code INT,
              is_Selected INT,
              upperBound INT,
              lowerBound INT,
              FOREIGN KEY (tank_code) REFERENCES tank(tank_code),
              FOREIGN KEY (ParameterID) REFERENCES parameters(ParameterID)
          ); """
      
      csr_object.execute(tblParameter_Selection) #maps class to db
      print('table parameter_Selection created')
      
    except OperationalError: #printing statement to show user table already exists
      print('table parameter_selection was not made as it already exists')
    
  #saves the data into the table    
  def save(self, pID, tankCD, pBool, UB, LB): 
    try:
      if UB.isalpha() is True or LB.isalpha() is True:
        print('Boundaries are not valid entries')
        return False
      else:
        save_param = """
            INSERT INTO parameterSelection (ParameterID, tank_code, is_Selected, upperBound, lowerBound)
            VALUES (?,?,?,?,?)
        """
        csr_object.execute(save_param, (pID,
                                        tankCD,
                                        pBool, UB, LB)) #inserting
        connection_db.commit()
        
        print(pID, tankCD, pBool)
        return True
    except Exception as e: #if there is an error, error message is returned
      print()
      print('there was an error', e)
      return False