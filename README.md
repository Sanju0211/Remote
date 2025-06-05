# Fitness Tracker CLI

A command-line application to help you track various aspects of your health and fitness, including:
- Walking (steps and distance)
- Water consumption
- Sleep hours and quality
- Workout timings and types
- Body Mass Index (BMI)

All data is stored locally in JSON files.

## Setup

1.  **Prerequisites**:
    *   Ensure you have Python 3.6 or newer installed on your system. You can download it from [python.org](https://www.python.org/).

2.  **Clone the Repository (Optional)**:
    *   If you have this project as part of a Git repository, clone it to your local machine:
        ```bash
        git clone <repository-url>
        cd <repository-directory>
        ```

3.  **No External Dependencies**:
    *   This application uses only standard Python libraries (`json`, `uuid`, `argparse`, `datetime`, `os`, `unittest`). No additional installation steps like `pip install` are required for these.

## Usage

The application is controlled via the command line using `app.py`. You can see all available commands and options by running:

```bash
python app.py --help
```

This will show main commands like `user`, `log`, and `bmi`. Each main command has subcommands.

### User Management

**1. Add a new user:**
```bash
python app.py user add --name "Your Name" --height 175 --weight 70
```
(Replace 175 with height in cm, 70 with weight in kg)
This will output the new user's details, including their unique `user_id`. **Note this `user_id` for future commands.**

**2. Update user profile (e.g., new weight):**
```bash
python app.py user update --user_id "your_user_id_here" --weight 72
```

**3. View user details:**
```bash
python app.py user view --user_id "your_user_id_here"
```

### Logging Activities

Replace `"your_user_id_here"` with the actual ID of the user. Dates should be in `YYYY-MM-DD` format, times in `HH:MM`.

**1. Record walking:**
```bash
python app.py log add_walk --user_id "your_user_id_here" --date "2023-10-26" --steps 10000 --distance 7.5
```

**2. Record water consumption:**
```bash
python app.py log add_water --user_id "your_user_id_here" --date "2023-10-26" --amount 2000
```
(Amount in ml)

**3. Record sleep:**
```bash
python app.py log add_sleep --user_id "your_user_id_here" --date "2023-10-25" --hours 7.5 --quality "Good"
```

**4. Record a workout:**
```bash
python app.py log add_workout --user_id "your_user_id_here" --date "2023-10-26" --start "18:00" --end "19:00" --type "Running" --notes "Evening run in the park"
```

**5. View logs for a user:**
To view all walking logs for a user:
```bash
python app.py log view_logs --user_id "your_user_id_here" --type "walking"
```
Available log types: `walking`, `water`, `sleep`, `workout`.

### BMI Calculation

**1. Calculate BMI for a user:**
Ensure the user's height and weight are up-to-date.
```bash
python app.py bmi calculate --user_id "your_user_id_here"
```

This will output the user's calculated BMI and a general category (e.g., Normal weight).

## Running Tests

The application includes a suite of unit tests to ensure functionality is working as expected. To run the tests:

1.  Navigate to the root directory of the project in your terminal.
2.  Execute the following command:

    ```bash
    python -m unittest discover -s tests
    ```

    (On some systems, you might need to use `python3` instead of `python`).

This will automatically discover and run all tests located in the `tests` directory.
