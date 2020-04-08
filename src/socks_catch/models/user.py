import datetime
from itertools import chain

from utilities.reddit import Reddit
from utilities.db_interact import DbInteract
from models.activity import Activity

class User():
  def __init__(self, user_id):
    self.id = user_id

  def crawl(self):
    r = Reddit()
    db = DbInteract()
    user = r.conn.redditor(self.id)
    activity = []
    for comment in list(user.comments.new(limit=None)):
      activity.append(Activity(comment.subreddit_id, comment.author.id, 'comment', datetime.datetime.fromtimestamp(comment.created_utc).isoformat()))

    for submission in list(user.submissions.new(limit=None)):
      activity.append(Activity(submission.subreddit.id, submission.author.id, 'submission', datetime.datetime.fromtimestamp(submission.created_utc).isoformat()))
    
    db.add_activity_records(activity)

  def calculate_delay(self, user_name):
    self.pull_metadata(user_name)
  
  def pull_metadata(self):
    db = DbInteract()
    r = Reddit()
    try:
      print(self.id)
      if db.user_metadata_exists((self.id,)):
        return

      registrationTime = r.conn.redditor(self.id).created_utc
      comments = []
      oldest = None
      for comment in r.conn.redditor(self.id).comments.new(limit=None):
        comments.append(comment)
        if oldest == None or comment.created_utc < oldest:
          oldest = comment.created_utc

      submitted = []
      for submission in r.conn.redditor(self.id).submissions.new(limit=None):
        submitted.append(submission)
        if oldest == None or submission.created_utc < oldest:
          oldest = submission.created_utc

      comment_count = len(comments)
      submission_count = len(submitted)

      max_activity = False

      if comment_count == 1000 or submission_count == 1000:
        max_activity = True

      db.save_user_metadata((self.id, max_activity, registrationTime, oldest, oldest-registrationTime))
      print("Saved")
    except Exception as e: print(e)