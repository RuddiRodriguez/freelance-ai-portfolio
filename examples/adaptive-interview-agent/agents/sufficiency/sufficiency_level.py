from enum import Enum


class SufficiencyLevel(str, Enum):
    INSUFFICIENT = "Insufficient"
    SOMEWHAT_INSUFFICIENT = "SomewhatInsufficient"
    MODERATE = "Moderate"
    SOMEWHAT_SUFFICIENT = "SomewhatSufficient"
    SUFFICIENT = "Sufficient"
    INAPPLICABLE = "Inapplicable"
