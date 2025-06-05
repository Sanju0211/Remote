import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import os # Not strictly needed for these tests due to mocking open, but often used with data_manager

# Assuming data_manager.py is accessible
from data_manager import save_data, load_data

class TestDataManager(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_data(self, mock_json_dump, mock_file_open):
        """Test saving data successfully."""
        sample_data = {"key": "value", "numbers": [1, 2, 3]}
        dummy_filename = "test_save.json"

        save_data(sample_data, dummy_filename)

        mock_file_open.assert_called_once_with(dummy_filename, 'w', encoding='utf-8')
        # json.dump is called with the file object (handle) from open, and the data
        mock_json_dump.assert_called_once_with(sample_data, mock_file_open(), indent=4)

    @patch("builtins.open", new_callable=mock_open)
    @patch("data_manager.print") # Suppress print on error
    def test_save_data_io_error(self, mock_print, mock_file_open):
        """Test saving data when an IOError occurs."""
        sample_data = {"key": "value"}
        dummy_filename = "test_io_error.json"
        mock_file_open.side_effect = IOError("Disk full")

        save_data(sample_data, dummy_filename)

        mock_file_open.assert_called_once_with(dummy_filename, 'w', encoding='utf-8')
        mock_print.assert_called_once_with(f"Error saving data to {dummy_filename}: Disk full")

    def test_load_data_success(self):
        """Test loading data successfully from a JSON file."""
        sample_json_string = '{"name": "Test User", "age": 30}'
        expected_data = {"name": "Test User", "age": 30}
        dummy_filename = "test_load.json"

        # Patch 'open' specifically for this test using a context manager or decorator
        with patch("builtins.open", mock_open(read_data=sample_json_string)) as mock_file:
            loaded_data = load_data(dummy_filename)
            mock_file.assert_called_once_with(dummy_filename, 'r', encoding='utf-8')
            self.assertEqual(loaded_data, expected_data)

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_data_file_not_found(self, mock_file_open):
        """Test loading data when the file does not exist."""
        dummy_filename = "non_existent.json"

        loaded_data = load_data(dummy_filename)

        mock_file_open.assert_called_once_with(dummy_filename, 'r', encoding='utf-8')
        self.assertEqual(loaded_data, []) # Should return an empty list

    @patch("builtins.open", new_callable=mock_open, read_data="this is not json")
    @patch("data_manager.print") # Suppress print output during test
    def test_load_data_json_decode_error(self, mock_print, mock_file_open_invalid_json):
        """Test loading data when the file content is invalid JSON."""
        dummy_filename = "invalid_json.json"

        loaded_data = load_data(dummy_filename)

        mock_file_open_invalid_json.assert_called_once_with(dummy_filename, 'r', encoding='utf-8')
        mock_print.assert_called_once_with(f"Error: The file {dummy_filename} does not contain valid JSON. Returning empty list.")
        self.assertEqual(loaded_data, [])

    @patch("builtins.open", side_effect=IOError("Permission denied"))
    @patch("data_manager.print") # Suppress print output
    def test_load_data_io_error_other_than_not_found(self, mock_print, mock_file_open_io_error):
        """Test loading data with a generic IOError."""
        dummy_filename = "io_error_test.json"

        loaded_data = load_data(dummy_filename)

        mock_file_open_io_error.assert_called_once_with(dummy_filename, 'r', encoding='utf-8')
        mock_print.assert_called_once_with(f"Error loading data from {dummy_filename}: Permission denied. Returning empty list.")
        self.assertEqual(loaded_data, [])


if __name__ == '__main__':
    unittest.main()
