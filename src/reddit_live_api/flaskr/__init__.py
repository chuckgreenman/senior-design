from flask import Flask
import os
from reddit_live_api.flaskr import subreddit, user
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    CORS(app)
    

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(subreddit.bp)
    app.register_blueprint(user.bp)

    return app
