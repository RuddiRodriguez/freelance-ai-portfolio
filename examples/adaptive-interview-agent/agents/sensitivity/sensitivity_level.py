from enum import Enum


class SensitivityLevel(str, Enum):
    NOT_SENSITIVE = "NotSensitive"
    MODERATE = "Moderate"
    SENSITIVE = "Sensitive"
    INAPPLICABLE = "Inapplicable"
