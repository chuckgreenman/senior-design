import os
import sqlite3
import math

class DbInteract:
  def __init__(self, environment='development'):
    if environment == 'development':
      self.connection = sqlite3.connect(os.path.join("development.db"))
      self.environment = environment
    else:
      raise Exception("Unrecognized enviroment variable.")

  # Add activity record will add an activity record to the
  # database if it is not already recorded 
  def add_activity_records(self, activities):
    if self.environment == 'development':
      c = self.connection.cursor()
      c.executemany("INSERT INTO activity (page_id, subreddit, user, type, occurred) VALUES (?,?,?,?,?);", activities)
      self.connection.commit()

  def refresh_action_graph(self):
    if self.environment == 'development':
      c = self.connection.cursor()
      c.execute("DELETE FROM action_graph")
      weights = c.execute("SELECT page_id, user, count(*), AVG(occurred) FROM activity GROUP BY user, page_id ORDER BY page_id")
      c2 = self.connection.cursor()
      c2.executemany("INSERT INTO action_graph (page_id, user, num_interactions, weight) VALUES (?,?,?,?);", weights)
      self.connection.commit()

  def refresh_relationship_graph(self):
    if self.environment == 'development':
      c = self.connection.cursor()
      unique_users_tuple = self.get_unique_users()

      c.execute("DELETE FROM relationship_graph")
      
      user_interaction_query = """
      SELECT DISTINCT ui.page_id, ui.user_i, ui.user_j, ui.user_i_weight, action_graph.weight as user_j_weight FROM
        action_graph,
        (SELECT DISTINCT pairs.page_id as page_id, pairs.user_i as user_i, pairs.user_j as user_j, action_graph.weight as user_i_weight FROM
          action_graph,
          (SELECT a.page_id, a.user as user_i, b.user as user_j FROM
            activity a,
            activity b
          WHERE
            NOT a.user = b.user AND
            NOT a.user = "AutoModerator" AND
            NOT b.user = "AutoModerator" AND
            a.page_id = b.page_id) pairs
          WHERE
            action_graph.user = pairs.user_i AND
            action_graph.page_id = pairs.page_id) ui
          WHERE
            action_graph.user = ui.user_j AND
            action_graph.page_id = ui.page_id;
      """
      rows = c.execute(user_interaction_query)

      distance = {}
      for row in rows:
        user_i = row[1]
        user_j = row[2]
        user_i_weight = row[3]
        user_j_weight = row[4]

        if user_i not in distance:
          distance[user_i] = {}
        if user_j not in distance[user_i]:
          distance[user_i][user_j] = 0

        distance[user_i][user_j] += 1/(1+((user_i_weight - user_j_weight)**2))

      distance_tuple_list = []
      max_dist = None
      min_dist = None
      for outer_key in distance:
        for inner_key in distance[outer_key]:
          if max_dist == None or max_dist < math.sqrt(distance[outer_key][inner_key]):
            max_dist = math.sqrt(distance[outer_key][inner_key])
          if min_dist == None or min_dist > math.sqrt(distance[outer_key][inner_key]):
            min_dist = math.sqrt(distance[outer_key][inner_key])

          distance_tuple_list.append((math.sqrt(distance[outer_key][inner_key]), outer_key, inner_key,))

      complete_tuple = []
      for tup in distance_tuple_list:
        weighted = (tup[0]-min_dist)/(max_dist-min_dist)
        complete_tuple.append((tup[0], weighted, tup[1], tup[2]))

      c.executemany("INSERT INTO relationship_graph (distance, weight, user_i, user_j) VALUES (?,?,?,?);", complete_tuple)
      self.connection.commit()

  def get_unique_users(self):
    if self.environment == 'development':
      c = self.connection.cursor()
      unique_users = c.execute("SELECT DISTINCT user FROM activity;")
      return unique_users

  def save_user_metadata(self, user):
    if self.environment == 'development':
      c = self.connection.cursor()
      c.execute("INSERT INTO user (user, max_activity, registrationTime, firstActionTime) VALUES (?,?,?,?);", user)
      self.connection.commit()

  def user_metadata_exists(self, user_name):
    if self.environment == 'development':
      c = self.connection.cursor()
      result = c.execute("SELECT count(*) FROM user WHERE user = ?;", user_name)
      values = result.fetchone()
      count = values[0]
      if count >= 1:
        return True
      return False

  def calculate_activity_percentile(self, user_id):
    if self.environment == 'development':
      c = self.connection.cursor()
      total_users = c.execute("SELECT count(DISTINCT user) FROM activity").fetchone()[0]
      users_actions = c.execute("SELECT count(*) FROM activity WHERE user = ?", (user_id,)).fetchone()[0]
      users_with_more_actions_query = """
        SELECT count(u.user_act_count) FROM
          (SELECT count(*) as user_act_count FROM activity GROUP BY user) u
        WHERE
          u.user_act_count > ?
      """

      users_with_more_actions = c.execute(users_with_more_actions_query, (users_actions,)).fetchone()[0]

      return 1-(users_with_more_actions/total_users)        
