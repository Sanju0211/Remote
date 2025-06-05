import uuid

class User:
    def __init__(self, name: str, height_cm: float, weight_kg: float):
        self.user_id = str(uuid.uuid4())
        self.name = name
        self.height_cm = height_cm
        self.weight_kg = weight_kg

    def to_dict(self) -> dict:
        return self.__dict__

class WalkingLog:
    def __init__(self, user_id: str, date: str, steps: int, distance_km: float = None):
        self.log_id = str(uuid.uuid4())
        self.user_id = user_id
        self.date = date
        self.steps = steps
        self.distance_km = distance_km

    def to_dict(self) -> dict:
        return self.__dict__

class WaterLog:
    def __init__(self, user_id: str, date: str, amount_ml: int):
        self.log_id = str(uuid.uuid4())
        self.user_id = user_id
        self.date = date
        self.amount_ml = amount_ml

    def to_dict(self) -> dict:
        return self.__dict__

class SleepLog:
    def __init__(self, user_id: str, date: str, sleep_duration_hours: float, quality: str = None):
        self.log_id = str(uuid.uuid4())
        self.user_id = user_id
        self.date = date
        self.sleep_duration_hours = sleep_duration_hours
        self.quality = quality

    def to_dict(self) -> dict:
        return self.__dict__

class WorkoutLog:
    def __init__(self, user_id: str, date: str, start_time: str, end_time: str, type_of_workout: str, notes: str = None):
        self.log_id = str(uuid.uuid4())
        self.user_id = user_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.type_of_workout = type_of_workout
        self.notes = notes

    def to_dict(self) -> dict:
        return self.__dict__
