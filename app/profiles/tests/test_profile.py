from profiles import profiles
import pytest


TEST_PROFILES = ["TEST_PROFILE", "SECOND_TEST_PROFILE", "THIRD_TEST_PROFILE", "FOURTH_TEST_PROFILE", "FIFTH_TEST_PROFILE"]
ALPHABETICAL_PROFILES = ['A', 'B', 'Z', 'Bc']
TO_STRING = "Profile = { name: TEST_PROFILE, USBL: True, Altimeter: False, DepthCell: True, GPS: True, IMU: True, InsidePressure: False, BatMonit: False, Thrusters: True}"

def test_clone():
    profile = profiles.Profile(TEST_PROFILES[0], True, False, True, True, True, False, False, True)

    cloned = profile.clone()

    assert profile.getName() == cloned.getName()
    assert profile.getUsbl() == cloned.getUsbl()
    assert profile.getAltimeter() == cloned.getAltimeter()
    assert profile.getDepthCell() == cloned.getDepthCell()
    assert profile.getGps() == cloned.getGps()
    assert profile.getImu() == cloned.getImu()
    assert profile.getInsidePressure() == cloned.getInsidePressure()
    assert profile.getBatMonit() == cloned.getBatMonit()
    assert profile.getThrusters() == cloned.getThrusters()


def test_clone_deep_copy():
    profile = profiles.Profile(TEST_PROFILES[0], True, False, True, True, True, False, False, True)

    cloned = profile.clone()

    cloned.setName(TEST_PROFILES[1])

    assert profile.getName() == TEST_PROFILES[0]
    assert cloned.getName() == TEST_PROFILES[1]


def test_equals_with_equal_profile():
    profile = profiles.Profile(TEST_PROFILES[0], True, False, True, True, True, False, False, True)

    cloned = profile.clone()

    assert profile == cloned


def test_equals_with_different_profile():
    profile = profiles.Profile(TEST_PROFILES[0], True, False, True, True, True, False, False, True)

    cloned = profile.clone()
    cloned.setName(TEST_PROFILES[1])

    assert profile != cloned


def test_equals_with_non_profile_object():
    profile = profiles.Profile(TEST_PROFILES[0], True, False, True, True, True, False, False, True)

    assert profile != None
    assert profile != 9


def test_to_string():
    profile = profiles.Profile(TEST_PROFILES[0], True, False, True, True, True, False, False, True)

    assert str(profile) == TO_STRING


def test_comparisson_with_different_type():
    profile = profiles.Profile(TEST_PROFILES[0], True, False, True, True, True, False, False, True)

    with pytest.raises(TypeError) as e:
        profile < 3

    assert "Other must be a Profile object" in str(e.value)


def test_comparisson():
    profile = profiles.Profile(ALPHABETICAL_PROFILES[0], True, False, True, True, True, False, False, True)
    other = profiles.Profile(ALPHABETICAL_PROFILES[1], True, False, True, True, True, False, False, True)

    assert profile < other
    assert other > profile

    profile = profiles.Profile(ALPHABETICAL_PROFILES[3], True, False, True, True, True, False, False, True)
    other = profiles.Profile(ALPHABETICAL_PROFILES[2], True, False, True, True, True, False, False, True)

    assert profile < other
    assert other > profile