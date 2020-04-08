from .db_interact import DbInteract
class Evaluation():
  def __init__(self, user_id):
    db = DbInteract()
    self.user_id = user_id
    self.delay_percentile = db.calculate_delay_percentile(self.user_id)
    self.action_count_percentile = db.calculate_activity_percentile(self.user_id)
    self.closest_users_by_relationship_weight = db.closest_users_by_relationship_weight(self.user_id)
