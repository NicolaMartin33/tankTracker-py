import sqlite3


class init_sql:
  def __init__(self):
    pass
  
    def initialise_SQL():
      try:
    
        # connecting to fish database
        import_sql = sqlite3.connect('fishfundamentals.db')
        csr = import_sql.cursor()
        print('DB Init')
    
        qry = 'select sqlite_version();'
        csr.execute(qry)
    
        # output variable fetches the result and stores it
        output = csr.fetchall()
        print('SQLite Version is {}'.format(output))
    
        # close the cursor in database
        csr.close()
    
      except sqlite3.Error as error:
        print('There has been an error: ', error)
    
      finally:
    
        if import_sql is True:
          import_sql.close()
          print('connection to sqlite3 has been closed')

    initialise_SQL()
      