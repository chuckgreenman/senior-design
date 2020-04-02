import os
import sqlite3

class DbInteract:
  def __init__(self, environment='development'):
    if environment == 'development':
      self.connection = sqlite3.connect(os.path.join("development.db"))
      self.environment = environment
    else:
      raise Exception("Unrecognized enviroment variable.")

  # Add activity record will add an activity record to the
  # database if it is not already recorded 
  def add_activity_records(self, activities):
    if self.environment == 'development':
      c = self.connection.cursor()
      c.executemany("INSERT INTO activity (page_id, subreddit, user, type, occurred) VALUES (?,?,?,?,?);", activities)
      self.connection.commit()
      