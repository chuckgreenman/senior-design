# A class that takes a Subreddit object and converts it to a data transfer object (DTO) that only contains the desired
# information about related subreddits for HTTP request


class RelatedDto:
    def __init__(self, subreddit, create_graph):
        self.name = subreddit.subreddit_name
        self.related_subreddits = subreddit.get_related_subreddits()
        if create_graph:
            self.related_graph = subreddit.create_subreddit_graph()
        else:
            self.related_graph = None
