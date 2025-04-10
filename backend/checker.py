from config import connection_db, csr_object


def get_users():
  with connection_db: #with means the connection is def closed after execution
      csr_object.execute("SELECT * FROM user ")
      print(csr_object.fetchall()) #fetches all data from user
get_users()

def get_tanks():
  with connection_db: #with means the connection is def closed after execution
      csr_object.execute("SELECT * FROM tank")
      print(csr_object.fetchall()) #fetches all data from tank
get_tanks()

def get_params():
  with connection_db: #with means the connection is def closed after execution
    csr_object.execute("SELECT * FROM parameterSelection")
    print(csr_object.fetchall()) #fetches all data from parameterSelection
    print('hi')
get_params()

def get_graph():
  with connection_db: #with means the connection is def closed after execution
    csr_object.execute("SELECT * FROM graph")
    print(csr_object.fetchall()) #fetches all data from graph
get_graph()

def get_question():
  with connection_db: #with means the connection is def closed after execution
    csr_object.execute("SELECT * FROM question")
    print(csr_object.fetchall()) #fetches all data from question
get_question()


