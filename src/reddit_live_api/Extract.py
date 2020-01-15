from User import User
from Subreddit import Subreddit

from matplotlib import pyplot as plt
import prawcore.exceptions
import tkinter


def subreddit_plot_current_top_users_top_subreddits(sr, num_srs=3, filter_subs_less_than=2):
    sr = Subreddit(sr)
    users = sr.get_top_submission_authors()

    sr_user_top_subs = {}
    for user in users:
        u = User(user)
        k = 0
        try:
            for ts in u.get_submission_subreddits(True):
                if ts in sr_user_top_subs:
                    sr_user_top_subs[ts] += 1
                else:
                    sr_user_top_subs[ts] = 1
                k += 1
                if k == num_srs:
                    break
        except prawcore.exceptions.NotFound:
            # Fail gracefully
            pass

    for s in sr_user_top_subs.keys():
        if sr_user_top_subs[s] >= filter_subs_less_than:
            plt.barh(s, sr_user_top_subs[s])

    plt.title("Top Three Most Submitted to SubReddits by {0} Current Top Submission Submitters".format(len(users)))
    plt.show()


subreddit_plot_current_top_users_top_subreddits("dnd")
