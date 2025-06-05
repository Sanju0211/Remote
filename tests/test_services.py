import unittest
from unittest.mock import patch, MagicMock, ANY # ANY is useful for some assertions
import os # For filename constants if needed, though services has them
import json # For comparing dicts if necessary

# Assuming services.py, models.py, data_manager.py are accessible
import services
from models import User, WalkingLog # Import specific models for type checks or direct use
# Constants from services
from services import USERS_FILE, WALKING_LOG_FILE, WATER_LOG_FILE, SLEEP_LOG_FILE, WORKOUT_LOG_FILE

class TestServices(unittest.TestCase):

    @patch("services.save_data")
    @patch("services.load_data")
    def test_add_user(self, mock_load_data, mock_save_data):
        mock_load_data.return_value = [] # Simulate no existing users

        name = "Test User"
        height = 175.0
        weight = 70.0

        created_user_obj = services.add_user(name, height, weight)

        mock_load_data.assert_called_once_with(USERS_FILE)

        self.assertIsInstance(created_user_obj, User)
        self.assertEqual(created_user_obj.name, name)
        self.assertEqual(created_user_obj.height_cm, height)
        self.assertEqual(created_user_obj.weight_kg, weight)

        # Check that save_data was called with a list containing the new user's dict
        mock_save_data.assert_called_once()
        args_saved = mock_save_data.call_args[0] # Get positional arguments
        saved_data_list = args_saved[0]
        saved_filename = args_saved[1]

        self.assertEqual(saved_filename, USERS_FILE)
        self.assertEqual(len(saved_data_list), 1)
        self.assertEqual(saved_data_list[0]['name'], name)
        self.assertEqual(saved_data_list[0]['user_id'], created_user_obj.user_id)

    @patch("services.save_data")
    @patch("services.load_data")
    @patch("services._get_user_by_id") # Mocking the helper directly
    def test_update_user_profile_success(self, mock_get_user_by_id, mock_load_data, mock_save_data):
        user_id = "test_user_123"
        original_users_data = [
            {"user_id": user_id, "name": "Old Name", "height_cm": 170.0, "weight_kg": 65.0},
            {"user_id": "other_user", "name": "Other User", "height_cm": 160.0, "weight_kg": 60.0}
        ]
        mock_load_data.return_value = original_users_data
        # _get_user_by_id is not strictly needed here if load_data is mocked for update_user_profile's internal load
        # but it's good practice to keep it if other parts of the flow use it.
        # For update_user_profile, it re-loads data itself.

        success = services.update_user_profile(user_id, new_weight_kg=70.0, new_height_cm=172.0)

        self.assertTrue(success)
        mock_load_data.assert_called_once_with(USERS_FILE)

        mock_save_data.assert_called_once()
        saved_data_list = mock_save_data.call_args[0][0]

        updated_user_in_saved_data = None
        for u in saved_data_list:
            if u['user_id'] == user_id:
                updated_user_in_saved_data = u
                break

        self.assertIsNotNone(updated_user_in_saved_data)
        self.assertEqual(updated_user_in_saved_data['weight_kg'], 70.0)
        self.assertEqual(updated_user_in_saved_data['height_cm'], 172.0)

    @patch("services.load_data") # update_user_profile loads data itself
    def test_update_user_profile_user_not_found(self, mock_load_data):
        mock_load_data.return_value = [{"user_id": "other_user", "name": "Other"}]

        success = services.update_user_profile("non_existent_user", new_weight_kg=70.0)
        self.assertFalse(success)
        mock_load_data.assert_called_once_with(USERS_FILE)


    @patch("services.save_data")
    @patch("services.load_data")
    @patch("services._get_user_by_id")
    def test_record_walking_user_exists(self, mock_get_user_by_id, mock_load_data, mock_save_data):
        user_id = "user1"
        mock_get_user_by_id.return_value = {"user_id": user_id, "name": "Test User"} # Simulate user exists
        mock_load_data.return_value = [] # Simulate no existing logs

        date = "2023-01-01"
        steps = 5000
        distance = 3.5

        log_entry = services.record_walking(user_id, date, steps, distance)

        mock_get_user_by_id.assert_called_once_with(user_id)
        mock_load_data.assert_called_once_with(WALKING_LOG_FILE)

        self.assertIsNotNone(log_entry)
        self.assertEqual(log_entry['user_id'], user_id)
        self.assertEqual(log_entry['steps'], steps)
        self.assertEqual(log_entry['distance_km'], distance)
        self.assertTrue('log_id' in log_entry)

        mock_save_data.assert_called_once()
        saved_logs = mock_save_data.call_args[0][0]
        self.assertEqual(len(saved_logs), 1)
        self.assertEqual(saved_logs[0]['user_id'], user_id)
        self.assertEqual(saved_logs[0]['steps'], steps)

    @patch("services.print") # Suppress print
    @patch("services._get_user_by_id")
    def test_record_walking_user_not_exists(self, mock_get_user_by_id, mock_print):
        mock_get_user_by_id.return_value = None # Simulate user does not exist

        log_entry = services.record_walking("unknown_user", "2023-01-01", 5000)

        self.assertIsNone(log_entry)
        mock_get_user_by_id.assert_called_once_with("unknown_user")
        mock_print.assert_called_once_with("Error: User with ID 'unknown_user' not found. Cannot record log.")

    @patch("services.load_data")
    @patch("services._get_user_by_id")
    def test_get_user_data_found(self, mock_get_user_by_id, mock_load_data):
        user_id = "user_test"
        mock_get_user_by_id.return_value = {"user_id": user_id, "name": "Test User"}

        dummy_log_data = [
            {"log_id": "log1", "user_id": user_id, "steps": 100},
            {"log_id": "log2", "user_id": "other_user", "steps": 200},
            {"log_id": "log3", "user_id": user_id, "steps": 300},
        ]
        mock_load_data.return_value = dummy_log_data

        # Test for "walking" type, which uses WALKING_LOG_FILE
        user_logs = services.get_user_data(user_id, "walking")

        mock_get_user_by_id.assert_called_once_with(user_id)
        mock_load_data.assert_called_once_with(WALKING_LOG_FILE) # Check correct file is loaded

        self.assertEqual(len(user_logs), 2)
        self.assertTrue(all(log['user_id'] == user_id for log in user_logs))
        self.assertEqual(user_logs[0]['steps'], 100)
        self.assertEqual(user_logs[1]['steps'], 300)

    @patch("services.print") # Suppress print
    @patch("services._get_user_by_id")
    def test_get_user_data_user_not_found(self, mock_get_user_by_id, mock_print):
        mock_get_user_by_id.return_value = None

        user_logs = services.get_user_data("unknown_user", "walking")

        self.assertEqual(user_logs, [])
        mock_get_user_by_id.assert_called_once_with("unknown_user")
        mock_print.assert_called_once_with("Error: User with ID 'unknown_user' not found. Cannot retrieve data.")

    @patch("services.print")
    @patch("services._get_user_by_id") # Assume user exists for this test
    def test_get_user_data_invalid_type(self, mock_get_user_by_id, mock_print):
        user_id = "user_test"
        mock_get_user_by_id.return_value = {"user_id": user_id, "name": "Test User"}

        user_logs = services.get_user_data(user_id, "invalid_log_type")

        self.assertEqual(user_logs, [])
        mock_get_user_by_id.assert_called_once_with(user_id) # Still checks user
        # Check that print was called with the specific error message for invalid data_type
        valid_types = ", ".join(["walking", "water", "sleep", "workout"])
        mock_print.assert_called_once_with(f"Error: Invalid data_type 'invalid_log_type'. Valid types are: {valid_types}")


if __name__ == '__main__':
    unittest.main()
