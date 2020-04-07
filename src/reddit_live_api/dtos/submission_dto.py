# A class that takes a Submission object and converts it to a data transfer object (DTO) that only contains the desired
# information for an HTTP request
from ..Utils import scrub_text


class SubmissionDto:
    def __init__(self, submission):
        self.title = scrub_text(submission.title)
        self.text = scrub_text(submission.selftext)
        self.author = submission.author.name
        self.subreddit = submission.subreddit.display_name
        self.upvote_ratio = submission.upvote_ratio
