"""
Various utilities
"""
import functools
from typing import Union, List, Dict

import yaml

BASE_DIRECTORY = "elite_dangerous_cabin_fitter"


def get_cabin_data() -> List[dict]:
    """
    Return the raw cabin data
    """
    return load_yaml_from_file(f"{BASE_DIRECTORY}/cabins.yaml")


def get_mission_data() -> List[dict]:
    """
    Return the raw mission data
    """
    return load_yaml_from_file(f"{BASE_DIRECTORY}/missions.yaml")


def get_cabin_capacities() -> Dict[str, int]:
    """
    Gets a list of the cabin capacities
    """
    return load_yaml_from_file(f"{BASE_DIRECTORY}/conf/cabin_capacity.yaml")


def get_cabin_scores() -> Dict[str, int]:
    """
    Gets a list of the cabin capacities
    """
    return load_yaml_from_file(f"{BASE_DIRECTORY}/conf/cabin_passenger_scores.yaml")


def load_yaml_from_file(file_path: str) -> Union[list, dict]:
    """
    Loads yaml data from a given file
    """
    with open(file_path) as file_handle:
        return yaml.load(file_handle, Loader=yaml.FullLoader)


def counter_wrapper(func):
    """
    Adds a "counter" variable to the function, incrementing each time it is called
    """

    @functools.wraps(func)  # pragma: no mutate
    def execute(*args, **kwargs):
        """
        Adds a "counter" variable to the function, incrementing each time it is called
        """
        execute.counter += 1
        return func(*args, **kwargs)

    execute.counter = 0

    return execute


def update_mission_file(mission_yaml: str):
    """
    .
    """
    mission_header = read_mission_file().split("\n-\n")[0]
    write_mission_file(mission_header + "\n" + mission_yaml)


def read_mission_file() -> str:
    """
    Gets mission file content
    """
    return open(f"{BASE_DIRECTORY}/missions.yaml", "r").read()


def write_mission_file(data: str):
    """
    .
    """
    with open(f"{BASE_DIRECTORY}/missions.yaml", "w") as mission_file:
        mission_file.write(data)
