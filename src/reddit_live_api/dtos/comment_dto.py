# A class that takes a Comment object and converts it to a data transfer object (DTO) that only contains the desired
# information for an HTTP request


class CommentDto:
    def __init__(self, comment):
        self.text = comment.body
        self.author = comment.author.name
