from User import User
from Subreddit import Subreddit
from Utils import SubmissionType, sort_dictionary

from matplotlib import pyplot as plt
import prawcore.exceptions
import networkx as nx


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
    # Sort users first to group data better
    users = sort_dictionary(users)

    for s in users.keys():
        if users[s] >= filter_level:
            plt.barh(s, users[s])

    plt.title(title.format(len(users)))
    plt.show()


def subreddit_plot_current_top_users_top_subreddits_to_submit(sr, sub_type=SubmissionType.TOP, num_srs=3, filter_subs_less_than=2):
    sr = Subreddit(sr)
    users = sr.get_submission_authors(sub_type)

    filter_and_plot_users(get_users_top_ranked_subs_to_action(users, num_srs, User.get_submission_subreddits),
                          filter_subs_less_than, "Top " + str(num_srs) +
                          " Most Submitted to SubReddits by {0} Current Top Submission Submitters")


def submission_plot_commenters_other_top_subreddits(sr, sub_type=SubmissionType.TOP, post_num=0, num_srs=3,
                                                    filter_subs_less_than=2, match_title=""):
    subreddit = Subreddit(sr)

    # Acquire the post we want examined
    if match_title == "":
        try:
            sub = subreddit.get_submissions(sub_type)[post_num]
        except IndexError:
            print("Post number index out of bounds.")
    else:
        found = False
        for p in subreddit.get_submissions(sub_type):
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


def submission_plot_users_top_upvoted_subreddits(sr, sub_type=SubmissionType.TOP, num_srs=3, filter_subs_less_than=2):
    sr = Subreddit(sr)
    users = sr.get_submission_authors(sub_type)

    filter_and_plot_users(get_users_top_ranked_subs_to_action(users, num_srs, User.get_upvoted_subreddits),
                          filter_subs_less_than, "Top " + str(num_srs) +
                          " Most Upvoted SubReddits by {0} Current Top Submission Submitters")


def create_sub_network(sr, sub_type=SubmissionType.TOP, num_srs=3, filter_subs_less_than=15):
    # This will hold the subs and the number of users who have this sub as one of their top subs
    # Using dicts for quicker lookup
    srs_and_user_count_total = {}
    # Could just use one of these, but the memory overhead is minimal and I think it's more clear this way.
    srs_explored = {}
    srs_to_explore = {}

    # Directional graph that will store all nodes and edges
    sub_network = nx.DiGraph()

    # Tracks which sub will be explored next
    next_sub = sr

    continue_creation = True
    while continue_creation is True:
        # Needs to be reset on a per sub explored basis:
        # https://www.datacamp.com/community/tutorials/social-network-analysis-python
        subreddit = Subreddit(next_sub)
        users = subreddit.get_submission_authors(sub_type)
        users_top_srs = get_users_top_ranked_subs_to_action(users, num_srs, User.get_submission_subreddits)

        # Track explored sub
        srs_explored[subreddit.subreddit_name] = True

        for top_sr in users_top_srs:
            if top_sr in srs_and_user_count_total:
                srs_and_user_count_total[top_sr] = srs_and_user_count_total[top_sr] + users_top_srs[top_sr]
            else:
                srs_and_user_count_total[top_sr] = users_top_srs[top_sr]
            # Check to see if this sub's community interacts with top_sr enough to get over filter for exploration
            if users_top_srs[top_sr] >= filter_subs_less_than and top_sr not in srs_explored:
                srs_to_explore[top_sr] = True

        # Add to graph object
        for sub in users_top_srs:
            if users_top_srs[sub] >= filter_subs_less_than:
                # Ensure all edges are created
                sub_network.add_edge(subreddit.subreddit_name, sub)

        # Reset
        next_sub = ""
        for sub in srs_to_explore:
            if sub not in srs_explored:
                next_sub = sub
                break

        # If no more subs meet criteria, end exploration.
        if next_sub == "":
            continue_creation = False

    # Space out the graph to make it nice to view and draw it.
    nx.spring_layout(sub_network)
    nx.draw_networkx(sub_network)
    print(nx.info(sub_network))
    plt.show()


create_sub_network(sr="politics", filter_subs_less_than=10)
# subreddit_plot_current_top_users_top_subreddits_to_submit("news", SubmissionType.TOP, 10)

# submission_plot_commenters_other_top_subreddits(sr="conservative", match_title="clever title")
# subreddit_plot_current_top_users_top_subreddits_to_submit(sr="politics")
# submission_plot_users_top_upvoted_subreddits(sr="politics")
