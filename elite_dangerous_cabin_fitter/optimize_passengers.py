#!/usr/bin/env python3
"""
Runs the optimization of passenger missions for a given cabin configuration
"""
import sys
from typing import List, Dict

from texttable import Texttable

from elite_dangerous_cabin_fitter import utils
from elite_dangerous_cabin_fitter.cabin import Cabin
from elite_dangerous_cabin_fitter.mission import Mission


def optimize():
    """
    Optimize cabins for missions
    """
    print("Loading cabins...")
    cabins = load_cabins()
    if not cabins:
        raise ValueError("No cabins provided! Exiting")
    print("Loading missions...")
    missions = load_missions()
    if not missions:
        raise ValueError("No missions provided! Exiting")

    print("Validating missions...")
    if has_duplicate_missions(missions):
        raise ValueError("Duplicate missions detected!")

    print("Assigning missions...")
    assigned_missions = assign_missions_to_cabins(missions, cabins)

    print("")
    print("Optimal mission assignment:")
    print_results(assigned_missions)

    if should_update_mission_list():
        print("")
        print("Updating mission list...")
        update_mission_list(missions, assigned_missions)


def should_update_mission_list() -> bool:
    """
    Check if argument passed in to update mission list
    after calculating optimal missions
    """
    args = get_sys_args()
    if len(args) == 1:
        update = input("Remove these from missions? (y/N)").lower() == "y"
    else:
        update = args[1] == "update"

    return update


def get_sys_args() -> List[str]:
    """
    Wraps getting system arguments
    """
    return sys.argv


def update_mission_list(missions: List[Mission], assigned_missions: List[Mission]):
    """
    Updates the mission list to remove the ones that were assigned
    """
    remaining_missions = list(
        filter(lambda mission: mission not in assigned_missions, missions)
    )
    mission_yaml = ""
    for mission in remaining_missions:
        mission_yaml += mission.yaml()

    utils.update_mission_file(mission_yaml)


def load_cabins() -> List[Cabin]:
    """
    Load cabins from yaml file
    """
    cabins = []
    cabin_data = utils.get_cabin_data()
    for cabin in cabin_data:
        cabins.append(Cabin(cabin["class"], cabin["quality"]))

    return cabins


def load_missions() -> List[Mission]:
    """
    Load missions from yaml file
    """
    missions = []
    mission_data = utils.get_mission_data()
    for mission in mission_data:
        missions.append(
            Mission(
                mission["name"],
                mission["faction"],
                mission["reward"],
                mission["min-quality"],
                mission["passengers"],
            )
        )

    return missions


def has_duplicate_missions(missions: List[Mission]) -> bool:
    """
    Raises an error if duplicate missions found
    """
    mission_count = len(missions)
    collisions = []
    for one in range(mission_count):
        mission_one = str(missions[one])
        for two in range(one + 1, mission_count):
            if mission_one == str(missions[two]) and mission_one not in collisions:
                collisions.append(mission_one)

    if collisions:
        print("At least two missions share a faction and name!")
        for collision in collisions:
            print(f" - {collision}")

    return bool(collisions)


def assign_missions_to_cabins(
    missions: List[Mission], cabins: List[Cabin]
) -> List[Mission]:
    """
    Finds the mission best fit for each cabin
    Optimizes for each cabin, so naively will assume the best mission for each cabin
    should be reserved immediately, without doing
    any sort of backtracking or cross-checking

    Returns a list of missions that were assigned
    """
    assigned_missions = {}  # type: Dict[Mission, Cabin]
    for cabin in cabins:
        best_mission = None
        best_score = 0
        for mission in missions:
            mission_score = mission.get_scaled_reward(
                cabin.fit_passengers(mission.min_quality, mission.passenger_count)
            )
            # If score is the same as the best, then the mission must have
            # EXACTLY the same requirements - min quality and passenger count, since
            # there are no other variables between missions which would affect the score
            if mission_score > best_score:
                best_mission = mission
                best_score = mission_score

        assigned_missions[best_mission] = cabin
        missions.remove(best_mission)

    return assigned_missions


def print_results(missions: Dict[Mission, Cabin]) -> None:
    """
    Prints the result of mission assignments
    """
    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.set_cols_dtype(["t", "t", "i", "t", "f", "f"])
    table.add_rows(
        [
            [
                "Faction",
                "Name",
                "Cabin Class",
                "Cabin Quality",
                "Algorithm Score",
                "Reward",
            ]
        ]
    )

    for mission, cabin in missions.items():
        table.add_row(
            [
                mission.faction,
                mission.name,
                cabin.cclass,
                cabin.quality,
                cabin.fit_passengers(mission.min_quality, mission.passenger_count),
                mission.reward,
            ]
        )

    print(table.draw())


if __name__ == "__main__":
    optimize()
