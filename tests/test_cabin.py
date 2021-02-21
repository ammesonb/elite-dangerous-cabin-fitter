"""
Test cabin functions
"""
import pytest

from elite_dangerous_cabin_fitter.cabin import Cabin


def test_invalid_cabin_quality(capsys):
    """
    .
    """
    with pytest.raises(ValueError):
        Cabin(4, "economy")

    printed = capsys.readouterr()
    assert (
        printed.out == "Invalid cabin configuration with class 4 and quality economy\n"
    ), "Expected error prints"

    with pytest.raises(ValueError):
        Cabin(4, "c")

    printed = capsys.readouterr()
    assert (
        printed.out == "Invalid cabin configuration with class 4 and quality c\n"
    ), "Expected error prints"


def test_invalid_cabin_class(capsys):
    """
    .
    """
    with pytest.raises(ValueError):
        Cabin(1, "e")

    printed = capsys.readouterr()
    assert (
        printed.out == "Invalid cabin configuration with class 1 and quality e\n"
    ), "Expected error prints"

    with pytest.raises(ValueError):
        Cabin("6", "e")

    printed = capsys.readouterr()
    assert (
        printed.out == "Invalid cabin configuration with class 6 and quality e\n"
    ), "Expected error prints"


def test_fit_passengers():
    """
    .
    """
    cabin = Cabin(3, "e")
    assert cabin.fit_passengers("e", 4) == 1, "Exact match for passengers is one"
    assert cabin.fit_passengers("e", 2) == 0.5, "Half passengers scales"
    assert cabin.fit_passengers("e", 5) == 0, "Too many passengers fails"
    assert cabin.fit_passengers("b", 1) == 0, "Business can't be in economy"
    assert cabin.fit_passengers("f", 1) == 0, "First class can't be in economy"
    assert cabin.fit_passengers("l", 1) == 0, "Luxury can't be in economy"

    biz_cabin = Cabin(4, "b")
    assert biz_cabin.fit_passengers("e", 3) == 0.25, "Passengers scale across classes"
