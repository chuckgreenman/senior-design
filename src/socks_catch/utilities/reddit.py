import praw
import keys

class Reddit():
  def __init__(self):
    self.conn = praw.Reddit(client_id=keys.getID(),
                            client_secret=keys.getSecret(),
                            user_agent='sockscatch')
