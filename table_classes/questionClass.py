from sqlite3 import OperationalError

from backend.config import connection_db, csr_object


class Question:
  def __init__(self):
    pass


  @classmethod #can be called outwith the class instance
  def create_tbl(cls):
    try:
      tblQuestion = """
          CREATE TABLE question (
              answerID INTEGER PRIMARY KEY,
              question_text VARCHAR(255) NOT NULL,
              title VARCHAR(25) NOT NULL,
              url TEXT NOT NULL,
              score INT NOT NULL
          ); """

      csr_object.execute(tblQuestion) #maps class to db
      print('table question created')
      connection_db.commit()
      

    except OperationalError: #printing statement to show user table already exists
      print('table question was not made as it already exists')

  def save(self, question, title, url, score): #saving entries
    try:
      save_user = """
          INSERT INTO question (question_text, title, url, score)
          VALUES (?,?,?,?)
      """
      csr_object.execute(save_user,(question,
                                    title,
                                    url,
                                    score))
      connection_db.commit()
      
      #inserting
      return True
    except Exception as e:
      print()
      print('there was an error', e) # describes error
      return False