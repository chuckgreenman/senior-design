from flask import Blueprint, request
from reddit_live_api.Subreddit import Subreddit
from reddit_live_api.dtos.subreddit_dto import SubredditDto
from reddit_live_api.dtos.submission_dto import SubmissionDto
from reddit_live_api.dtos.comment_dto import CommentDto
from reddit_live_api.dtos.related_dto import RelatedDto
from reddit_live_api.Utils import SubmissionType, TimeFrame
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


@bp.route("/submissions", methods=["GET"])
def get_subreddit_submissions():
    subreddit_name = request.args.get('name')
    sub_type = request.args.get('type')
    time_frame = request.args.get('time_frame')

    if subreddit_name is None:
        return "The request could not be completed because a required parameter (name) was not provided"
    if sub_type is None or str.upper(sub_type) not in SubmissionType.__members__:
        return "The request could not be completed because a required parameter (type) was not an acceptable value"
    if time_frame is None or str.upper(time_frame) not in TimeFrame.__members__:
        return "The request could not be completed because a required parameter (time_frame) was not an acceptable value"

    submissions = Subreddit(subreddit_name).get_submissions(SubmissionType[str.upper(sub_type)], TimeFrame[str.upper(time_frame)])
    submissions_dtos = [SubmissionDto(sub) for sub in submissions]

    return json.dumps([dto.__dict__ for dto in submissions_dtos])


@bp.route("/comments", methods=["GET"])
def get_subreddit_comments():
    subreddit_name = request.args.get('name')
    limit = int(request.args.get('limit'))

    if subreddit_name is None:
        return "The request could not be completed because a required parameter (name) was not provided"
    if limit is None or limit < 0:
        return "The request could not be completed because a required parameter (limit) was not provided or was less than 0"

    comments = Subreddit(subreddit_name).get_comments(limit)
    comments_dtos = [CommentDto(comment) for comment in comments]

    return json.dumps([dto.__dict__ for dto in comments_dtos])


@bp.route("/related", methods=["GET"])
def get_related_subreddits():
    subreddit_name = request.args.get('name')
    create_graph = request.args.get('create_graph')

    if create_graph is None or str.lower(create_graph) == 'false':
        create_graph = False
    elif  str.lower(create_graph) == 'true':
        create_graph = True
    else:
        return "The request could not be completed because a required parameter (graph) was not provided"

    if subreddit_name is None:
        return "The request could not be completed because a required parameter (name) was not provided"

    sub = Subreddit(subreddit_name)
    return json.dumps(RelatedDto(sub, create_graph).__dict__)


