"""
Test the optimization of cabins
"""
import pytest

from elite_dangerous_cabin_fitter import optimize_passengers, utils
from elite_dangerous_cabin_fitter.cabin import Cabin
from elite_dangerous_cabin_fitter.mission import Mission


def test_get_cabins(monkeypatch):
    """
    .
    """
    _orig_load = utils.load_yaml_from_file

    @utils.counter_wrapper
    def fake_load(path):
        """
        .
        """
        return (
            _orig_load(path)
            if not path.endswith("cabins.yaml")
            else [{"class": 3, "quality": "e"}, {"class": 4, "quality": "b"}]
        )

    monkeypatch.setattr(utils, "load_yaml_from_file", fake_load)

    cabins = optimize_passengers.load_cabins()
    assert (
        fake_load.counter == 5
    ), "YAML loaded for cabins, plus score and capacity for each"
    assert cabins[0].cclass == 3 and cabins[0].quality == "e", "First cabin correct"
    assert cabins[1].cclass == 4 and cabins[1].quality == "b", "Second cabin correct"


def test_get_missions(monkeypatch):
    """
    .
    """
    test_missions = [
        {
            "name": "Jane",
            "faction": 1,
            "reward": 1.5,
            "min-quality": "e",
            "passengers": 3,
        },
        {
            "name": "John",
            "faction": "SC",
            "reward": 0.24,
            "min-quality": "b",
            "passengers": 1,
        },
    ]

    attribute_map = {"min-quality": "min_quality", "passengers": "passenger_count"}

    @utils.counter_wrapper
    def fake_load(path):
        """
        .
        """
        assert path.endswith("missions.yaml"), "Missions YAML only file loaded"
        return test_missions

    monkeypatch.setattr(utils, "load_yaml_from_file", fake_load)

    missions = optimize_passengers.load_missions()
    assert fake_load.counter == 1, "YAML loaded for missions"

    idx = 0
    for mission in test_missions:
        for attr, value in mission.items():
            assert (
                getattr(missions[idx], attribute_map.get(attr, attr)) == value
            ), f"Mission f{idx} has correct value for {attr}"

        idx += 1


def test_duplicate_missions(capsys):
    """
    .
    """
    mission_one = Mission("name", "faction", 1.2, "e", 4)
    mission_two = Mission("name2", "faction", 1.3, "b", 4)
    mission_three = Mission("name", "faction2", 1.4, "e", 4)
    mission_four = Mission("name2", "faction2", 1.5, "l", 4)

    assert not optimize_passengers.has_duplicate_missions(
        [
            mission_one,
            mission_two,
            mission_three,
            mission_four,
        ]
    ), "No duplicates"

    printed = capsys.readouterr()
    assert printed.out == "", "Nothing printed"

    assert optimize_passengers.has_duplicate_missions(
        [mission_one, mission_two, mission_three, mission_four, mission_two]
    ), "Has single duplicate"

    printed = capsys.readouterr()
    assert printed.out == (
        "At least two missions share a faction and name!\n" " - faction - name2\n"
    ), "Single collision printed correctly"

    assert optimize_passengers.has_duplicate_missions(
        [
            mission_one,
            mission_two,
            mission_three,
            mission_four,
            mission_two,
            mission_three,
        ]
    ), "Has multiple duplicate"

    printed = capsys.readouterr()
    assert printed.out == (
        "At least two missions share a faction and name!\n"
        " - faction - name2\n"
        " - faction2 - name\n"
    ), "Multiple collision printed correctly"


def test_assign_missions():
    """
    .
    """
    mission_one = Mission("name1", "faction1", 1.23, "e", 3)
    cabin_one = Cabin(3, "b")

    mission_two = Mission("name2", "faction1", 0.4, "b", 3)
    cabin_two = Cabin(5, "f")

    mission_three = Mission("name1", "faction2", 3, "e", 4)
    cabin_three = Cabin(5, "e")

    results = optimize_passengers.assign_missions_to_cabins(
        [mission_one, mission_two, mission_three], [cabin_three, cabin_two, cabin_one]
    )

    assert results == {
        mission_one: cabin_two,
        mission_two: cabin_one,
        mission_three: cabin_three,
    }, "Expected assignment returned"


def test_print_result(capsys):
    """
    .
    """
    mission_one = Mission("name1", "faction1", 1.23, "e", 3)
    cabin_one = Cabin(3, "b")

    mission_two = Mission("name2", "faction1", 0.4, "b", 3)
    cabin_two = Cabin(5, "f")

    mission_three = Mission("name1", "faction2", 3, "e", 4)
    cabin_three = Cabin(5, "e")

    optimize_passengers.print_results(
        {
            mission_one: cabin_one,
            mission_two: cabin_two,
            mission_three: cabin_three,
        }
    )
    printed = capsys.readouterr()
    expected_table_lines = [
        "Faction    Name    Cabin Class   Cabin Quality   Algorithm Score   Reward",
        "=========================================================================",
        "faction1   name1   3             b               0.500             1.230 ",
        "faction1   name2   5             f               0.250             0.400 ",
        "faction2   name1   5             e               0.250             3.000 ",
        "",
    ]
    actual_table_lines = printed.out.split("\n")

    line = 0
    for expected, actual in zip(expected_table_lines, actual_table_lines):
        assert actual == expected, f"Table line {line} correct"
        line += 1

    assert len(expected_table_lines) == len(
        actual_table_lines
    ), "Same number of lines in tables"


def test_optimize_failures(monkeypatch):
    """
    .
    """
    monkeypatch.setattr(optimize_passengers, "load_cabins", lambda: [])
    with pytest.raises(ValueError) as exception:
        optimize_passengers.optimize()
        assert (
            str(exception) == "No cabins provided! Exiting"
        ), "Cabins exception correct"

    monkeypatch.setattr(optimize_passengers, "load_cabins", lambda: ["cabin"])
    monkeypatch.setattr(optimize_passengers, "load_missions", lambda: [])
    with pytest.raises(ValueError) as exception:
        optimize_passengers.optimize()
        assert (
            str(exception) == "No missions provided! Exiting"
        ), "Missions exception correct"

    monkeypatch.setattr(optimize_passengers, "load_missions", lambda: ["mission"])
    monkeypatch.setattr(
        optimize_passengers, "has_duplicate_missions", lambda missions: True
    )
    with pytest.raises(ValueError) as exception:
        optimize_passengers.optimize()
        assert (
            str(exception) == "No missions provided! Exiting"
        ), "Missions exception correct"


def test_optimize_success(capsys, monkeypatch):
    """
    .
    """

    @utils.counter_wrapper
    def load_cabins():
        """
        .
        """
        return ["cabin"]

    @utils.counter_wrapper
    def load_missions():
        """
        .
        """
        return ["mission"]

    @utils.counter_wrapper
    def has_collision(missions):
        """
        .
        """
        return False

    @utils.counter_wrapper
    def assign_missions(missions, cabins):
        """
        .
        """
        return {}

    @utils.counter_wrapper
    def print_results(missions):
        """
        .
        """

    monkeypatch.setattr(optimize_passengers, "load_cabins", load_cabins)
    monkeypatch.setattr(optimize_passengers, "load_missions", load_missions)
    monkeypatch.setattr(optimize_passengers, "has_duplicate_missions", has_collision)
    monkeypatch.setattr(
        optimize_passengers, "assign_missions_to_cabins", assign_missions
    )
    monkeypatch.setattr(optimize_passengers, "print_results", print_results)

    optimize_passengers.optimize()
    assert load_cabins.counter == 1, "Cabins loaded"
    assert load_missions.counter == 1, "Missions loaded"
    assert has_collision.counter == 1, "Mission collisions checked"
    assert assign_missions.counter == 1, "Missions assigned"
    assert print_results.counter == 1, "Results printed"

    printed = capsys.readouterr()
    assert printed.out == "\n".join(
        [
            "Loading cabins...",
            "Loading missions...",
            "Validating missions...",
            "Assigning missions...",
            "",
            "Optimal mission assignment:\n",
        ]
    )
