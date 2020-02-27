# A class that takes a Submission object and converts it to a data transfer object (DTO) that only contains the desired
# information for an HTTP request


class UserDto:
    def __init__(self, user):
        self.is_valid = user.get_user_is_valid()
        self.comment_karma = user.get_comment_karma()
        self.link_karma = user.get_link_karma()
