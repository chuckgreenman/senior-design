import praw

class Reddit():
  def __init__(self):
    self.conn = praw.Reddit(client_id='hRv5efdLrLgCPA',
                     client_secret='uI4yR0qnC3UbZ_ibVSLKhIjCt7g',
                     user_agent='sockscatch')


