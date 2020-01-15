from User import User
from Subreddit import Subreddit

from matplotlib import pyplot as plt
from itertools import islice
import prawcore.exceptions
import tkinter


# Should only call this function if the User function supports the ranking
# functionality. Allows us to dynamically call this as needed
def get_users_top_ranked_subs_to_action(users, num_srs, function_to_run):
    sr_user_top_subs = {}
    for user in users:
        u = User(user)
        k = 0
        try:
            for ts in function_to_run(u, True):
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
    return sr_user_top_subs


def filter_and_plot_users(users, filter_level, title):
    for s in users.keys():
        if users[s] >= filter_level:
            plt.barh(s, users[s])

    plt.title(title.format(len(users)))
    plt.show()


def subreddit_plot_current_top_users_top_subreddits_to_submit(sr, num_srs=3, filter_subs_less_than=2):
    sr = Subreddit(sr)
    users = sr.get_top_submission_authors()

    filter_and_plot_users(get_users_top_ranked_subs_to_action(users, num_srs, User.get_submission_subreddits),
                          filter_subs_less_than, "Top " + str(num_srs) +
                          " Most Submitted to SubReddits by {0} Current Top Submission Submitters")


def submission_plot_commenters_other_top_subreddits(sr, post_num=0, num_srs=3,
                                                    filter_subs_less_than=2, match_title=""):
    subreddit = Subreddit(sr)

    # Acquire the post we want examined
    if match_title == "":
        sub = next(islice(subreddit.get_top_submissions(), post_num, None))
    else:
        found = False
        for p in subreddit.get_top_submissions():
            if p.title.lower() == match_title.lower():
                sub = p
                found = True
                break
        if found is False:
            print("Failed to find post {0} on r/{1}".format(match_title, sr))
            return

    # Look at top comments. Get list of all comments.
    sub.comment_sort = 'top'
    sub.comments.replace_more(limit=0)
    comments = sub.comments.list()

    users = {}
    for c in comments:
        # Accounts for deleted comments by seeing if author name is None
        if c.author is not None and c.author.name not in users:
            # Let's track score. Maybe we can cluster with it?
            users[c.author.name] = [c.score]

    filter_and_plot_users(get_users_top_ranked_subs_to_action(users.keys(), num_srs, User.get_comment_subreddits),
                          filter_subs_less_than,
                          "Top " + str(num_srs) + " Most Commented on SubReddits by {0} Commenters on Post:\n" +
                          sub.title + " on r/" + sr)


# subreddit_plot_current_top_users_top_subreddits_to_submit("dnd")

# submission_plot_commenters_other_top_subreddits(sr="conservative", match_title="clever title")
submission_plot_commenters_other_top_subreddits(sr="askreddit", post_num=3)