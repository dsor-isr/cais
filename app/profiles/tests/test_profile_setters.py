from profiles import profiles
import pytest
import os

TEST_PROFILES = ["TEST_PROFILE", "SECOND_TEST_PROFILE", "THIRD_TEST_PROFILE", "FOURTH_TEST_PROFILE", "FIFTH_TEST_PROFILE"]

def delete_json():
    try:
        os.remove("profiles.json")
    except FileNotFoundError:
        pass
    except PermissionError:
        raise PermissionError("Permission denied to delete profiles.json")
    except Exception as e:
        raise Exception("Unexpected error: ", e)
    

def test_setters_with_valid_values():
    profile = profiles.Profile(TEST_PROFILES[0], True, False, True, True, True, False, False)

    assert profile.getName() == TEST_PROFILES[0]
    assert profile.getUsbl() == True
    assert profile.getAltimeter() == False
    assert profile.getDepthCell() == True
    assert profile.getGps() == True
    assert profile.getImu() == True
    assert profile.getInsidePressure() == False
    assert profile.getBatMonit() == False

    profile.setName(TEST_PROFILES[1])
    profile.setUsbl(False)
    profile.setAltimeter(True)
    profile.setDepthCell(False)
    profile.setGps(False)
    profile.setImu(False)
    profile.setInsidePressure(True)
    profile.setBatMonit(True)

    assert profile.getName() == TEST_PROFILES[1]
    assert profile.getUsbl() == False
    assert profile.getAltimeter() == True
    assert profile.getDepthCell() == False
    assert profile.getGps() == False
    assert profile.getImu() == False
    assert profile.getInsidePressure() == True
    assert profile.getBatMonit() == True


def test_set_name_with_invalid_values():
    profile = profiles.Profile(TEST_PROFILES[0], True, False, True, True, True, False, False)

    with pytest.raises(ValueError) as e:
        profile.setName("")

    assert "Name can't be None/Null or empty" in str(e.value)

    with pytest.raises(TypeError) as e:
        profile.setName(None)

    assert "Name must be a string" in str(e.value)

    with pytest.raises(TypeError) as e:
        profile.setName(3)

    assert "Name must be a string" in str(e.value)


def test_set_usbl_with_invalid_values():
    profile = profiles.Profile(TEST_PROFILES[0], True, False, True, True, True, False, False)

    with pytest.raises(TypeError) as e:
        profile.setUsbl(None)

    assert "USBL must be a boolean" in str(e.value)

    with pytest.raises(TypeError) as e:
        profile.setUsbl(2.5)

    assert "USBL must be a boolean" in str(e.value)


def test_set_altimeter_with_invalid_values():
    profile = profiles.Profile(TEST_PROFILES[0], True, False, True, True, True, False, False)

    with pytest.raises(TypeError) as e:
        profile.setAltimeter(None)

    assert "Altimeter must be a boolean" in str(e.value)

    with pytest.raises(TypeError) as e:
        profile.setAltimeter(2.5)

    assert "Altimeter must be a boolean" in str(e.value)


def test_set_depth_cell_with_invalid_values():
    profile = profiles.Profile(TEST_PROFILES[0], True, False, True, True, True, False, False)

    with pytest.raises(TypeError) as e:
        profile.setDepthCell(None)

    assert "depthCell must be a boolean" in str(e.value)

    with pytest.raises(TypeError) as e:
        profile.setDepthCell(2.5)

    assert "depthCell must be a boolean" in str(e.value)


def test_set_bat_monit_with_invalid_values():
    profile = profiles.Profile(TEST_PROFILES[0], True, False, True, True, True, False, False)

    with pytest.raises(TypeError) as e:
        profile.setBatMonit(None)

    assert "batMonit must be a boolean" in str(e.value)

    with pytest.raises(TypeError) as e:
        profile.setBatMonit(2.5)

    assert "batMonit must be a boolean" in str(e.value)


def test_set_inside_pressure_with_invalid_values():
    profile = profiles.Profile(TEST_PROFILES[0], True, False, True, True, True, False, False)

    with pytest.raises(TypeError) as e:
        profile.setInsidePressure(None)

    assert "insidePressure must be a boolean" in str(e.value)

    with pytest.raises(TypeError) as e:
        profile.setInsidePressure(2.5)

    assert "insidePressure must be a boolean" in str(e.value)


def test_set_imu_with_invalid_values():
    profile = profiles.Profile(TEST_PROFILES[0], True, False, True, True, True, False, False)

    with pytest.raises(TypeError) as e:
        profile.setImu(None)

    assert "imu must be a boolean" in str(e.value)

    with pytest.raises(TypeError) as e:
        profile.setImu(2.5)

    assert "imu must be a boolean" in str(e.value)


def test_set_gps_with_invalid_values():
    profile = profiles.Profile(TEST_PROFILES[0], True, False, True, True, True, False, False)

    with pytest.raises(TypeError) as e:
        profile.setGps(None)

    assert "gps must be a boolean" in str(e.value)

    with pytest.raises(TypeError) as e:
        profile.setGps(2.5)

    assert "gps must be a boolean" in str(e.value)