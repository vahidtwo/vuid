import pytest  # NOQA
from datetime import datetime
from vuid.vuid import VUID, START_EPOC_TIME, generate_vuid, _saturate, _dehydrate

# Test data
TEST_TIMESTAMP = datetime.now().timestamp()
TEST_CODE = "1A2b3C4d5"


def test_generate_vuid():
    """
    Test the `generate_vuid` function to ensure it generates a valid VUID.
    """
    vuid = generate_vuid(TEST_TIMESTAMP)
    assert isinstance(vuid, str)
    assert len(vuid) == 9  # VUIDs should be 9 characters long


def test_vuid_creation():
    """
    Test the `VUID` class initialization with a timestamp.
    """
    vuid = VUID(TEST_TIMESTAMP)
    assert isinstance(vuid.code, str)
    assert len(vuid.code) == 9


def test_vuid_from_code():
    """
    Test creating a `VUID` object from an existing code.
    """
    vuid = VUID.from_code(TEST_CODE)
    assert vuid.code == TEST_CODE


def test_vuid_created_time():
    """
    Test the `created_time` property to ensure it returns the correct timestamp.
    """
    vuid = VUID(TEST_TIMESTAMP)
    created_time = vuid.created_time
    assert isinstance(created_time, datetime)
    assert created_time >= datetime.fromtimestamp(START_EPOC_TIME)


def test_vuid_comparison():
    """
    Test comparison operations between two VUIDs.
    """
    vuid1 = VUID(TEST_TIMESTAMP)
    vuid2 = VUID(TEST_TIMESTAMP + 1)  # Ensure vuid2 is created after vuid1

    assert vuid1 != vuid2
    assert vuid1 < vuid2
    assert vuid1 <= vuid2
    assert vuid2 > vuid1
    assert vuid2 >= vuid1


def test_vuid_hash():
    """
    Test the `__hash__` method to ensure VUIDs can be used in sets and dictionaries.
    """
    vuid1 = VUID.from_code(TEST_CODE)
    vuid2 = VUID.from_code(TEST_CODE)

    assert hash(vuid1) == hash(vuid2)
    assert vuid1 in {vuid1, vuid2}


def test_saturate():
    """
    Test the `_saturate` function to ensure it correctly converts a base-62 string to an integer.
    """
    base62_str = "1A2b3"
    integer = _saturate(base62_str)
    assert isinstance(integer, int)
    assert integer > 0


def test_dehydrate():
    """
    Test the `_dehydrate` function to ensure it correctly converts an integer to a base-62 string.
    """
    integer = 123456789
    base62_str = _dehydrate(integer)
    assert isinstance(base62_str, str)
    assert len(base62_str) > 0


def test_edge_case_timestamp_overflow():
    """
    Test the behavior when the timestamp exceeds the 5-character limit in base-62 encoding.
    """
    overflow_timestamp = START_EPOC_TIME + (62**5)  # This will cause an overflow
    vuid = VUID(overflow_timestamp)
    assert len(vuid.code) == 9  # Ensure the code is still 9 characters long


def test_edge_case_zero_timestamp():
    """
    Test the behavior when the timestamp is equal to the start epoch time.
    """
    vuid = VUID(START_EPOC_TIME)
    assert vuid.code.startswith("0")  # The base-62 representation of 0 is "0"


def test_edge_case_empty_code():
    """
    Test the behavior when an empty code is passed to `VUID.from_code`.
    """
    with pytest.raises(ValueError):
        VUID.from_code("")


def test_edge_case_invalid_code_length():
    """
    Test the behavior when a code with an invalid length is passed to `VUID.from_code`.
    """
    with pytest.raises(ValueError):
        VUID.from_code("12345678")  # Code length exceeds 9 characters


def test_edge_case_negative_timestamp():
    """
    Test the behavior when a negative timestamp is passed to `VUID`.
    """
    with pytest.raises(ValueError):
        VUID(-1)


def test_edge_case_large_timestamp():
    """
    Test the behavior when a very large timestamp is passed to `VUID`.
    """
    large_timestamp = START_EPOC_TIME + (62**6)  # Extremely large timestamp
    vuid = VUID(large_timestamp)
    assert len(vuid.code) == 9  # Ensure the code is still 9 characters long


def test_edge_case_randomness():
    """
    Test the randomness of the 4-character suffix in the VUID.
    """
    vuid1 = VUID(TEST_TIMESTAMP)
    vuid2 = VUID(TEST_TIMESTAMP)
    assert vuid1.code != vuid2.code  # Ensure the random suffix makes the codes unique
