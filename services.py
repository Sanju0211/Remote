import os
import datetime # Not strictly used yet, but good for future date validation
from typing import List, Dict, Any, Type, Optional

# Assuming models.py and data_manager.py are in the same directory
from models import User, WalkingLog, WaterLog, SleepLog, WorkoutLog
from data_manager import load_data, save_data

# Define constants for filenames
USERS_FILE = "users.json"
WALKING_LOG_FILE = "walking_log.json"
WATER_LOG_FILE = "water_log.json"
SLEEP_LOG_FILE = "sleep_log.json"
WORKOUT_LOG_FILE = "workout_log.json"

# --- User Management ---

def add_user(name: str, height_cm: float, weight_kg: float) -> User:
    """
    Creates a new user, saves them to the users file, and returns the User object.
    """
    users_data = load_data(USERS_FILE) # Returns list of dicts or empty list

    new_user = User(name=name, height_cm=height_cm, weight_kg=weight_kg)

    # Ensure users_data is a list before appending
    if not isinstance(users_data, list):
        users_data = []

    users_data.append(new_user.to_dict())
    save_data(users_data, USERS_FILE)
    return new_user

def _get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Helper function to load users and find one by user_id.
    Returns the user dictionary if found, otherwise None.
    """
    users_data = load_data(USERS_FILE)
    if not isinstance(users_data, list): # Should be a list of user dicts
        return None
    for user_dict in users_data:
        if isinstance(user_dict, dict) and user_dict.get('user_id') == user_id:
            return user_dict
    return None

def update_user_profile(user_id: str, new_weight_kg: Optional[float] = None, new_height_cm: Optional[float] = None) -> bool:
    """
    Updates a user's weight and/or height.
    Returns True if successful, False otherwise.
    """
    users_data = load_data(USERS_FILE)
    if not isinstance(users_data, list):
        return False # Data integrity issue

    user_found = False
    updated_users_data = []
    for user_dict in users_data:
        if isinstance(user_dict, dict) and user_dict.get('user_id') == user_id:
            user_found = True
            if new_weight_kg is not None:
                user_dict['weight_kg'] = new_weight_kg
            if new_height_cm is not None:
                user_dict['height_cm'] = new_height_cm
        updated_users_data.append(user_dict)

    if user_found:
        save_data(updated_users_data, USERS_FILE)
        return True
    return False

# --- Generic Log Entry ---

def record_log_entry(
    user_id: str,
    log_data_class_constructor: Type[Union[WalkingLog, WaterLog, SleepLog, WorkoutLog]],
    log_file: str,
    **kwargs: Any
) -> Optional[Dict[str, Any]]:
    """
    Generic helper to record a new log entry for a user.
    Checks if user exists, creates log entry, saves it, and returns the entry as a dict.
    """
    if _get_user_by_id(user_id) is None:
        print(f"Error: User with ID '{user_id}' not found. Cannot record log.")
        return None

    log_entries = load_data(log_file) # Returns list of dicts or empty list

    # Ensure log_entries is a list before appending
    if not isinstance(log_entries, list):
        log_entries = []

    # Create new log object using the provided constructor and kwargs
    # The constructor (e.g., WalkingLog) will generate its own log_id
    new_log_entry_obj = log_data_class_constructor(user_id=user_id, **kwargs)

    log_entries.append(new_log_entry_obj.to_dict())
    save_data(log_entries, log_file)
    return new_log_entry_obj.to_dict()

# --- Specific Log Recording Functions ---

def record_walking(user_id: str, date: str, steps: int, distance_km: Optional[float] = None) -> Optional[Dict[str, Any]]:
    """Records a walking log entry for the user."""
    return record_log_entry(
        user_id=user_id,
        log_data_class_constructor=WalkingLog,
        log_file=WALKING_LOG_FILE,
        date=date,
        steps=steps,
        distance_km=distance_km
    )

def record_water(user_id: str, date: str, amount_ml: int) -> Optional[Dict[str, Any]]:
    """Records a water intake log entry for the user."""
    return record_log_entry(
        user_id=user_id,
        log_data_class_constructor=WaterLog,
        log_file=WATER_LOG_FILE,
        date=date,
        amount_ml=amount_ml
    )

def record_sleep(user_id: str, date: str, sleep_duration_hours: float, quality: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Records a sleep log entry for the user."""
    return record_log_entry(
        user_id=user_id,
        log_data_class_constructor=SleepLog,
        log_file=SLEEP_LOG_FILE,
        date=date,
        sleep_duration_hours=sleep_duration_hours,
        quality=quality
    )

def record_workout(
    user_id: str, date: str, start_time: str, end_time: str,
    type_of_workout: str, notes: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Records a workout log entry for the user."""
    return record_log_entry(
        user_id=user_id,
        log_data_class_constructor=WorkoutLog,
        log_file=WORKOUT_LOG_FILE,
        date=date,
        start_time=start_time,
        end_time=end_time,
        type_of_workout=type_of_workout,
        notes=notes
    )

# --- Data Retrieval ---

def get_user_data(user_id: str, data_type: str) -> List[Dict[str, Any]]:
    """
    Retrieves specific log data for a user.
    data_type can be "walking", "water", "sleep", "workout".
    """
    if _get_user_by_id(user_id) is None:
        print(f"Error: User with ID '{user_id}' not found. Cannot retrieve data.")
        return []

    log_file_map = {
        "walking": WALKING_LOG_FILE,
        "water": WATER_LOG_FILE,
        "sleep": SLEEP_LOG_FILE,
        "workout": WORKOUT_LOG_FILE,
        # "all_user_info": USERS_FILE # Could be an option
    }

    if data_type not in log_file_map:
        print(f"Error: Invalid data_type '{data_type}'. Valid types are: {', '.join(log_file_map.keys())}")
        return []

    log_file = log_file_map[data_type]
    all_logs = load_data(log_file) # Returns list of dicts

    if not isinstance(all_logs, list): # Should be a list of log dicts
        print(f"Warning: Data file {log_file} did not return a list. Returning empty.")
        return []

    user_specific_logs = []
    for log_entry in all_logs:
        if isinstance(log_entry, dict) and log_entry.get('user_id') == user_id:
            user_specific_logs.append(log_entry)

    return user_specific_logs

# Example of how to get user's own profile data (not logs)
def get_user_profile(user_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves the profile data for a specific user."""
    return _get_user_by_id(user_id)

# Type alias for log data class constructors
LogDataClass = Type[Union[WalkingLog, WaterLog, SleepLog, WorkoutLog]]
from typing import Union # ensure Union is imported if not already at top for LogDataClass
# (already imported, but good to double check for standalone snippets)

# Minor correction for record_log_entry type hint for log_data_class_constructor
# It should be Type[Union[...]] as used in the alias, not the instance.
# The current implementation has:
# log_data_class_constructor: Type[Union[WalkingLog, WaterLog, SleepLog, WorkoutLog]],
# which is correct.

# A note for add_user: it returns a User object, but saves its dict representation.
# This is consistent with the plan.

# A note for _get_user_by_id: it returns a dict, not a User object.
# This is fine for internal use, as other functions expect dicts for processing.

# A note for update_user_profile: it loads all users, modifies one, then saves all.
# This is standard for JSON file list management.

# A note for get_user_data:
# Added a check if all_logs is actually a list after loading.
# Ensures that filtering works on dictionary items.
print("services.py defined")
