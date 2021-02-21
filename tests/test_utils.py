"""
Tests for utilities
"""
from elite_dangerous_cabin_fitter import utils

def test_load_yaml_file():
    """
    .
    """
    assert utils.load_yaml_from_file("tests/test.yaml") == {
        6: {
            "b": 1,
            "e": 0.5
        },
        5: {
            "e": 0.5,
            "f": 0.25
        },
    }
