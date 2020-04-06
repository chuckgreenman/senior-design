CREATE TABLE activity (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  subreddit VARCHAR(21),
  user VARCHAR(21),
  page_id VARCHAR(21),
  type VARCHAR(21),
  occurred DATETIME
);
