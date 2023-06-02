import os
import json
import pytest
from profiles import profiles

KEYS = ["name", "email", "password", "username", "website", "phone", "address", "notes"]
VALUES = ["test", "email", "password", "username", "website", "phone", "address", "notes"]
NUM_PROFILES = 5

def clean_files():
    if (os.path.exists("profiles.json")):
        os.remove("profiles.json")


def test_delete_profile_by_name_invalid_input_type():
    with pytest.raises(TypeError) as e:
        profiles.deleteProfileByName(1)

    assert "Profile name must be a string" in str(e.value)

    with pytest.raises(TypeError) as e:
        profiles.deleteProfileByName(None)

    assert "Profile name must be a string" in str(e.value)


def test_delete_profile_by_name_invalid_input_value():
    with pytest.raises(ValueError) as e:
        profiles.deleteProfileByName("")

    assert "Profile name can't be empty" in str(e.value)


def test_delete_profile_by_name_file_not_found():
    clean_files()

    with pytest.raises(FileNotFoundError) as e:
        profiles.deleteProfileByName(VALUES[0])

    assert "No such file or directory: 'profiles.json'" in str(e.value)


def test_delete_profile_by_name_profile_doesnt_exist():
    clean_files()

    profiles.serializeClass({KEYS[0]: VALUES[0]})

    with pytest.raises(ValueError) as e:
        profiles.deleteProfileByName("test1")

    assert "Profile doesn't exist" in str(e.value)

    clean_files()


def test_delete_profile_by_name_permission_error():
    clean_files()

    with open("profiles.json", "w") as jsonFile:
        json.dump([{KEYS[0]: VALUES[0]}], jsonFile)
        
    os.chmod("profiles.json", 0o222) # 222 = -w--w--w-

    with pytest.raises(PermissionError) as e:
        profiles.deleteProfileByName(VALUES[0])

    assert "Permission denied: 'profiles.json'" in str(e.value)

    clean_files()


def test_delete_profile_by_name():
    clean_files()

    profiles.serializeClass({KEYS[0]: VALUES[0]})
    data = profiles.readJSONfile("profiles.json")

    assert type(data) == list
    assert len(data) == 1
    assert len(data[0]) == 1
    assert KEYS[0] in data[0].keys()
    assert VALUES[0] in data[0].values()
    assert data[0][KEYS[0]] == VALUES[0]

    profiles.deleteProfileByName(VALUES[0])
    data = profiles.readJSONfile("profiles.json")

    assert type(data) == list
    assert len(data) == 0

    clean_files()


def test_delete_profile_by_name_multiple_profiles():
    clean_files()

    for i in range(NUM_PROFILES):
        profiles.serializeClass({KEYS[0]: VALUES[0] + str(i)})

    data = profiles.readJSONfile("profiles.json")

    assert type(data) == list
    assert len(data) == NUM_PROFILES

    for i in range(NUM_PROFILES):
        assert len(data[i]) == 1
        assert KEYS[0] in data[i].keys()
        assert VALUES[0] + str(i) in data[i].values()
        assert data[i][KEYS[0]] == VALUES[0] + str(i)

    profiles.deleteProfileByName(VALUES[0] + str(0))
    data = profiles.readJSONfile("profiles.json")

    assert type(data) == list
    assert len(data) == NUM_PROFILES - 1

    for i in range(NUM_PROFILES - 1):
        assert len(data[i]) == 1
        assert KEYS[0] in data[i].keys()
        assert VALUES[0] + str(i + 1) in data[i].values()
        assert data[i][KEYS[0]] == VALUES[0] + str(i + 1)

    clean_files()