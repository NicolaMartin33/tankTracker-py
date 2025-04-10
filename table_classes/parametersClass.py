from collections import deque
from sqlite3 import OperationalError

from backend.config import connection_db, csr_object


class Parameters:
  parameterqueue = deque(['calcium', 'magnesium', 'alkalinity',
                   'ammonia', 'nitrate', 'nitrite', 'pH'])
  parameter_name_dict = {}
  #example param timings
  frequency_dict ={
    'calcium' : 'weekly',
    'magnesium' : 'weekly',
    'alkalinity' : 'monthly',
    'ammonia' : 'weekly',
    'nitrate' : 'fortnight',
    'nitrite' : 'weekly',
    'pH' : 'weekly'
  } 
  #set articles for table insertion
  LBarticle_dict = {
    'calcium' : 'https://www.reef2reef.com/threads/any-tips-for-lowering-calcium-in-your-aquarium-rapidly.175296/',
    'magnesium' : 'https://www.reef2reef.com/threads/any-way-to-reduce-magnesium.298115/',
    'alkalinity' : 'https://www.reddit.com/r/Aquariums/comments/onlljf/how_do_i_lower_ph_hardness_and_alkalinity_levels/',
    'ammonia' : 'https://www.birdexoticsvet.com.au/fishamphibians/2020/6/9/treating-ammonia-toxicity-in-an-aquarium-or-fish-pond',
    'nitrate' : 'https://www.thesprucepets.com/reduce-high-toxic-nitrates-efficiently-2925185',
    'nitrite' : 'https://aquariumstoredepot.com/blogs/news/how-to-lower-nitrites-in-fish-tank',
    'pH' : 'https://www.reddit.com/r/Aquariums/comments/onlljf/how_do_i_lower_ph_hardness_and_alkalinity_levels/'
  }
  #sets lower bound articles
  UBarticle_dict = {
    'calcium' : 'https://www.ultimatereef.net/threads/help-with-raising-calcium.894075/',
    'magnesium' : 'https://www.reef2reef.com/threads/how-to-raise-magnesium.229925/',
    'alkalinity' : 'https://atlas-scientific.com/blog/how-to-lower-alkalinity-without-lowering-ph/',
    'ammonia' : 'https://www.freshwatersystems.com/blogs/blog/how-to-cycle-a-fish-tank',
    'nitrate' : 'fortnight',
    'nitrite' : 'https://www.quora.com/How-do-I-quickly-increase-my-nitrate-levels-in-my-aquarium-It-s-a-new-tank-and-I-currently-have-a-few-fish-that-are-doing-well-but-my-nitrate-levels-are-reading-as-very-low-Also-the-water-is-very-alkaline-How-doI',
    'pH' : 'https://aquaforest.eu/en/articles/how-to-raise-ph-in-aquarium/'
  }


    
  def __init__(self):
    self.freq = None
    self.param_name = None
    
#creates table
  @classmethod #can be called outwith the class instance
  def create_tbl(cls):
    try:
      tblParameters = """ CREATE TABLE parameters(
          ParameterID INTEGER PRIMARY KEY,
          ParameterName CHAR(25) NOT NULL,
          Frequency CHAR(25),
          Upper_web VARCHAR(255),
          Lower_web VARCHAR(255)
      ); """

      csr_object.execute(tblParameters)  #maps class to db
      print('table Parameters created')
      connection_db.commit()
    except OperationalError: #printing statement to show user that table already exists
      print('table Parameters was not made as it already exists')
  #saves the data into the table
      
  
  def save(self):
    try:
      save_parameters = """
          INSERT INTO parameters (ParameterName, Frequency, Upper_web, Lower_web )
          VALUES (?,?,?,?)
      """
      paramQ = deque.copy(self.parameterqueue)
      while bool(paramQ) is True:
        self.param_name = paramQ.popleft()
        self.freq = self.frequency_dict[self.param_name]
        #upper boundary website
        ub_web = self.UBarticle_dict[self.param_name]
        #lower boundary website
        lb_web = self.LBarticle_dict[self.param_name]
        #saving to table
        csr_object.execute(save_parameters,(self.param_name, self.freq, ub_web, lb_web)) 
        #inserts the parameter name and its corresponding id into a dictionary
        self.parameter_name_dict[self.param_name] = csr_object.lastrowid
        connection_db.commit()
      return self.parameter_name_dict
    except Exception as e:
      print(f'error occurred: {e}')