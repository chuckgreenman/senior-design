CREATE TABLE activity (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  subreddit_id VARCHAR(21),
  user_id VARCHAR(21),
  page_id VARCHAR(21),
  type VARCHAR(21),
  occurred DATETIME
);
