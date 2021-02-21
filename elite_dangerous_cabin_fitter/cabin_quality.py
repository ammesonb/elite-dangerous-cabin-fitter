"""
Cabin qualities
"""
import enum

class CabinQuality(enum.Enum):
    """
    List of cabin qualities
    """
    ECONOMY = "e"
    BUSINESS = "b"
    FIRST_CLASS = "f"
    LUXURY = "l"
