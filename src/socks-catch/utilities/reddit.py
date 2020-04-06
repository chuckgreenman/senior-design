import praw

class Reddit():
  def __init__(self):
    self.conn = praw.Reddit(client_id='Pn4vT2vccae0GA',
                     client_secret='',
                     user_agent='sockscatch')


