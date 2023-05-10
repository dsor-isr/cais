import pytest
from profiles import profiles

TEST_PROFILES = ["TEST_PROFILE", "SECOND_TEST_PROFILE", "THIRD_TEST_PROFILE", "FOURTH_TEST_PROFILE", "FIFTH_TEST_PROFILE"]
INVALID_LIST = [None]
INVALID_TUPLE = (3, 4, 5)
EMPTY_STRING = ""
LIST_OR_TUPLE_EXCEPTION = "Files must be a list or tuple"
LIST_OR_TUPLE_OF_STRINGS_EXCEPTION = "Files must be a list or tuple of strings"
FILES_CANT_BE_EMPTY_EXCEPTION = "Files can't be empty"
FILES_CANT_BE_NONE_OR_EMPTY_STRINGS = "Files can't contain None/Null or empty strings"

UPPER_CASE_BASIC_FILTER_TEST = ['DEPTHCELL', 'GPS', 'IMU', 'INSIDEPRESSURE', 'USBL', 'ALTIMETER', 'BATMONIT']
LOWER_CASE_BASIC_FILTER_TEST = ['depthcell', 'gps', 'imu', 'insidepressure', 'usbl', 'altimeter', 'batmonit']
MIXED_CASE_BASIC_FILTER_TEST = ['DepthCell', 'Gps', 'Imu', 'InsidePressure', 'Usbl', 'Altimeter', 'BatMonit']
COMPLEX_REGEC_FILTER_TEST_CASE = ['_DepthCell', 'GPSGPS', '!3?Imu', '##USbL##']


def test_filter_invalid_input_type():
    profile = profiles.Profile(TEST_PROFILES[0], True, False, True, True, True, False, False, True)

    with pytest.raises(TypeError) as e:
        profile.filter(None)

    assert LIST_OR_TUPLE_EXCEPTION in str(e.value)

    with pytest.raises(TypeError) as e:
        profile.filter(3)

    assert LIST_OR_TUPLE_EXCEPTION in str(e.value)

    with pytest.raises(TypeError) as e:
        profile.filter(TEST_PROFILES[0])

    assert LIST_OR_TUPLE_EXCEPTION in str(e.value)

    with pytest.raises(TypeError) as e:
        profile.filter(INVALID_LIST)

    assert LIST_OR_TUPLE_OF_STRINGS_EXCEPTION in str(e.value)

    with pytest.raises(TypeError) as e:
        profile.filter(INVALID_TUPLE)
    
    assert LIST_OR_TUPLE_OF_STRINGS_EXCEPTION in str(e.value)


def test_filter_empty_input():
    profile = profiles.Profile(TEST_PROFILES[0], True, False, True, True, True, False, False, True)

    with pytest.raises(ValueError) as e:
        profile.filter([])

    assert FILES_CANT_BE_EMPTY_EXCEPTION in str(e.value)

    with pytest.raises(ValueError) as e:
        profile.filter(())

    assert FILES_CANT_BE_EMPTY_EXCEPTION in str(e.value)


def test_filter_empty_string():
    profile = profiles.Profile(TEST_PROFILES[0], True, False, True, True, True, False, False, True)

    with pytest.raises(ValueError) as e:
        profile.filter([EMPTY_STRING])

    assert FILES_CANT_BE_NONE_OR_EMPTY_STRINGS in str(e.value)

    with pytest.raises(ValueError) as e:
        profile.filter((EMPTY_STRING,))

    assert FILES_CANT_BE_NONE_OR_EMPTY_STRINGS in str(e.value)


def test_filter_everything():
    profile = profiles.Profile(TEST_PROFILES[0], True, True, True, True, True, True, True, True)

    assert profile.filter(UPPER_CASE_BASIC_FILTER_TEST) == []
    assert profile.filter(LOWER_CASE_BASIC_FILTER_TEST) == []
    assert profile.filter(MIXED_CASE_BASIC_FILTER_TEST) == []


def test_dont_filter_anything():
    profile = profiles.Profile(TEST_PROFILES[0], False, False, False, False, False, False, False, True)

    assert profile.filter(UPPER_CASE_BASIC_FILTER_TEST) == UPPER_CASE_BASIC_FILTER_TEST
    assert profile.filter(LOWER_CASE_BASIC_FILTER_TEST) == LOWER_CASE_BASIC_FILTER_TEST
    assert profile.filter(MIXED_CASE_BASIC_FILTER_TEST) == MIXED_CASE_BASIC_FILTER_TEST


def test_filter_some_flags():
    profile = profiles.Profile(TEST_PROFILES[0], True, False, True, True, True, False, False, True)

    assert profile.filter(UPPER_CASE_BASIC_FILTER_TEST) == ['INSIDEPRESSURE', 'ALTIMETER', 'BATMONIT']
    assert profile.filter(LOWER_CASE_BASIC_FILTER_TEST) == ['insidepressure', 'altimeter', 'batmonit']
    assert profile.filter(MIXED_CASE_BASIC_FILTER_TEST) == ['InsidePressure', 'Altimeter', 'BatMonit']

    profile = profiles.Profile(TEST_PROFILES[0], False, True, False, False, False, True, True, True)

    assert profile.filter(UPPER_CASE_BASIC_FILTER_TEST) == ['DEPTHCELL', 'GPS', 'IMU', 'USBL']
    assert profile.filter(LOWER_CASE_BASIC_FILTER_TEST) == ['depthcell', 'gps', 'imu', 'usbl']
    assert profile.filter(MIXED_CASE_BASIC_FILTER_TEST) == ['DepthCell', 'Gps', 'Imu', 'Usbl']


def test_non_simple_regex():
    profile = profiles.Profile(TEST_PROFILES[0], True, True, True, True, True, True, True, True)

    assert profile.filter(COMPLEX_REGEC_FILTER_TEST_CASE) == []

    profile = profiles.Profile(TEST_PROFILES[0], False, False, False, False, False, False, False, True)

    assert profile.filter(COMPLEX_REGEC_FILTER_TEST_CASE) == COMPLEX_REGEC_FILTER_TEST_CASE