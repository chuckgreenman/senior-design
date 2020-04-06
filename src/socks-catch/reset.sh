rm development.db
python cli.py dbsetup
python cli.py importbaseline link --path /home/chuck/Documents/reddit_data/links
python cli.py importbaseline comment --path /home/chuck/Documents/reddit_data/comments/
python cli.py refreshactiongraph
python cli.py refreshrelationshipgraph
python cli.py crawlusermeta