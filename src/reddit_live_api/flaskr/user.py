from flask import Blueprint, request
from reddit_live_api.User import User
from reddit_live_api.dtos.user_dto import UserDto
from reddit_live_api.dtos.submission_dto import SubmissionDto
from reddit_live_api.dtos.comment_dto import CommentDto
import json

bp = Blueprint("user", __name__, url_prefix="/user")


# Returns basic information about the user and nothing else
@bp.route("", methods=["GET"])
def get_user():
    username = request.args.get('name')
    if username is None:
        return "The request could not be completed because a required parameter (name) was not provided"

    user = User(username)
    return json.dumps(UserDto(user).__dict__)


# Returns recent user comments
@bp.route("/comments", methods=["GET"])
def get_user_comments():
    username = request.args.get('name')

    if username is None:
        return "The request could not be completed because a required parameter (name) was not provided"

    comments = User(username).get_comments()
    comments_dtos = [CommentDto(comment) for comment in comments]

    return json.dumps([dto.__dict__ for dto in comments_dtos])


@bp.route("/submissions", methods=["GET"])
def get_user_submissions():
    username = request.args.get('name')

    if username is None:
        return "The request could not be completed because a required parameter (name) was not provided"

    submissions = User(username).get_submissions()
    submissions_dtos = [SubmissionDto(sub) for sub in submissions]

    return json.dumps([dto.__dict__ for dto in submissions_dtos])
