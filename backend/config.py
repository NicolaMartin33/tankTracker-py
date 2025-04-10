import sqlite3

#connecting to db 
connection_db = sqlite3.connect('fishfundamentals.db') 

#setting cursor 
csr_object = connection_db.cursor()

