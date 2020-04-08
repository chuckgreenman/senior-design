from urllib.parse import urlparse

import praw
import prawcore.exceptions
from bs4 import BeautifulSoup

from ..keys import getID, getSecret, getAgent
from .User import User
from .Utils import scrub_text, SubmissionType, TimeFrame, remove_stopwords, rank_items, ignore_website


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

    def get_submission_links(self, sub_type=SubmissionType.TOP, time=TimeFrame.WEEK):
        items = []
        submissions = self.get_submissions(sub_type, time)
        for submission in submissions:
            if submission.url is not None:
                items = items + [submission.url]
        return items

    def get_submission_upvote_ratios(self, sub_type=SubmissionType.TOP, time=TimeFrame.WEEK):
        items = []
        submissions = self.get_submissions(sub_type, time)
        print(len(submissions))
        for submission in submissions:
                items = items + [submission.upvote_ratio]
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

    ''' Extra analysis
    '''
    # Gets most used words from top post titles and body text
    def get_popular_words(self):
        submission_titles = self.get_submission_titles()
        submission_text = self.get_submission_text()

        all_text = submission_titles + submission_text

        all_words = []
        for sentence in all_text:
            all_words += remove_stopwords(scrub_text(sentence))

        rank_dict = rank_items(all_words, True)

        sorted_rank_dict = {k: v for k, v in sorted(rank_dict.items(), key=lambda item: item[1], reverse=True) if v > 4}
        return sorted_rank_dict

    # Analyzes all recent authors of top posts to get any subreddits that have a strong association
    def get_related_subreddits(self):
        top_authors = self.get_submission_authors()[:20]  # Get authors of recent popular posts
        subreddit_candidates = {}

        for author in top_authors:
            author_user = User(author)  # Create a User object for each author so we can get top subs
            author_top_subs_dict = author_user.get_top_subreddits()
            author_top_subs = list(author_top_subs_dict.keys())[:3]

            for sub in author_top_subs:
                sub = sub.lower()
                if sub in subreddit_candidates:
                    subreddit_candidates[sub] += 1
                else:
                    subreddit_candidates[sub] = 1

        filtered_subs = {k: v for k, v in subreddit_candidates.items() if ((v >= 2) and (k != self.subreddit_name.lower()))}

        return filtered_subs

    # A more in depth version of above; instead of stopping at first association, sees what's associated with those,
    # and so on, to create a graph of related subreddit activity
    def create_subreddit_graph(self):
        num_nodes = 1
        current_subreddit = self.subreddit_name.lower()
        to_explore = [current_subreddit]
        explored = []
        edges = {}
        weights = {}
        while num_nodes < 10:
            subreddit = Subreddit(current_subreddit)
            top_authors = subreddit.get_submission_authors()[:20]  # Get authors of recent popular posts
            subreddit_candidates = {}

            for author in top_authors:
                author_user = User(author)  # Create a User object for each author so we can get top subs
                author_top_subs_dict = author_user.get_top_subreddits()
                author_top_subs = list(author_top_subs_dict.keys())[:3]

                for sub in author_top_subs:
                    if sub.lower() in subreddit_candidates:
                        subreddit_candidates[sub.lower()] += 1
                    else:
                        subreddit_candidates[sub.lower()] = 1

            # Filter so frequencies of one and entries for current subreddit are removed.
            # Note that we convert subs to lowercase for comparison to avoid case issues
            filtered_subs = [k.lower() for k, v
                             in subreddit_candidates.items() if ((v >= 2) and (k.lower() != current_subreddit))]

            # If no connected subreddits pass the threshold, either explore a new node or quit exploring
            if len(filtered_subs) == 0:
                if len(to_explore) > 0:  # Explore the next viable node
                    explored += to_explore.pop(0)
                    if len(to_explore) > 0:
                        current_subreddit = to_explore[0]
                else:  # If there are no more viable nodes to explore, just quit
                    num_nodes = 11  # force quit
            else:
                # Add edges to the dictionary for any related subreddit that has enough activity
                if current_subreddit in edges:
                    edges[current_subreddit] = edges[current_subreddit] + filtered_subs
                else:
                    edges[current_subreddit] = filtered_subs

                # Update weights with anything we found this round
                for visited_sub in filtered_subs:
                    if visited_sub in weights:
                        weights[visited_sub] = weights[visited_sub] + subreddit_candidates[visited_sub]
                    else:
                        weights[visited_sub] = subreddit_candidates[visited_sub]

                # Update the number of nodes now that we've added edges
                filtered_subs = [val for val in filtered_subs if val not in explored]  # alter so only includes new subs
                num_nodes += len(filtered_subs)
                # Remove the first element of the list of nodes to explore because we've explored it
                explored += to_explore.pop(0)
                to_explore += filtered_subs
                current_subreddit = to_explore[0]

        if self.subreddit_name.lower() in weights:
            weights[self.subreddit_name.lower()] += 20
        else:
            weights[self.subreddit_name.lower()] = 20

        return edges, weights

    def get_most_linked_websites(self):
        links = self.get_submission_links()
        scrubbed_links = [urlparse(link).netloc for link in links]
        scrubbed_links = [link.replace('www.', '') for link in scrubbed_links if
                          not any(x in link for x in ignore_website) and link != '']

        rank_dict = rank_items(scrubbed_links, True)

        sorted_rank_dict = {k: v for k, v in sorted(rank_dict.items(), key=lambda item: item[1], reverse=True)}
        return sorted_rank_dict

    def get_proportion_controversial(self):
        votes = self.get_submission_upvote_ratios()
        print(len(votes))
        count = sum(map(lambda x: (x <= 0.75) is True, votes))
        return {'controversial': count, 'non-controversial': (len(votes)-count)}
