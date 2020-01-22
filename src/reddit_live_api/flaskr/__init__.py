from flask import Flask, request
import os
from reddit_live_api.Subreddit import Subreddit


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/subreddit', methods=['GET'])
    def get_subreddit():
        subreddit_name = request.args.get('name')
        #attribute = request.args.get('attribute')
        if subreddit_name is None:
            return "some parameter not provided"

        subreddit = Subreddit(subreddit_name)
        return subreddit.get_description()

    return app
