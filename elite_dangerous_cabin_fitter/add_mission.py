#!/usr/bin/env python3
"""
Adds missions to the yaml file to save typing
"""
from elite_dangerous_cabin_fitter.mission import Mission


def loop():
    """
    Main loop for prompting answers
    """
    faction = None
    while True:
        faction = prompt(faction)
        if not faction:
            break


def prompt(faction: str = None) -> str:
    """
    Prompt user for inputs
    """
    name = input("Name: ")
    if not name:
        return None
    if not faction:
        faction = input("Faction: ")

    reward = input("Reward: ")
    cabin = input("Cabin class: ")
    passengers = input("Passenger count: ")

    write_mission_file(Mission(name, faction, reward, cabin, passengers))

    return faction


def write_mission_file(mission: Mission):
    """
    Actually record results in the mission file
    """
    with open("missions.yaml", "a") as mission_file:
        mission_file.write(mission.yaml())


if __name__ == "__main__":
    loop()
