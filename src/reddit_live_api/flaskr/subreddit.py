from flask import Blueprint, request
from reddit_live_api.Subreddit import Subreddit
from reddit_live_api.dtos.subreddit_dto import SubredditDto
import json

bp = Blueprint("subreddit", __name__, url_prefix="/subreddit")


# Returns basic information about the subreddit and nothing else
@bp.route("", methods=["GET"])
def get_subreddit():
    subreddit_name = request.args.get('name')
    if subreddit_name is None:
        return "The request could not be completed because a required parameter (name) was not provided"

    subreddit = Subreddit(subreddit_name)
    return json.dumps(SubredditDto(subreddit).__dict__)

# @bp.route("/submissions", methods=["GET"])
# def get_subreddit_submissions():
#     type = request.args.get('type')
