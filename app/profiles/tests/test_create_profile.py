from profiles import profiles
import pytest
import os

TEST_PROFILES = ["TEST_PROFILE", "SECOND_TEST_PROFILE", "THIRD_TEST_PROFILE", "FOURTH_TEST_PROFILE", "FIFTH_TEST_PROFILE"]
EXISTING_PROFILE_MESSAGE_ERROR = "Profile already exists"
INVALID_NAME_TYPE_EXCEPTION = "Name must be a string"
INVALID_NAME_VALUE_EXCEPTION = "Name can't be None/Null or empty"


def delete_json():
    try:
        os.remove("profiles.json")
    except FileNotFoundError:
        pass
    except PermissionError:
        raise PermissionError("Permission denied to delete profiles.json")
    except Exception as e:
        raise Exception("Unexpected error: ", e)


def test_create_profile():
    delete_json()
    profile = profiles.Profile(TEST_PROFILES[0], True, False, True, True, True, False, False)

    assert profile.getName() == TEST_PROFILES[0]
    assert profile.getUsbl() == True
    assert profile.getAltimeter() == False
    assert profile.getDepthCell() == True
    assert profile.getGps() == True
    assert profile.getImu() == True
    assert profile.getInsidePressure() == False
    assert profile.getBatMonit() == False


def test_create_several_profiles():
    delete_json()

    num_profiles = len(TEST_PROFILES)
    for i in range(num_profiles):
        profile = profiles.Profile(TEST_PROFILES[i], True, False, True, True, True, False, False)

        assert profile.getName() == TEST_PROFILES[i]
        assert profile.getUsbl() == True
        assert profile.getAltimeter() == False
        assert profile.getDepthCell() == True
        assert profile.getGps() == True
        assert profile.getImu() == True
        assert profile.getInsidePressure() == False
        assert profile.getBatMonit() == False


# def test_serialize_one_profile():

# def test_serialize_several_profiles():

def test_serialize_two_equal_profiles():
    delete_json() # Delete the json file to setup the test
    profile = profiles.Profile(TEST_PROFILES[0], True, False, True, True, True, False, False)
    profiles.Profile.serializeClass(profile)

    assert profile.getName() == TEST_PROFILES[0]
    assert profile.getUsbl() == True
    assert profile.getAltimeter() == False
    assert profile.getDepthCell() == True
    assert profile.getGps() == True
    assert profile.getImu() == True
    assert profile.getInsidePressure() == False
    assert profile.getBatMonit() == False

    profile = profiles.Profile(TEST_PROFILES[0], True, False, True, True, True, False, False)
    with pytest.raises(ValueError) as e:
        profiles.Profile.serializeClass(profile)

    assert EXISTING_PROFILE_MESSAGE_ERROR in str(e.value)

    delete_json() # Delete the json file to clean after the test


def test_create_existing_profile_with_invalid_name():
    delete_json()
    with pytest.raises(ValueError) as e:
        profiles.Profile("", True, False, True, True, True, False, False)

    assert INVALID_NAME_VALUE_EXCEPTION in str(e.value)

    with pytest.raises(TypeError) as e:
        profiles.Profile(1, True, False, True, True, True, False, False)

    assert INVALID_NAME_TYPE_EXCEPTION in str(e.value)

    with pytest.raises(TypeError) as e:
        profiles.Profile(None, True, False, True, True, True, False, False)

    assert INVALID_NAME_TYPE_EXCEPTION in str(e.value)


def test_create_profile_with_invalid_boolean_flags():
    delete_json()
    with pytest.raises(TypeError) as e:
        profiles.Profile(TEST_PROFILES[0], 1, False, True, True, True, False, False)

    assert "USBL must be a boolean" in str(e.value)

    with pytest.raises(TypeError) as e:
        profiles.Profile(TEST_PROFILES[0], None, False, True, True, True, False, False)

    assert "USBL must be a boolean" in str(e.value)

    with pytest.raises(TypeError) as e:
        profiles.Profile(TEST_PROFILES[0], 2.5, False, True, True, True, False, False)

    assert "USBL must be a boolean" in str(e.value)

    with pytest.raises(TypeError) as e:
        profiles.Profile(TEST_PROFILES[0], True, 1, True, True, True, False, False)

    assert "Altimeter must be a boolean" in str(e.value)

    with pytest.raises(TypeError) as e:
        profiles.Profile(TEST_PROFILES[0], True, False, 1, True, True, False, False)

    assert "DepthCell must be a boolean" in str(e.value)

    with pytest.raises(TypeError) as e:
        profiles.Profile(TEST_PROFILES[0], True, False, True, 1, True, False, False)

    assert "GPS must be a boolean" in str(e.value)

    with pytest.raises(TypeError) as e:
        profiles.Profile(TEST_PROFILES[0], True, False, True, True, 1, False, False)
    
    assert "IMU must be a boolean" in str(e.value)

    with pytest.raises(TypeError) as e:
        profiles.Profile(TEST_PROFILES[0], True, False, True, True, True, 1, False)

    assert "InsidePressure must be a boolean" in str(e.value)

    with pytest.raises(TypeError) as e:
        profiles.Profile(TEST_PROFILES[0], True, False, True, True, True, False, 1)

    assert "BatMonit must be a boolean" in str(e.value)


# def test_create_profile_thrown_exceptions():

# def test_set_valid_attributes():

# def test_set_invalid_attributes():

# def test_profile_setters_and_getters():