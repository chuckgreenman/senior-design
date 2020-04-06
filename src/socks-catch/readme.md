# Readme
This package is an altered implementation of a sock-puppet detection algorithm that was used by french researchers on Wikipedia.  You can read the full article [here](https://doi-org.proxy.libraries.uc.edu/10.1016/j.knosys.2018.03.002).

There are a couple of strucures and methodologies that are necessary for understanding what is going on in this part of the project.

The french paper takes a fair number of pains to genericize terms, but here I'll ungenericise the terms to make them applicable to our project specifically.

* Users -> Redditors - When we talk about users in the context of this project, we're talking about the 
* Categories -> Subreddits
* Pages -> Subreddits have a bunch of posts on the links.
* Actions -> Either a link submission or comment.

There are two artifacts that we need to generate, an action graph and a relationship graph.

* Action graph - This is a bipartite graph, the weight between a user and a page is defined as the average timestamp of that user's interactions with a page.
* Relationship graph - This is an undirected graph, the weight between two users is defined by the degree of relation between the two accounts (ui and uj) and it is calculated based on the normalized and inversed euclidean distance between the average of the actions’ time of ui and uj.

Using these two artifacts we apply the following techniques.

## Data Model
Storing the action graph and the relationship graphs tables is a little strange and it isn't immediately clear why the architectual decisions that were made, were made in the way that they were.

The table `activity` is a firehose of all the actions that they system understands, `action_grap` stores all of the weights for user and page combinations.  The Action graph is bipartite which allows it to be stored in this manner.

The `relationship graph` is fairly different, this is an undirected graph, where the distance between two users is calculated as described above. Due to this, we are going to need two tables to avoid duplicating data.

When possible we use performance sensitive SQL access, for example SQLite's `executemany`, as a result, some actions favor destroy and rebuilding a table rather than performing thousands of selects, at the current scale this is the correct decision.

## CLI
All commands can be called with `python cli.py`

* *dbsetup* - This will format the database properly for the environment that your pass it (development will be sqlite, postgres will be used in production.)
* *crawl* - Crawl can be called with the 
