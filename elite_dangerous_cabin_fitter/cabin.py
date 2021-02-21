"""
Contains the definition of a cabin, and scoring relative to a requested passenger group
"""
from elite_dangerous_cabin_fitter.cabin_quality import CabinQuality
from elite_dangerous_cabin_fitter import utils


# pylint: disable=too-few-public-methods
class Cabin:
    """
    A cabin on a ship
    """

    def __init__(self, cabin_class: int, cabin_quality: CabinQuality):
        self.cclass = cabin_class
        self.quality = cabin_quality
        self.capacity = (
            utils.get_cabin_capacities().get(cabin_class, {}).get(cabin_quality)
        )
        if not self.capacity:
            print(
                "Invalid cabin configuration with class "
                f"{cabin_class} and quality {cabin_quality}"
            )
            raise ValueError("Invalid cabin configuration")

        self._cabin_scores = utils.get_cabin_scores()[self.quality]

    def fit_passengers(
        self, min_cabin_quality: CabinQuality, passenger_count: int
    ) -> float:
        """
        Score how well a group of passengers fit this cabin
        """
        return (
            # Cannot use this cabin if insufficient capacity
            0
            if passenger_count > self.capacity
            # Otherwise, check the compatibility score for quality, and multiple by
            # the ratio of how full this cabin will be for this group
            else (
                self._cabin_scores[min_cabin_quality]
                * (passenger_count / self.capacity)
            )
        )
