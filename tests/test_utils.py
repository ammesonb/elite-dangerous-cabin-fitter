"""
Tests for utilities
"""
from elite_dangerous_cabin_fitter import utils


def test_load_yaml_file():
    """
    .
    """
    assert utils.load_yaml_from_file("tests/test.yaml") == {
        6: {"b": 1, "e": 0.5},
        5: {"e": 0.5, "f": 0.25},
    }


def test_update_missions(monkeypatch):
    """
    .
    """
    new_mission_yaml = (
        "-\n"
        "  name: mission1\n"
        "  faction: faction1\n"
        "  reward: 2\n"
        "  min-quality: b\n"
        "  passengers: 3\n"
        "-\n"
        "  name: mission2\n"
        "  faction: faction2\n"
        "  reward: 1.5\n"
        "  min-quality: f\n"
        "  passengers: 2\n"
    )

    @utils.counter_wrapper
    def read():
        """
        .
        """
        return (
            "a header\nsome text\n"
            "-\n"
            "  name: foo\n"
            "  faction: bar\n"
            "  reward: 1\n"
            "  min-quality: e\n"
            "  passengers: 4\n"
        )

    @utils.counter_wrapper
    def write(data):
        """
        .
        """
        assert data == (
            "a header\nsome text\n" + new_mission_yaml
        ), "Mission data correct"

    monkeypatch.setattr(utils, "read_mission_file", read)
    monkeypatch.setattr(utils, "write_mission_file", write)
    utils.update_mission_file(new_mission_yaml)
    assert read.counter == 1, "Mission file read"
    assert write.counter == 1, "Mission file written"
