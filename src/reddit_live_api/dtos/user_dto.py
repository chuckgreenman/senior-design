# A class that takes a Submission object and converts it to a data transfer object (DTO) that only contains the desired
# information for an HTTP request


class UserDto:
    def __init__(self, user):
        self.is_valid = user.get_user_is_valid()
        if self.is_valid:
            self.comment_karma = user.get_comment_karma()
            self.link_karma = user.get_link_karma()
            self.top_subreddits = user.get_top_subreddits()
            self.popular_words = user.get_popular_words()
            self.most_linked_websites = user.get_most_linked_websites()
            self.proportion_controversial_posts = user.get_proportion_controversial()
            self.evaluation = user.get_evaluation()
