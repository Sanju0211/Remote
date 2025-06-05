import unittest
import uuid
from models import User, WalkingLog, WaterLog, SleepLog, WorkoutLog # Assuming models.py is accessible

def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False

class TestModels(unittest.TestCase):

    def test_user_creation_and_to_dict(self):
        user = User(name="Test User", height_cm=180.0, weight_kg=75.0)
        self.assertIsInstance(user, User)
        self.assertTrue(is_valid_uuid(user.user_id))
        self.assertEqual(user.name, "Test User")
        self.assertEqual(user.height_cm, 180.0)
        self.assertEqual(user.weight_kg, 75.0)

        user_dict = user.to_dict()
        self.assertIsInstance(user_dict, dict)
        self.assertEqual(user_dict['user_id'], user.user_id)
        self.assertEqual(user_dict['name'], "Test User")
        self.assertEqual(user_dict['height_cm'], 180.0)
        self.assertEqual(user_dict['weight_kg'], 75.0)

    def test_walking_log_creation_and_to_dict(self):
        log = WalkingLog(user_id="test_user_123", date="2023-01-01", steps=5000)
        self.assertTrue(is_valid_uuid(log.log_id))
        self.assertEqual(log.user_id, "test_user_123")
        self.assertEqual(log.date, "2023-01-01")
        self.assertEqual(log.steps, 5000)
        self.assertIsNone(log.distance_km) # Optional, default None

        log_with_dist = WalkingLog(user_id="test_user_123", date="2023-01-01", steps=5000, distance_km=3.5)
        self.assertEqual(log_with_dist.distance_km, 3.5)

        log_dict = log_with_dist.to_dict()
        self.assertIsInstance(log_dict, dict)
        self.assertEqual(log_dict['log_id'], log_with_dist.log_id)
        self.assertEqual(log_dict['user_id'], "test_user_123")
        self.assertEqual(log_dict['steps'], 5000)
        self.assertEqual(log_dict['distance_km'], 3.5)

    def test_water_log_creation_and_to_dict(self):
        log = WaterLog(user_id="test_user_456", date="2023-01-02", amount_ml=500)
        self.assertTrue(is_valid_uuid(log.log_id))
        self.assertEqual(log.user_id, "test_user_456")
        self.assertEqual(log.date, "2023-01-02")
        self.assertEqual(log.amount_ml, 500)

        log_dict = log.to_dict()
        self.assertIsInstance(log_dict, dict)
        self.assertEqual(log_dict['log_id'], log.log_id)
        self.assertEqual(log_dict['amount_ml'], 500)

    def test_sleep_log_creation_and_to_dict(self):
        log = SleepLog(user_id="test_user_789", date="2023-01-03", sleep_duration_hours=7.5)
        self.assertTrue(is_valid_uuid(log.log_id))
        self.assertEqual(log.user_id, "test_user_789")
        self.assertEqual(log.sleep_duration_hours, 7.5)
        self.assertIsNone(log.quality) # Optional, default None

        log_with_quality = SleepLog(user_id="test_user_789", date="2023-01-03", sleep_duration_hours=8.0, quality="Good")
        self.assertEqual(log_with_quality.quality, "Good")

        log_dict = log_with_quality.to_dict()
        self.assertIsInstance(log_dict, dict)
        self.assertEqual(log_dict['log_id'], log_with_quality.log_id)
        self.assertEqual(log_dict['quality'], "Good")

    def test_workout_log_creation_and_to_dict(self):
        log = WorkoutLog(user_id="test_user_abc", date="2023-01-04", start_time="10:00", end_time="11:00", type_of_workout="Running")
        self.assertTrue(is_valid_uuid(log.log_id))
        self.assertEqual(log.user_id, "test_user_abc")
        self.assertEqual(log.type_of_workout, "Running")
        self.assertIsNone(log.notes) # Optional, default None

        log_with_notes = WorkoutLog(user_id="test_user_abc", date="2023-01-04", start_time="10:00", end_time="11:00", type_of_workout="Weightlifting", notes="Heavy session")
        self.assertEqual(log_with_notes.notes, "Heavy session")

        log_dict = log_with_notes.to_dict()
        self.assertIsInstance(log_dict, dict)
        self.assertEqual(log_dict['log_id'], log_with_notes.log_id)
        self.assertEqual(log_dict['notes'], "Heavy session")

if __name__ == '__main__':
    unittest.main()
