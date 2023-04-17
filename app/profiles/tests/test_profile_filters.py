import pytest
from profiles import profiles

TEST_PROFILES = ["TEST_PROFILE", "SECOND_TEST_PROFILE", "THIRD_TEST_PROFILE", "FOURTH_TEST_PROFILE", "FIFTH_TEST_PROFILE"]
INVALID_LIST = [None]
INVALID_TUPLE = (3, 4, 5)
EMPTY_STRING = ""



def test_filter_invalid_input_type():
    profile = profiles.Profile(TEST_PROFILES[0], True, False, True, True, True, False, False)

    with pytest.raises(TypeError) as e:
        profile.filter(None)

    assert "Files must be a list or tuple" in str(e.value)

    with pytest.raises(TypeError) as e:
        profile.filter(3)

    assert "Files must be a list or tuple" in str(e.value)

    with pytest.raises(TypeError) as e:
        profile.filter(TEST_PROFILES[0])

    assert "Files must be a list or tuple" in str(e.value)

    with pytest.raises(TypeError) as e:
        profile.filter(INVALID_LIST)

    assert "Files must be a list or tuple of strings" in str(e.value)

    with pytest.raises(TypeError) as e:
        profile.filter(INVALID_TUPLE)
    
    assert "Files must be a list or tuple of strings" in str(e.value)


def test_filter_empty_input():
    profile = profiles.Profile(TEST_PROFILES[0], True, False, True, True, True, False, False)

    with pytest.raises(ValueError) as e:
        profile.filter([])

    assert "Files can't be empty" in str(e.value)

    with pytest.raises(ValueError) as e:
        profile.filter(())

    assert "Files can't be empty" in str(e.value)


def test_filter_empty_string():
    profile = profiles.Profile(TEST_PROFILES[0], True, False, True, True, True, False, False)

    with pytest.raises(ValueError) as e:
        profile.filter([EMPTY_STRING])

    assert "Files can't contain None/Null or empty strings" in str(e.value)

    with pytest.raises(ValueError) as e:
        profile.filter((EMPTY_STRING,))

    assert "Files can't contain None/Null or empty strings" in str(e.value)


# TODO - Add tests for filter() with valid input