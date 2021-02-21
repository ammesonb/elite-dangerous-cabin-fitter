"""
Tests mission adder
"""

from elite_dangerous_cabin_fitter import add_mission, utils


def test_loop(monkeypatch):
    """
    .
    """
    # pylint: disable=unused-argument
    @utils.counter_wrapper
    def prompt(faction=None):
        """
        .
        """
        return "foo" if prompt.counter == 1 else None

    monkeypatch.setattr(add_mission, "prompt", prompt)
    add_mission.loop()
    assert prompt.counter == 2, "Prompt called twice"


def test_prompt(monkeypatch):
    """
    .
    """
    # pylint: disable=unused-argument
    @utils.counter_wrapper
    def empty(text=None):
        """
        .
        """
        return ""

    # Does have input
    # pylint: disable=no-member
    monkeypatch.setitem(add_mission.__builtins__, "input", empty)
    assert add_mission.prompt() is None, "Exits with none if no name provided"

    @utils.counter_wrapper
    def fields(text=None):
        """
        .
        """
        return "something"

    @utils.counter_wrapper
    def write_missions(mission):
        """
        .
        """

    monkeypatch.setitem(add_mission.__builtins__, "input", fields)
    monkeypatch.setattr(add_mission, "write_mission_file", write_missions)

    assert add_mission.prompt() == "something", "Exits with faction on success"
    assert fields.counter == 5, "All 5 data points requested"
    assert write_missions.counter == 1, "Missions written"
