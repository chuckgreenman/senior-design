import praw
import prawcore.exceptions
from reddit_live_api.keys import getID, getSecret, getAgent
from bs4 import BeautifulSoup
from reddit_live_api.Utils import scrub_text, SubmissionType, TimeFrame, SubmissionAttribute, remove_stopwords, rank_items
import wordcloud
import matplotlib.pyplot as plt


class Subreddit:
    # Set up connection to Reddit and reference to subreddit
    def __init__(self, subreddit_name):
        self.ID = getID()
        self.secret = getSecret()
        self.agent = getAgent()
        self.subreddit_name = subreddit_name
        self.reddit = praw.Reddit(client_id=self.ID,
                                  client_secret=self.secret,
                                  user_agent=self.agent)
        self.subreddit = self.reddit.subreddit(self.subreddit_name)

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
    def get_comments(self, number=100):
        items = []
        try:
            for comment in self.subreddit.comments(limit=number):
                items = items + [comment]
        except prawcore.exceptions.NotFound:
            print('Encountered an error trying to obtain recent comments. Subreddit not found.')
        except prawcore.exceptions.Forbidden:
            print('Encountered an error trying to obtain recent comments. Access is forbidden.')
        return items

    # TODO: banned users... could be interesting

    ''' Submission attributes
    '''
    def get_submission_titles(self, sub_type=SubmissionType.TOP, time=TimeFrame.WEEK):
        items = []
        submissions = self.get_submissions(sub_type, time)
        for submission in submissions:
            items = items + [scrub_text(submission.title)]
        return items

    def get_submission_text(self, sub_type=SubmissionType.TOP, time=TimeFrame.WEEK):
        items = []
        submissions = self.get_submissions(sub_type, time)
        for submission in submissions:
            items = items + [scrub_text(submission.selftext)]
        return items

    def get_submission_authors(self, sub_type=SubmissionType.TOP, time=TimeFrame.WEEK):
        items = []
        submissions = self.get_submissions(sub_type, time)
        for submission in submissions:
            if submission.author is None:
                print("Encountered an error with getting submission author's name.")
            else:
                items = items + [submission.author.name]
        return items

    def get_submission_comments(self, sub_type=SubmissionType.TOP, time=TimeFrame.WEEK, comment_limit=15):
        items = []
        submissions = self.get_submissions(sub_type, time)
        for submission in submissions:
            submission.comment_limit = comment_limit
            submission.comments.replace_more(limit=0)
            items = items + [submission.comments.list()]
        return items

    ''' General submissions
    '''
    def get_submissions(self, sub_type=SubmissionType.NEW, time=TimeFrame.WEEK):
        items = []
        submissions = []
        try:
            if sub_type == SubmissionType.NEW:
                submissions = self.subreddit.new()
            elif sub_type == SubmissionType.TOP:
                submissions = self.subreddit.top(time.name.lower())
            elif sub_type == SubmissionType.HOT:
                submissions = self.subreddit.hot()
            elif sub_type == SubmissionType.CONTROVERSIAL:
                submissions = self.subreddit.controversial(time.name.lower())
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

    ''' Word analysis
    '''
    def get_popular_words(self, limit=10, sub_type=SubmissionType.NEW, time=TimeFrame.WEEK, attribute=SubmissionAttribute.TITLE):
        if attribute == SubmissionAttribute.TITLE:
            sentences = self.get_submission_titles(sub_type, time)
        elif attribute == SubmissionAttribute.TEXT:
            sentences = self.get_submission_text(sub_type, time)
        elif attribute == SubmissionAttribute.COMMENTS:
            submissions = self.get_submission_comments(sub_type, time)
            sentences = []
            for submission in submissions:
                sentences += [comment.body for comment in submission]
        else:
            print("Invalid attribute for popular word analysis.")
            return []

        all_words = []
        for sentence in sentences:
            all_words += remove_stopwords(scrub_text(sentence))

        text = ' '.join(word for word in all_words)
        cloud = wordcloud.WordCloud().generate(text)
        plt.imshow(cloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()

        return rank_items(all_words)[0:limit]
