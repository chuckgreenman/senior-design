import praw
import prawcore.exceptions
from keys import getID, getSecret, getAgent
from Utils import scrub_text, rank_items


class User:
    # Set up connection to Reddit and reference to user
    def __init__(self, username):
        self.ID = getID()
        self.secret = getSecret()
        self.agent = getAgent()
        self.username = username
        self.reddit = reddit = praw.Reddit(client_id= self.ID,
                         client_secret=self.secret,
                         user_agent=self.agent)
        self.user = reddit.redditor(self.username)

    ''' Comments
    This section allows us to obtain information about comments the user has left
    '''

    def get_comments(self):
        comments = []
        try:
            for comment in self.user.comments.new():
                    comments = comments + [scrub_text(comment.body)]
        except prawcore.exceptions.NotFound:
            # ignore posts from quarantined subreddits
            print('Encountered an error trying to obtain comments. Comments not found.')
            pass
        return comments

    def get_comment_subreddits(self, ranked=False):
        subs = []
        try:
            for comment in self.user.comments.new():

                    subs = subs + [comment.subreddit.display_name]
            if ranked:
                return rank_items(subs)
        except prawcore.exceptions.NotFound:
            # ignore posts from quarantined subreddits
            print('Encountered an error trying to obtain subreddits of comments. Comments not found.')
            pass
        return subs

    def get_comment_upvotes(self):
        items = []
        try:
            for item in self.user.comments.new():
                items = items + [item.score]
        except prawcore.exceptions.NotFound:
            # ignore posts from quarantined subreddits
            print('Encountered an error trying to obtain comment upvotes. Comments not found.')
            pass
        return items

    def get_comment_karma(self):
        try:
            return self.user.comment_karma
        except prawcore.exceptions.NotFound:
            # ignore posts from quarantined subreddits
            print('Encountered an error trying to obtain comment karma. Comments not found.')
            pass
        return -1

    ''' Downvotes
    This section allows the us to obtain information about posts the user has downvoted,
    indicating that they disagree with the content of the post.
    '''

    def get_downvoted_titles(self):
        items = []
        testing = self.user.downvoted()
        print(next(next(testing)))
        try:
            for dv in self.user.downvoted():
                items = items + [scrub_text(dv.title)]
        except prawcore.exceptions.NotFound:
            # ignore posts from quarantined subreddits
            print('Encountered an error trying to obtain downvoted titles. Downvoted posts not found.')
            pass
        except prawcore.exceptions.Forbidden:
            print('Encountered an error trying to obtain downvoted titles. Access to downvoted posts is forbidden.')
            pass
        return items

    def get_downvoted_text(self):
        items = []
        try:
            for dv in self.user.downvoted():
                items = items + [scrub_text(dv.selftext)]
        except prawcore.exceptions.NotFound:
            # ignore posts from quarantined subreddits
            print('Encountered an error trying to obtain downvoted text. Downvoted posts not found.')
            pass
        except prawcore.exceptions.Forbidden:
            print('Encountered an error trying to obtain downvoted text. Access to downvoted posts is forbidden.')
            pass
        return items

    def get_downvoted_subreddits(self, ranked=False):
        items = []
        try:
            for dv in self.user.downvoted():
                items = items + [dv.subreddit.display_name]
            if ranked:
                return rank_items(items)
        except prawcore.exceptions.NotFound:
            # ignore posts from quarantined subreddits
            print('Encountered an error trying to obtain downvoted subreddits. Downvoted posts not found.')
            pass
        except prawcore.exceptions.Forbidden:
            print('Encountered an error trying to obtain downvoted subreddits. Access to downvoted posts is forbidden.')
            pass
        return items

    def get_downvoted_upvote_ratios(self):
        items = []
        try:
            for dv in self.user.downvoted():
                items = items + [dv.upvote_ratio]
        except prawcore.exceptions.NotFound:
            # ignore posts from quarantined subreddits
            print('Encountered an error trying to obtain downvoted updvote ratios. Downvoted posts not found.')
            pass
        except prawcore.exceptions.Forbidden:
            print('Encountered an error trying to obtain downvoted upvote ratios. Access to downvoted posts is forbidden.')
            pass
        return items

    ''' Links
    '''
    def get_link_karma(self):
        try:
            return self.user.link_karma
        except prawcore.exceptions.NotFound:
            # ignore posts from quarantined subreddits
            print('Encountered an error trying to obtain link karma. Link karma not found.')
            pass
        return -1

    # TODO: potentially create a method that returns all links from comments if we end up needing it.

    ''' Submissions
    '''
    def get_submission_titles(self):
        items = []
        try:
            for submission in self.user.submissions.top('all'):
                items = items + [submission.title]
        except prawcore.exceptions.NotFound:
            print('Encountered an error trying to obtain submission titles. Submissions not found.')
            pass
        return items

    def get_submission_text(self):
        items = []
        try:
            for submission in self.user.submissions.top('all'):
                items = items + [scrub_text(submission.selftext)]
        except prawcore.exceptions.NotFound:
            print('Encountered an error trying to obtain submission text. Submissions not found.')
            pass
        return items

    def get_submission_subreddits(self, ranked=False):
        items = []
        try:
            for submission in self.user.submissions.new():
                items = items + [submission.subreddit.display_name]
            if ranked:
                return rank_items(items)
        except prawcore.exceptions.NotFound:
            print('Encountered an error trying to obtain submission subreddits. Submissions not found.')
            pass
        return items

    def get_submission_upvote_ratios(self):
        items = []
        try:
            for submission in self.user.submissions.top('all'):
                items = items + [submission.upvote_ratio]
        except prawcore.exceptions.NotFound:
            print('Encountered an error trying to obtain submission upvote ratios. Submissions not found.')
            pass
        return items

    # TODO: get URLs that the submissions link to, if necessary

    ''' Upvoted
    '''
    def get_upvoted_titles(self):
        items = []
        try:
            for uv in self.user.upvoted():
                items = items + [scrub_text(uv.title)]
        except prawcore.exceptions.NotFound:
            print('Encountered an error trying to obtain upvoted titles. Upvotes not found.')
            pass
        except prawcore.exceptions.Forbidden:
            print('Encountered an error trying to obtain upvoted titles. Access to upvoted posts is forbidden.')
            pass
        return items

    def get_upvoted_text(self):
        items = []
        try:
            for uv in self.user.upvoted():
                items = items + [scrub_text(uv.selftext)]
        except prawcore.exceptions.NotFound:
            print('Encountered an error trying to obtain upvoted text. Upvotes not found.')
            pass
        except prawcore.exceptions.Forbidden:
            print('Encountered an error trying to obtain upvoted text. Access to upvoted posts is forbidden.')
            pass
        return items

    def get_upvoted_subreddits(self, ranked=False):
        items = []
        try:
            for uv in self.user.upvoted():
                items = items + [uv.subreddit.display_name]
            if ranked:
                return rank_items(items)
        except prawcore.exceptions.NotFound:
            print('Encountered an error trying to obtain upvoted subreddits. Upvotes not found.')
            pass
        except prawcore.exceptions.Forbidden:
            print('Encountered an error trying to obtain upvoted subreddits. Access to upvoted posts is forbidden.')
            pass
        return items

    def get_upvoted_upvote_ratios(self):
        items = []
        try:
            for uv in self.user.upvoted():
                items = items + [uv.upvote_ratio]
        except prawcore.exceptions.NotFound:
            print('Encountered an error trying to obtain upvoted upvote ratios. Upvotes not found.')
            pass
        except prawcore.exceptions.Forbidden:
            print('Encountered an error trying to obtain upvoted upvote ratios. Access to upvoted posts is forbidden.')
            pass
        return items

user = User('_yobond')
print(user.get_submission_subreddits(True))