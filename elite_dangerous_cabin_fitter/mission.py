"""
A mission which can be accepted
"""
from elite_dangerous_cabin_fitter.cabin_quality import CabinQuality


class Mission:
    """
    A mission
    """

    def __init__(
        self,
        name: str,
        faction: str,
        reward: float,
        min_cabin_quality: CabinQuality,
        passenger_count: int,
    ):
        self.name = name
        self.faction = faction
        self.reward = reward
        self.min_quality = min_cabin_quality
        self.passenger_count = passenger_count

    def get_scaled_reward(self, cabin_score: float) -> float:
        """
        Provide the scaled reward for a given fit to a cabin
        """
        return self.reward * cabin_score

    def __str__(self) -> str:
        """
        String version of this
        """
        return f"{self.faction} - {self.name}"
