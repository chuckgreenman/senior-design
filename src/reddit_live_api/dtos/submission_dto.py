# A class that takes a Submission object and converts it to a data transfer object (DTO) that only contains the desired
# information for an HTTP request
from reddit_live_api.Utils import scrub_text


class SubmissionDto:
    def __init__(self, submission):
        self.title = scrub_text(submission.title)
        self.text = scrub_text(submission.selftext)
        self.author = submission.author.name