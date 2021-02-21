"""
Checks mission functions
"""
from elite_dangerous_cabin_fitter.mission import Mission


def test_get_scaled_reward():
    """
    .
    """
    mission = Mission("test", "faction", 125, "b", 6)
    assert mission.get_scaled_reward(0.5) == 62.5, "Expected mission reward returned"


def test_name():
    """
    .
    """
    mission = Mission("test", "faction", 125, "b", 6)
    assert str(mission) == "faction - test", "String version of mission is correct"


def test_yaml():
    """
    .
    """
    mission = Mission("test", "faction", 125, "b", 6)
    assert mission.yaml() == "\n".join(
        [
            "-",
            "  name: test",
            "  faction: faction",
            "  reward: 125",
            "  min-quality: b",
            "  passengers: 6",
            "\n",
        ]
    ), "YAML for mission correct"
