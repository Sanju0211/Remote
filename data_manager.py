import json
from typing import Any, Union, List, Dict

def save_data(data: Union[List[Any], Dict[str, Any]], filename: str) -> None:
    """
    Saves the given data to a file in JSON format.

    Args:
        data (Union[List[Any], Dict[str, Any]]): The data to save,
                                                  typically a list or dictionary.
        filename (str): The name of the file to save the data to.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Error saving data to {filename}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while saving data to {filename}: {e}")

def load_data(filename: str) -> Union[List[Any], Dict[str, Any]]:
    """
    Loads data from a JSON file.

    Args:
        filename (str): The name of the file to load data from.

    Returns:
        Union[List[Any], Dict[str, Any]]: The loaded data (list or dict).
                                          Returns an empty list if the file is not found,
                                          is not valid JSON, or if another I/O error occurs.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        # It's common to start with an empty list if the file doesn't exist yet
        return []
    except json.JSONDecodeError:
        print(f"Error: The file {filename} does not contain valid JSON. Returning empty list.")
        return []
    except IOError as e:
        print(f"Error loading data from {filename}: {e}. Returning empty list.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while loading data from {filename}: {e}. Returning empty list.")
        return []
