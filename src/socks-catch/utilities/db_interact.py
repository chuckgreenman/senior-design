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
      for activity in activities:
        print("Insert!")
        c.execute("INSERT INTO activity (subreddit_id, user_id, type, occurred) VALUES (?,?,?,?);", (activity.subreddit_id, activity.user_id, activity.type, activity.occured))
      self.connection.commit()
      