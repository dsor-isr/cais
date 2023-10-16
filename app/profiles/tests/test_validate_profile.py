import os
import pytest
from profiles import profiles

KEYS = ["name", "driverFilters", "plotFilters"]
VALUES = ["test", ["test"], ["test"]]

def clean_files():
    if os.path.exists("profiles.json"):
        os.remove("profiles.json")


def test_validate_profile_invalid_input_type():
    with pytest.raises(TypeError) as e:
        profiles.validate_profile(1)

    assert "Profile must be a dictionary" in str(e.value)

    with pytest.raises(TypeError) as e:
        profiles.validate_profile(None)

    assert "Profile must be a dictionary" in str(e.value)


def test_validate_profile_invalid_input_value():
    with pytest.raises(ValueError) as e:
        profiles.validate_profile({})

    assert "Profile can't be an empty dictionary" in str(e.value)


def test_validate_profile_no_name():
    with pytest.raises(ValueError) as e:
        profiles.validate_profile({KEYS[1]: VALUES[1], KEYS[2]: VALUES[2]})

    assert "Profile must contain name, driverFilters and plotFilters" in str(e.value)


def test_validate_profile_no_driverFilters():
    with pytest.raises(ValueError) as e:
        profiles.validate_profile({KEYS[0]: VALUES[0], KEYS[2]: VALUES[2]})

    assert "Profile must contain name, driverFilters and plotFilters" in str(e.value)


def test_validate_profile_no_plotFilters():
    with pytest.raises(ValueError) as e:
        profiles.validate_profile({KEYS[0]: VALUES[0], KEYS[1]: VALUES[1]})

    assert "Profile must contain name, driverFilters and plotFilters" in str(e.value)


def test_validate_profile_invalid_name_type():
    with pytest.raises(TypeError) as e:
        profiles.validate_profile({KEYS[0]: 1, KEYS[1]: VALUES[1], KEYS[2]: VALUES[2]})

    assert "Profile name must be a string" in str(e.value)

    with pytest.raises(TypeError) as e:
        profiles.validate_profile({KEYS[0]: None, KEYS[1]: VALUES[1], KEYS[2]: VALUES[2]})

    assert "Profile name must be a string" in str(e.value)


def test_validate_profile_invalid_name_value():
    with pytest.raises(ValueError) as e:
        profiles.validate_profile({KEYS[0]: "", KEYS[1]: VALUES[1], KEYS[2]: VALUES[2]})

    assert "Profile name can't be empty" in str(e.value)


def test_validate_profile_invalid_driverFilters_type():
    with pytest.raises(TypeError) as e:
        profiles.validate_profile({KEYS[0]: VALUES[0], KEYS[1]: 1, KEYS[2]: VALUES[2]})

    assert "Profile driverFilters must be a list" in str(e.value)

    with pytest.raises(TypeError) as e:
        profiles.validate_profile({KEYS[0]: VALUES[0], KEYS[1]: None, KEYS[2]: VALUES[2]})

    assert "Profile driverFilters must be a list" in str(e.value)

    with pytest.raises(TypeError) as e:
        profiles.validate_profile({KEYS[0]: VALUES[0], KEYS[1]: [1], KEYS[2]: VALUES[2]})

    assert "Profile driverFilters must be a list of strings" in str(e.value)


def test_validate_profile_invalid_driverFilters_value():
    with pytest.raises(ValueError) as e:
        profiles.validate_profile({KEYS[0]: VALUES[0], KEYS[1]: [], KEYS[2]: VALUES[2]})

    assert "Profile driverFilters can't be empty" in str(e.value)

    with pytest.raises(ValueError) as e:
        profiles.validate_profile({KEYS[0]: VALUES[0], KEYS[1]: [""], KEYS[2]: VALUES[2]})

    assert "Profile driverFilters can't contain empty strings" in str(e.value)


def test_validate_profile_invalid_plotFilters_type():
    with pytest.raises(TypeError) as e:
        profiles.validate_profile({KEYS[0]: VALUES[0], KEYS[1]: VALUES[1], KEYS[2]: 1})

    assert "Profile plotFilters must be a list" in str(e.value)

    with pytest.raises(TypeError) as e:
        profiles.validate_profile({KEYS[0]: VALUES[0], KEYS[1]: VALUES[1], KEYS[2]: None})

    assert "Profile plotFilters must be a list" in str(e.value)

    with pytest.raises(TypeError) as e:
        profiles.validate_profile({KEYS[0]: VALUES[0], KEYS[1]: VALUES[1], KEYS[2]: [1]})

    assert "Profile plotFilters must be a list of strings" in str(e.value)


def test_validate_profile_invalid_plotFilters_value():
    with pytest.raises(ValueError) as e:
        profiles.validate_profile({KEYS[0]: VALUES[0], KEYS[1]: VALUES[1], KEYS[2]: []})

    assert "Profile plotFilters can't be empty" in str(e.value)

    with pytest.raises(ValueError) as e:
        profiles.validate_profile({KEYS[0]: VALUES[0], KEYS[1]: VALUES[1], KEYS[2]: [""]})

    assert "Profile plotFilters can't contain empty strings" in str(e.value)
