from enum import IntEnum
from typing import List, Tuple, Optional


class BaseIntEnum(IntEnum):
    @classmethod
    def get_choices(cls) -> List[Tuple]:
        return [(item.value, item.name) for item in cls]

    @classmethod
    def get_string_for_value(cls, value: int) -> Optional[str]:
        """
        This class method returns the string representation of an enum integer value if it exists in the enum.

        Eg:
        Region.get_string_for_value(1) returns the string "UK"
        Parameter.get_string_for_value(1) returns the string "MAX_TEMP"

        """
        for item in cls:
            if item.value == value:
                return item.name
        return None

    @classmethod
    def get_obj_for_string(cls, type: str) -> "BaseIntEnum":
        """
        This method returns the enum object for the given string representation.

        Eg:
        Region.get_obj_for_string("ENGLAND") returns Region.ENGLAND obj
        Parameter.get_obj_for_string("MAX_TEMP") returns Parameter.MAX_TEMP obj

        Throws KeyError if the input string is invalid
        """
        return cls.__members__[type]


class Region(BaseIntEnum):
    UK = 1

    ENGLAND = 2
    ENGLAND_N = 3
    ENGLAND_S = 4
    ENGLAND_E_AND_NE = 5
    ENGLAND_NW_OR_WALES_N = 6
    ENGLAND_SW_OR_WALES_S = 7
    ENGLAND_SE_OR_CENTRAL_S = 8
    ENGLAND_AND_WALES = 8
    WALES = 9

    SCOTLAND = 10
    SCOTLAND_N = 11
    SCOTLAND_E = 12
    SCOTLAND_W = 13

    NOTHERN_IRELAND = 14

    MIDLANDS = 15
    EAST_ANGLIA = 16


class Parameter(BaseIntEnum):
    MAX_TEMP = 1
    MIN_TEMP = 2
    MEAN_TEMP = 3
    SUNSHINE = 4
    RAIN_DAYS_GREATER_OR_EQUAL_TO_1_MM = 5  # Rain days ≥ 1.0mm

    DAYS_OF_AIR_FROST = 6


WEATHER_DATA_SCHEMA = {
    "year": None,
    "jan": None,
    "feb": None,
    "mar": None,
    "apr": None,
    "may": None,
    "jun": None,
    "jul": None,
    "aug": None,
    "sep": None,
    "oct": None,
    "nov": None,
    "dec": None,
    "win": None,
    "spr": None,
    "sum": None,
    "aut": None,
    "ann": None,
}


MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
SEASONS = ["win", "spr", "sum", "aut"]
YEAR = "ann"


RANK_ORDER = "RANK_ORDER"
YEAR_ORDER = "YEAR_ORDER"
