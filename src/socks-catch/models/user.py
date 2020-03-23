import datetime

from utilities.reddit import Reddit
from utilities.db_interact import DbInteract
from models.activity import Activity

class User():
  def __init__(self, user_id):
    print('init user')
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
