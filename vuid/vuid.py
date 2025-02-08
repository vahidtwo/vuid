import datetime
import logging
import random
from typing import TypeVar
import math

CHARSET_DEFAULT = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
START_EPOC_TIME = 1735979648  # datetime(2025, 1, 4, 12, 4, 8)
logger = logging.getLogger(__name__)
UPPERCASE_OFFSET = 55
LOWERCASE_OFFSET = 61
DIGIT_OFFSET = 48

TimeStamp = TypeVar("TimeStamp", int, float)


def _true_ord(char):
    """
    Turns a digit [char] in character representation
    from the number system with base [BASE] into an integer.
    """

    if char.isdigit():
        return ord(char) - DIGIT_OFFSET
    elif "A" <= char <= "Z":
        return ord(char) - UPPERCASE_OFFSET
    elif "a" <= char <= "z":
        return ord(char) - LOWERCASE_OFFSET
    else:
        raise ValueError("%s is not a valid character" % char)


def _true_chr(integer, base: int = 62):
    """
    Turns an integer [integer] into digit in base [BASE]
    as a character representation.
    """
    if integer < 10:
        return chr(integer + DIGIT_OFFSET)
    elif 10 <= integer <= 35:
        return chr(integer + UPPERCASE_OFFSET)
    elif 36 <= integer < 62:
        return chr(integer + LOWERCASE_OFFSET)
    else:
        raise ValueError("%d is not a valid integer in the range of base %d" % (integer, base))


def _saturate(key, base: int = 62) -> int:
    """
    Turn the base [base] number [key] into an integer
    """
    int_sum = 0
    reversed_key = key[::-1]
    for idx, char in enumerate(reversed_key):
        int_sum += _true_ord(char) * int(math.pow(base, idx))
    return int_sum


def _dehydrate(integer, base: int = 62) -> str:
    """
    Turn an integer [integer] into a base [BASE] number
    in string representation
    """
    if integer == 0:
        return "0"

    string = ""
    while integer > 0:
        remainder = integer % base
        string = _true_chr(remainder, base) + string
        integer = int(integer / base)
    return string


def generate_vuid(timestamp: TimeStamp) -> str:
    """
    generate vahid unique id that's can consider it as a unique field
    we use timestamp that decrease from  {START_EPOC_TIME}
    and then convert it to base62 and add 4 random char to it.
    if we don't strip it we can generate 14_776_336 ids per second until *15/jan/2054* with length of 9
    for 1735979648 START_EPOC_TIME
    Returns 9 masalan unique character
    NOTE:
        In my test, I was able to create 1,000,000 * 12 codes in parallel mode
        and generated 11,592,876 unique codes in 14.04 seconds (825,237 per second).
        I also ran the algorithm until the first duplicate was found,
        obtaining approximately 4,000 unique VUIDs for a specific datetime.
    """
    timestamp_delta = timestamp - START_EPOC_TIME
    timestamp_delta_base62 = _dehydrate(int(timestamp_delta)).zfill(5)
    timestamp_delta_base62_length = len(timestamp_delta_base62)
    random_char = "".join(random.choice(CHARSET_DEFAULT) for _ in range(4))
    if timestamp_delta_base62_length > 5:
        # in the case that we cross the '15/jan/2054' the length of timestamp_delta_base62 be 6 char
        logger.critical(
            "timestamp base62 overflow of 5 char plz fix it",
            extra={"timestamp_base64": timestamp_delta_base62},
        )
        timestamp_delta_base62 = timestamp_delta_base62[-5:]
    return f"{timestamp_delta_base62}{random_char}"


class VUID:
    def __init__(self, timestamp: TimeStamp, *, prefix: str = ""):
        if timestamp < 0:
            raise ValueError("timestamp must be positive")
        self.prefix = prefix
        self.code = generate_vuid(timestamp)

    def __str__(self) -> str:
        return f"{self.prefix}{self.code}"

    def __repr__(self) -> str:
        return f'VUID("{self.prefix}{self.code}")'

    def __eq__(self, other) -> bool:
        return self.code == other.code

    def __hash__(self):
        return hash(f"{self.prefix}{self.code}")

    def __lt__(self, other) -> bool:
        return self.code < other.code

    def __le__(self, other) -> bool:
        return self.code <= other.code

    def __gt__(self, other) -> bool:
        return self.code > other.code

    def __ge__(self, other) -> bool:
        return self.code >= other.code

    def __ne__(self, other) -> bool:
        return self.code != other.code

    @property
    def created_time(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(_saturate(self.code[0:5]) + START_EPOC_TIME)

    @classmethod
    def from_code(cls, code: str) -> "VUID":
        if len(code) < 9:
            raise ValueError("code must be gte 9 characters")
        obj = cls.__new__(cls)
        obj.code = code[-9:]
        obj.prefix = code[:-9]
        return obj
