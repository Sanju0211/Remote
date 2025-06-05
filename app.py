import argparse
import json
from services import (
    add_user,
    update_user_profile,
    get_user_profile, # Using this instead of _get_user_by_id for direct profile view
    record_walking,
    record_water,
    record_sleep,
    record_workout,
    get_user_data
)
from utils import calculate_bmi
from models import User # For type hinting if needed, though services return dicts/objects
from typing import Any # Ensure Any is imported at the top level for pretty_print

def pretty_print(data: Any):
    """Helper to print data nicely, especially dicts and lists."""
    if isinstance(data, (dict, list)):
        print(json.dumps(data, indent=4))
    elif data is None:
        print("No data to show or operation resulted in None.")
    else:
        print(data)

def main():
    parser = argparse.ArgumentParser(description="Health & Fitness Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", help="Main command group", required=True)

    # --- User Subparser ---
    user_parser = subparsers.add_parser("user", help="Manage users")
    user_subparsers = user_parser.add_subparsers(dest="subcommand", help="User actions", required=True)

    # user add
    user_add_parser = user_subparsers.add_parser("add", help="Add a new user")
    user_add_parser.add_argument("--name", type=str, required=True, help="User's full name")
    user_add_parser.add_argument("--height", type=float, required=True, help="User's height in cm")
    user_add_parser.add_argument("--weight", type=float, required=True, help="User's weight in kg")

    # user update
    user_update_parser = user_subparsers.add_parser("update", help="Update user profile")
    user_update_parser.add_argument("--user_id", type=str, required=True, help="ID of the user to update")
    user_update_parser.add_argument("--height", type=float, help="New height in cm (optional)")
    user_update_parser.add_argument("--weight", type=float, help="New weight in kg (optional)")

    # user view
    user_view_parser = user_subparsers.add_parser("view", help="View user profile")
    user_view_parser.add_argument("--user_id", type=str, required=True, help="ID of the user to view")

    # --- Log Subparser ---
    log_parser = subparsers.add_parser("log", help="Manage activity logs")
    log_subparsers = log_parser.add_subparsers(dest="subcommand", help="Log actions", required=True)

    # log add_walk
    log_walk_parser = log_subparsers.add_parser("add_walk", help="Log a walking session")
    log_walk_parser.add_argument("--user_id", type=str, required=True, help="User ID")
    log_walk_parser.add_argument("--date", type=str, required=True, help="Date of walk (YYYY-MM-DD)")
    log_walk_parser.add_argument("--steps", type=int, required=True, help="Number of steps taken")
    log_walk_parser.add_argument("--distance", type=float, help="Distance walked in km (optional)")

    # log add_water
    log_water_parser = log_subparsers.add_parser("add_water", help="Log water intake")
    log_water_parser.add_argument("--user_id", type=str, required=True, help="User ID")
    log_water_parser.add_argument("--date", type=str, required=True, help="Date of intake (YYYY-MM-DD)")
    log_water_parser.add_argument("--amount", type=int, required=True, help="Amount of water in ml")

    # log add_sleep
    log_sleep_parser = log_subparsers.add_parser("add_sleep", help="Log a sleep session")
    log_sleep_parser.add_argument("--user_id", type=str, required=True, help="User ID")
    log_sleep_parser.add_argument("--date", type=str, required=True, help="Date of sleep (YYYY-MM-DD)")
    log_sleep_parser.add_argument("--hours", type=float, required=True, help="Hours slept")
    log_sleep_parser.add_argument("--quality", type=str, help="Sleep quality (e.g., Poor, Average, Good) (optional)")

    # log add_workout
    log_workout_parser = log_subparsers.add_parser("add_workout", help="Log a workout session")
    log_workout_parser.add_argument("--user_id", type=str, required=True, help="User ID")
    log_workout_parser.add_argument("--date", type=str, required=True, help="Date of workout (YYYY-MM-DD)")
    log_workout_parser.add_argument("--start", type=str, required=True, help="Start time (HH:MM)")
    log_workout_parser.add_argument("--end", type=str, required=True, help="End time (HH:MM)")
    log_workout_parser.add_argument("--type", dest="type_of_workout", type=str, required=True, help="Type of workout") # Renamed dest to avoid conflict with builtin type
    log_workout_parser.add_argument("--notes", type=str, help="Additional notes (optional)")

    # log view_logs
    log_view_parser = log_subparsers.add_parser("view_logs", help="View logs for a user")
    log_view_parser.add_argument("--user_id", type=str, required=True, help="User ID")
    log_view_parser.add_argument("--type", dest="log_type", type=str, required=True, help="Type of logs to view (walking, water, sleep, workout)") # Renamed dest

    # --- BMI Subparser ---
    bmi_parser = subparsers.add_parser("bmi", help="Calculate BMI")
    bmi_subparsers = bmi_parser.add_subparsers(dest="subcommand", help="BMI actions", required=True)

    # bmi calculate
    bmi_calc_parser = bmi_subparsers.add_parser("calculate", help="Calculate BMI for a user")
    bmi_calc_parser.add_argument("--user_id", type=str, required=True, help="User ID for BMI calculation")

    args = parser.parse_args()

    if args.command == "user":
        if args.subcommand == "add":
            user = add_user(name=args.name, height_cm=args.height, weight_kg=args.weight)
            print("User added successfully:")
            pretty_print(user.to_dict()) # User object has to_dict()
        elif args.subcommand == "update":
            success = update_user_profile(user_id=args.user_id, new_height_cm=args.height, new_weight_kg=args.weight)
            if success:
                print(f"User '{args.user_id}' profile updated.")
            else:
                print(f"Failed to update user '{args.user_id}'. User not found or no new data provided.")
        elif args.subcommand == "view":
            user_profile = get_user_profile(user_id=args.user_id)
            if user_profile:
                pretty_print(user_profile)
            else:
                print(f"User '{args.user_id}' not found.")

    elif args.command == "log":
        if args.subcommand == "add_walk":
            log = record_walking(user_id=args.user_id, date=args.date, steps=args.steps, distance_km=args.distance)
            pretty_print(log)
        elif args.subcommand == "add_water":
            log = record_water(user_id=args.user_id, date=args.date, amount_ml=args.amount)
            pretty_print(log)
        elif args.subcommand == "add_sleep":
            log = record_sleep(user_id=args.user_id, date=args.date, sleep_duration_hours=args.hours, quality=args.quality)
            pretty_print(log)
        elif args.subcommand == "add_workout":
            log = record_workout(user_id=args.user_id, date=args.date, start_time=args.start, end_time=args.end, type_of_workout=args.type_of_workout, notes=args.notes)
            pretty_print(log)
        elif args.subcommand == "view_logs":
            logs = get_user_data(user_id=args.user_id, data_type=args.log_type)
            pretty_print(logs)

    elif args.command == "bmi":
        if args.subcommand == "calculate":
            user_profile = get_user_profile(user_id=args.user_id)
            if user_profile:
                weight_kg = user_profile.get('weight_kg')
                height_cm = user_profile.get('height_cm')
                if weight_kg is not None and height_cm is not None and height_cm > 0:
                    height_m = height_cm / 100.0
                    bmi_value = calculate_bmi(weight_kg=weight_kg, height_m=height_m)
                    print(f"BMI for user '{args.user_id}': {bmi_value:.2f}")
                else:
                    print(f"User '{args.user_id}' found, but weight/height data is missing or invalid for BMI calculation.")
            else:
                print(f"User '{args.user_id}' not found.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
