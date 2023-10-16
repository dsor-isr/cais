import os
import pytest
from profiles import profiles

NUM_OF_PROFILES = 5

def clean_files():
    if (os.path.exists("profiles.json")):
        os.remove("profiles.json")


def test_serialize_class_invalid_input_type():
    with pytest.raises(TypeError) as e:
        profiles.serializeClass(1)

    assert "Profile must be a dictionary object" in str(e.value)

    with pytest.raises(TypeError) as e:
        profiles.serializeClass(None)

    assert "Profile must be a dictionary object" in str(e.value)


def test_serialize_class_invalid_input_value():
    with pytest.raises(KeyError) as e:
        profiles.serializeClass({})

    assert "Profile must have a name" in str(e.value)

    with pytest.raises(ValueError) as e:
        profiles.serializeClass({"name": ""})

    assert "Profile name can't be None/Null or empty" in str(e.value)

    with pytest.raises(ValueError) as e:
        profiles.serializeClass({"name": None})

    assert "Profile name can't be None/Null or empty" in str(e.value)


def test_serialize_class_file_not_found():
    clean_files()

    with pytest.raises(FileNotFoundError) as e:
        with open("profiles.json", "r") as jsonFile:
            pass

    assert "No such file or directory: 'profiles.json'" in str(e.value)

    profiles.serializeClass({"name": "test"})
    data = profiles.readJSONfile("profiles.json")

    assert type(data) == list

    assert len(data) == 1

    assert len(data[0]) == 1

    assert "name" in data[0].keys()

    assert "test" in data[0].values()

    assert data[0]["name"] == "test"

    clean_files()


def test_serialize_class_permission_error():
    clean_files()

    with open("profiles.json", "w") as jsonFile:
        jsonFile.write("")

    os.chmod("profiles.json", 0o222) # 222 = -w--w--w-

    with pytest.raises(PermissionError) as e:
        profiles.serializeClass({"name": "test"})

    assert "[Errno 13] Permission denied: 'profiles.json'" in str(e.value)

    clean_files()


def test_serialize_class():
    clean_files()

    profiles.serializeClass({"name": "test"})

    data = profiles.readJSONfile("profiles.json")

    assert type(data) == list

    assert len(data) == 1

    assert len(data[0]) == 1

    assert "name" in data[0].keys()

    assert "test" in data[0].values()

    assert data[0]["name"] == "test"

    clean_files()


def test_serialize_multiple_profiles():
    clean_files()

    key = "name"
    value = "test"
    for i in range(NUM_OF_PROFILES):
        currentValue = value + str(i)
        profiles.serializeClass({key: currentValue})
    
    data = profiles.readJSONfile("profiles.json")

    assert type(data) == list

    assert len(data) == NUM_OF_PROFILES

    for i in range(NUM_OF_PROFILES):
        currentValue = value + str(i)
        assert len(data[i]) == 1
        assert key in data[i].keys()
        assert currentValue in data[i].values()
        assert data[i][key] == currentValue

    clean_files()


def test_serialize_profile_one_profile_multiple_keys():
    clean_files()

    keys = ["name", "key1", "key2"]
    values = ["test", "value1", "value2"]
    profiles.serializeClass({keys[0]: values[0], keys[1]: values[1], keys[2]: values[2]})

    profile = profiles.loadProfile("test")

    assert type(profile) == dict

    assert len(profile) == 3

    for i in range(len(profile)):
        assert keys[i] in profile.keys()
        assert values[i] in profile.values()
        assert profile[keys[i]] == values[i]

    clean_files()


def test_serialize_profile_already_exists():
    clean_files()

    profiles.serializeClass({"name": "test"})

    with pytest.raises(ValueError) as e:
        profiles.serializeClass({"name": "test"})

    assert "Profile already exists" in str(e.value)

    clean_files()