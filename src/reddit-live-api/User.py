import praw
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
    # Gets user comments as list of strings, sorted by newest first
    def get_comments(self):
        comments = []
        for comment in self.user.comments.new():
            comments = comments + [scrub_text(comment.body)]
        return comments

    def get_comment_subreddits(self, ranked=False):
        subs = []
        for comment in self.user.comments.new():
            subs = subs + [comment.subreddit.display_name]
        if ranked:
            return rank_items(subs)
        return subs

    def get_comment_upvotes(self):
        items = []
        for item in self.user.comments.new():
            items = items + [item.score]
        return items

    def get_comment_karma(self):
        return self.user.comment_karma

    ''' Downvotes
    This section allows the us to obtain information about posts the user has downvoted,
    indicating that they disagree with the content of the post.
    '''

    def get_downvoted_titles(self):
        items = []
        for dv in self.user.downvoted():
            items = items + [scrub_text(dv.title)]
        return items

    def get_downvoted_text(self):
        items = []
        for dv in self.user.downvoted():
            items = items + [scrub_text(dv.selftext)]
        return items

    def get_downvoted_subreddits(self, ranked=False):
        items = []
        for dv in self.user.downvoted():
            items = items + [dv.subreddit.display_name]
        if ranked:
            return rank_items(items)
        return items

    def get_downvoted_upvote_ratios(self):
        items = []
        for dv in self.user.downvoted():
            items = items + [dv.upvote_ratio]
        return items

    ''' Links
    '''
    def get_link_karma(self):
        return self.user.link_karma

    # TODO: potentially create a method that returns all links from comments if we end up needing it.

    ''' Submissions
    '''
    def get_submission_titles(self):
        items = []
        for submission in self.user.submissions.top('all'):
            items = items + [submission.title]
        return items

    def get_submission_text(self):
        items = []
        for submission in self.user.submissions.top('all'):
            items = items + [scrub_text(submission.selftext)]
        return items

    def get_submission_subreddits(self, ranked=False):
        items = []
        for submission in self.user.submissions.top('all'):
            items = items + [submission.subreddit.display_name]
        if ranked:
            return rank_items(items)
        return items

    def get_submission_upvote_ratios(self):
        items = []
        for submission in self.user.submissions.top('all'):
            items = items + [submission.upvote_ratio]
        return items

    # TODO: get URLs that the submissions link to, if necessary

    ''' Upvoted
    '''
    def get_upvoted_titles(self):
        items = []
        for uv in self.user.upvoted():
            items = items + [scrub_text(uv.title)]
        return items

    def get_upvoted_text(self):
        items = []
        for uv in self.user.upvoted():
            items = items + [scrub_text(uv.selftext)]
        return items

    def get_upvoted_subreddits(self, ranked=False):
        items = []
        for uv in self.user.upvoted():
            items = items + [uv.subreddit.display_name]
        if ranked:
            return rank_items(items)
        return items

    def get_upvoted_upvote_ratios(self):
        items = []
        for uv in self.user.upvoted():
            items = items + [uv.upvote_ratio]
        return items

    ''' Moderator
    '''
    def get_moderated_subreddits(self):
        items = []
        for subreddit in self.user.moderated():
            items = items + [subreddit.display_name]

user = User('hawksoul12')
print(user.get_upvoted_titles())
