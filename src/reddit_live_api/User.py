from urllib.parse import urlparse

import praw
import prawcore.exceptions

from ..keys import getID, getSecret, getAgent
from .Utils import scrub_text, rank_items, remove_stopwords, ignore_website
from ..socks_catch.utilities.evaluation import Evaluation


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

    def get_user_is_valid(self):
        try:
            test = self.user.id
            return True
        except prawcore.exceptions.Forbidden:
            return False
        except prawcore.exceptions.NotFound:
            return False

    def get_top_subreddits(self):
        comment_subs = self.get_comment_subreddits()
        submission_subs = self.get_submission_subreddits()
        all_subs = comment_subs + submission_subs

        rank_dict = rank_items(all_subs, True)

        sorted_rank_dict = {k: v for k, v in sorted(rank_dict.items(), key=lambda item: item[1], reverse=True) if v > 4}
        return sorted_rank_dict

    def get_popular_words(self):
        submission_titles = self.get_submission_titles()
        submission_text = self.get_submission_text()
        comment_text = self.get_comments_text()

        all_text = submission_titles + submission_text + comment_text

        all_words = []
        for sentence in all_text:
            all_words += remove_stopwords(scrub_text(sentence))

        rank_dict = rank_items(all_words, True)

        sorted_rank_dict = {k: v for k, v in sorted(rank_dict.items(), key=lambda item: item[1], reverse=True) if v > 4}
        return sorted_rank_dict

    def get_most_linked_websites(self):
        links = self.get_submission_links()
        scrubbed_links = [urlparse(link).netloc for link in links]
        scrubbed_links = [link.replace('www.', '') for link in scrubbed_links if not any(x in link for x in ignore_website)]

        rank_dict = rank_items(scrubbed_links, True)

        sorted_rank_dict = {k: v for k, v in sorted(rank_dict.items(), key=lambda item: item[1], reverse=True)}
        return sorted_rank_dict

    def get_proportion_controversial(self):
        votes = self.get_submission_upvote_ratios()
        count = sum(map(lambda x: (x <= 0.75) is True, votes))
        return {'controversial': count, 'non-controversial': (len(votes)-count)}

    def get_evaluation(self):
        try:
            val = Evaluation(self.username).__dict__
        except TypeError:
            return None
        return val

    ''' Comments
    This section allows us to obtain information about comments the user has left
    '''

    def get_comments(self):
        comments = []
        try:
            for comment in self.user.comments.new():
                    comments = comments + [comment]
        except prawcore.exceptions.NotFound:
            print('Encountered an error trying to obtain comments. Comments not found.')
            pass
        except prawcore.exceptions.ResponseException:
            print("Encountered an error receiving a response from Reddit. Generally temporary. Failing gracefully.")
            pass
        return comments

    def get_comments_text(self):
        comments = []
        try:
            for comment in self.user.comments.new():
                comments = comments + [comment.body]
        except prawcore.exceptions.NotFound:
            print('Encountered an error trying to obtain comments. Comments not found.')
            pass
        except prawcore.exceptions.ResponseException:
            print("Encountered an error receiving a response from Reddit. Generally temporary. Failing gracefully.")
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
            print('Encountered an error trying to obtain subreddits of comments. Comments not found.')
            pass
        except prawcore.exceptions.ResponseException:
            print("Encountered an error receiving a response from Reddit. Generally temporary. Failing gracefully.")
            pass
        return subs

    def get_comment_upvotes(self):
        items = []
        try:
            for item in self.user.comments.new():
                items = items + [item.score]
        except prawcore.exceptions.NotFound:
            print('Encountered an error trying to obtain comment upvotes. Comments not found.')
            pass
        except prawcore.exceptions.ResponseException:
            print("Encountered an error receiving a response from Reddit. Generally temporary. Failing gracefully.")
            pass
        return items

    def get_comment_karma(self):
        try:
            return self.user.comment_karma
        except prawcore.exceptions.NotFound:
            print('Encountered an error trying to obtain comment karma. Comments not found.')
            pass
        except prawcore.exceptions.ResponseException:
            print("Encountered an error receiving a response from Reddit. Generally temporary. Failing gracefully.")
            pass
        return -1

    ''' Links
    '''
    def get_link_karma(self):
        try:
            return self.user.link_karma
        except prawcore.exceptions.NotFound:
            print('Encountered an error trying to obtain link karma. Link karma not found.')
            pass
        except prawcore.exceptions.ResponseException:
            print("Encountered an error receiving a response from Reddit. Generally temporary. Failing gracefully.")
            pass
        return -1

    # TODO: potentially create a method that returns all links from comments if we end up needing it.

    ''' Submissions
    This section allows us to access the user's most recent submissions.
    '''
    def get_submissions(self):
        items = []
        try:
            for submission in self.user.submissions.new():
                items = items + [submission]
        except prawcore.exceptions.NotFound:
            print('Encountered an error trying to obtain submissions. Submissions not found.')
            pass
        return items

    def get_submission_titles(self):
        items = []
        try:
            for submission in self.user.submissions.new():
                items = items + [submission.title]
        except prawcore.exceptions.NotFound:
            print('Encountered an error trying to obtain submission titles. Submissions not found.')
            pass
        except prawcore.exceptions.ResponseException:
            print("Encountered an error receiving a response from Reddit. Generally temporary. Failing gracefully.")
            pass
        return items

    def get_submission_text(self):
        items = []
        try:
            for submission in self.user.submissions.new():
                items = items + [scrub_text(submission.selftext)]
        except prawcore.exceptions.NotFound:
            print('Encountered an error trying to obtain submission text. Submissions not found.')
            pass
        except prawcore.exceptions.ResponseException:
            print("Encountered an error receiving a response from Reddit. Generally temporary. Failing gracefully.")
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
        except prawcore.exceptions.ResponseException:
            print("Encountered an error receiving a response from Reddit. Generally temporary. Failing gracefully.")
            pass
        return items

    def get_submission_upvote_ratios(self):
        items = []
        try:
            for submission in self.user.submissions.new():
                items = items + [submission.upvote_ratio]
        except prawcore.exceptions.NotFound:
            print('Encountered an error trying to obtain submission upvote ratios. Submissions not found.')
            pass
        except prawcore.exceptions.ResponseException:
            print("Encountered an error receiving a response from Reddit. Generally temporary. Failing gracefully.")
            pass
        return items

    def get_submission_links(self):
        items = []
        submissions = self.user.submissions.new()
        for submission in submissions:
            if submission.url is not None:
                items = items + [submission.url]
        return items
