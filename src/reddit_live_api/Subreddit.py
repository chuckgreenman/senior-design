from reddit_live_api.keys import getID, getSecret, getAgent
from reddit_live_api.Utils import scrub_text
import praw
import prawcore.exceptions
from bs4 import BeautifulSoup


class Subreddit:
    # Set up connection to Reddit and reference to subreddit
    def __init__(self, subreddit_name):
        self.ID = getID()
        self.secret = getSecret()
        self.agent = getAgent()
        self.subreddit_name = subreddit_name
        self.reddit = reddit = praw.Reddit(client_id= self.ID,
                         client_secret=self.secret,
                         user_agent=self.agent)
        self.subreddit = reddit.subreddit(self.subreddit_name)

    def get_description(self, format='plain'):
        html = self.subreddit.description_html
        if format == 'plain':
            soup = BeautifulSoup(html, "html.parser")
            return ''.join(soup.findAll(text=True))
        elif format == 'html':
            return html
        elif format == "md":
            return self.subreddit.description
        return 'description not found'

    def get_subscriber_count(self):
        return self.subreddit.subscribers

    ''' Recent activity
    '''
    def get_recent_comments(self, number=100):
        items = []
        for comment in self.subreddit.comments(limit=number):
            items = items + [comment.body]

    def get_recent_submission_titles(self):
        items = []
        for submission in self.subreddit.new():
            items = items + [submission.title]
        return items

    def get_recent_submission_text(self):
        items = []
        for submission in self.subreddit.new():
            items = items + [scrub_text(submission.selftext)]
        return items

    ''' Controversial submissions
    '''
    def get_controversial_submission_titles(self, time_period='week'):
        items = []
        for submission in self.subreddit.controversial(time_period):
            items = items + [submission.title]
        return items

    def get_controversial_submission_text(self, time_period='week'):
        items = []
        for submission in self.subreddit.controversial(time_period):
            items = items + [scrub_text(submission.selftext)]
        return items

    # TODO: banned users... could be interesting

    ''' Hot submissions
    '''
    def get_hot_submission_titles(self):
        items = []
        for submission in self.subreddit.hot():
            items = items + [submission.title]
        return items

    def get_hot_submission_text(self):
        items = []
        for submission in self.subreddit.hot():
            items = items + [scrub_text(submission.selftext)]
        return items

    def get_hot_submission_authors(self):
        items = []
        for submission in self.subreddit.hot():
            items = items + [scrub_text(submission.author.name)]
        return items

    ''' Top submissions
    '''
    def get_top_submission_titles(self, time='day'):
        items = []
        for submission in self.subreddit.top(time):
            items = items + [submission.title]
        return items

    def get_top_submission_text(self, time='day'):
        items = []
        for submission in self.subreddit.top(time):
            items = items + [scrub_text(submission.selftext)]
        return items

    def get_top_submission_authors(self, time='day'):
        items = []
        for submission in self.subreddit.top(time):
            items = items + [scrub_text(submission.author.name)]
        return items

    ''' Quarantined
    '''
    def get_is_quarantined(self):
        try:
            next(self.subreddit.hot())
            return False
        except prawcore.exceptions.Forbidden:
            return True

    # TODO: Search method could be useful but have to think about use case to implement properly.


sub = Subreddit('askReddit')
