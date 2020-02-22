from flask import Blueprint, request
from reddit_live_api.Subreddit import Subreddit
from reddit_live_api.dtos.subreddit_dto import SubredditDto
from reddit_live_api.dtos.submission_dto import SubmissionDto
from reddit_live_api.Utils import SubmissionType, TimeFrame, SubmissionAttribute
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
    type = request.args.get('type')
    time_frame = request.args.get('time_frame')
    attrib = request.args.get('attrib')

    if subreddit_name is None:
        return "The request could not be completed because a required parameter (name) was not provided"
    if type is None or str.upper(type) not in SubmissionType.__members__:
        return "The request could not be completed because a required parameter (type) was not an acceptable value"
    if time_frame is None or str.upper(time_frame) not in TimeFrame.__members__:
        return "The request could not be completed because a required parameter (time_frame) was not an acceptable value"

    submissions = Subreddit(subreddit_name).get_submissions(SubmissionType[str.upper(type)], TimeFrame[str.upper(time_frame)])
    submissions_dtos = [SubmissionDto(sub) for sub in submissions]

    return json.dumps([dto.__dict__ for dto in submissions_dtos])




