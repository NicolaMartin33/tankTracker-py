
from backend.classinitialisesql import init_sql
from backend.config import csr_object,connection_db
from ui_menu.menu import menu
#importing classes for the tables from folder table_classes
from table_classes.configurationClass import Configuration
from table_classes.graphClass import Graph
from table_classes.parameter_SelectionClass import Parameter_Selection
from table_classes.parametersClass import Parameters
from table_classes.questionClass import Question
from table_classes.tankClass import Tanktbl
from table_classes.userClass import User


def create_tables():
  init_sql() #creating database
  csr_object.execute("DROP TABLE parameters") #so that parameter dict is newly made each time
  Configuration.create_tbl() #creating table configuration
  Question.create_tbl() #creating table question
  Graph.create_tbl() #creating table graph
  User.create_tbl() #creating table user
  Parameters.create_tbl() #creating table parameters
  Tanktbl.create_tbl() #creating table tank
  Parameter_Selection.create_tbl() #creating table parameter type
  

create_tables() #makes tables


m = menu() #instance of menu class
m.startup() #calls start up method from menu


