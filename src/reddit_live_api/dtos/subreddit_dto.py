# A class that takes a Subreddit object and converts it to a data transfer object (DTO) that only contains the desired
# information for an HTTP request


class SubredditDto:
    def __init__(self, subreddit):
        self.name = subreddit.subreddit_name
        self.description = subreddit.get_description()
        self.sub_count = subreddit.get_subscriber_count()
        self.is_valid = subreddit.check_subreddit_valid()
        self.is_quarantined = subreddit.get_is_quarantined()