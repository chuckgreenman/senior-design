import os
import sqlite3

class DbSetup():
  def __init__(self, environment):
    if environment == 'production':
      print("Can't set up for production yet!")
    elif environment == 'development':
      self.setup_in_development()
    else:
      raise Exception("Unrecognized environment variable.")

  def setup_in_development(self):
    sqlite_conn = sqlite3.connect(os.path.join("development.db"));
    sqlite_curs = sqlite_conn.cursor()

    for file in os.listdir(os.path.join("sql", "table_creation")):
      with open(os.path.join("sql", "table_creation", file), 'r') as file_obj:
        query = file_obj.read().replace('\n', '')
        sqlite_curs.execute(query)

    print("Configured development.db")

dbs = DbSetup("development")
