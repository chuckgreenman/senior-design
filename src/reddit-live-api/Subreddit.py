import praw
import prawcore.exceptions
from keys import getID, getSecret, getAgent
from bs4 import BeautifulSoup
from Utils import scrub_text, SubmissionType


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

    # This method checks that a subreddit exists and is not quarantined. Note: we are currently not
    # supporting the analysis of quarantined subreddits due to potential issues this may cause.
    def check_subreddit_valid(self):
        try:
            test = self.subreddit.id
            return True
        except prawcore.exceptions.Redirect:
            return False
        except prawcore.exceptions.Forbidden:
            return False

    def get_description(self, format='plain'):
        try:
            html = self.subreddit.description_html
        except prawcore.exceptions.NotFound:
            print('Encountered an error trying to obtain subreddit description. Subreddit not found.')
            return 'Description not found'
        if format == 'plain':
            soup = BeautifulSoup(html, "html.parser")
            return ''.join(soup.findAll(text=True))
        elif format == 'html':
            return html
        elif format == 'md':
            return self.subreddit.description
        return 'Description not found'

    def get_subscriber_count(self):
        try:
            return self.subreddit.subscribers
        except prawcore.exceptions.NotFound:
            print('Encountered an error trying to obtain subreddit subscriber count. Subreddit not found.')
            return -1

    ''' Recent activity
    '''
    def get_recent_comments(self, number=100):
        items = []
        try:
            for comment in self.subreddit.comments(limit=number):
                items = items + [scrub_text(comment.body)]
        except prawcore.exceptions.NotFound:
            print('Encountered an error trying to obtain recent comments. Subreddit not found.')
        except prawcore.exceptions.Forbidden:
            print('Encountered an error trying to obtain recent comments. Access is forbidden.')
        return items

    def get_recent_submission_titles(self):
        items = []
        try:
            for submission in self.subreddit.new():
                items = items + [scrub_text(submission.title)]
        except prawcore.exceptions.NotFound:
            print('Encountered an error trying to obtain recent submission titles. Subreddit not found.')
        except prawcore.exceptions.Forbidden:
            print('Encountered an error trying to obtain recent submission titles. Access is forbidden.')
        return items

    def get_recent_submission_text(self):
        items = []
        try:
            for submission in self.subreddit.new():
                items = items + [scrub_text(submission.selftext)]
        except prawcore.exceptions.NotFound:
            print('Encountered an error trying to obtain recent submission text. Subreddit not found.')
        except prawcore.exceptions.Forbidden:
            print('Encountered an error trying to obtain recent submission text. Access is forbidden.')
        return items

    ''' Controversial submissions
    '''
    def get_controversial_submission_titles(self, time_period='week'):
        items = []
        try:
            for submission in self.subreddit.controversial(time_period):
                items = items + [scrub_text(submission.title)]
        except prawcore.exceptions.NotFound:
            print('Encountered an error trying to obtain controversial submission titles. Subreddit not found.')
        except prawcore.exceptions.Forbidden:
            print('Encountered an error trying to obtain controversial submission titles. Access is forbidden.')
        return items

    def get_controversial_submission_text(self, time_period='week'):
        items = []
        try:
            for submission in self.subreddit.controversial(time_period):
                items = items + [scrub_text(submission.selftext)]
        except prawcore.exceptions.NotFound:
            print('Encountered an error trying to obtain controversial submission text. Subreddit not found.')
        except prawcore.exceptions.Forbidden:
            print('Encountered an error trying to obtain controversial submission text. Access is forbidden.')
        return items

    # TODO: banned users... could be interesting

    ''' Hot submissions
    '''
    def get_hot_submission_titles(self):
        items = []
        try:
            for submission in self.subreddit.hot():
                items = items + [scrub_text(submission.title)]
        except prawcore.exceptions.NotFound:
            print('Encountered an error trying to obtain hot submission titles. Subreddit not found.')
        except prawcore.exceptions.Forbidden:
            print('Encountered an error trying to obtain hot submission titles. Access is forbidden.')
        return items

    def get_hot_submission_text(self):
        items = []
        try:
            for submission in self.subreddit.hot():
                items = items + [scrub_text(submission.selftext)]
        except prawcore.exceptions.NotFound:
            print('Encountered an error trying to obtain hot submission text. Subreddit not found.')
        except prawcore.exceptions.Forbidden:
            print('Encountered an error trying to obtain hot submission text. Access is forbidden.')
        return items

    ''' Top submissions
    '''
    def get_top_submission_titles(self, time='day'):
        items = []
        try:
            for submission in self.subreddit.top(time):
                items = items + [scrub_text(submission.title)]
        except prawcore.exceptions.NotFound:
            print('Encountered an error trying to obtain top submission titles. Subreddit not found.')
        except prawcore.exceptions.Forbidden:
            print('Encountered an error trying to obtain top submission titles. Access is forbidden.')
        return items

    def get_top_submission_text(self, time='day'):
        items = []
        try:
            for submission in self.subreddit.top(time):
                items = items + [scrub_text(submission.selftext)]
        except prawcore.exceptions.NotFound:
            print('Encountered an error trying to obtain top submission text. Subreddit not found.')
        except prawcore.exceptions.Forbidden:
            print('Encountered an error trying to obtain top submission text. Access is forbidden.')
        return items

    ''' General submissions
    '''
    def get_submissions(self, sub_type=SubmissionType.NEW, time='week'):
        items = []
        submissions = []
        try:
            if sub_type == SubmissionType.NEW:
                submissions = self.subreddit.new()
            elif sub_type == SubmissionType.TOP:
                submissions = self.subreddit.top(time)
            elif sub_type == SubmissionType.HOT:
                submissions = self.subreddit.hot()
            elif sub_type == SubmissionType.CONTROVERSIAL:
                submissions = self.subreddit.controversial(time)
        except prawcore.exceptions.NotFound:
            print('Encountered an error trying to obtain submissions. Subreddit not found.')
        except prawcore.exceptions.Forbidden:
            print('Encountered an error trying to obtain submissions. Access is forbidden.')

        for submission in submissions:
            items = items + [submission]

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