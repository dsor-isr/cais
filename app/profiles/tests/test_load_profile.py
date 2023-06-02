import os
from profiles import profiles
import pytest

def clean_files():
    if (os.path.exists("profiles.json")):
        os.remove("profiles.json")


def test_load_profile_invalid_input_type():
    with pytest.raises(TypeError) as e:
        profiles.loadProfile(1)

    assert "Profile name must be a string" in str(e.value)

    with pytest.raises(TypeError) as e:
        profiles.loadProfile(None)

    assert "Profile name must be a string" in str(e.value)


def test_load_profile_invalid_input_value():
    with pytest.raises(ValueError) as e:
        profiles.loadProfile("")

    assert "Profile name can't be empty" in str(e.value)


def test_load_profile_file_doesnt_exist():
    clean_files()
    profile = None
    with pytest.raises(FileNotFoundError) as e:
        profile = profiles.loadProfile("profiles.json")

    assert profile is None

    errorMessage = ("[Errno 2] No such file or directory: " + 
                    "'" + str("profiles.json") +  "'")
    
    assert errorMessage in str(e.value)


def test_load_profile_permission_error():
    clean_files()
    with open("profiles.json", "w") as f:
        f.write("")
        os.chmod("profiles.json", 0o222) # Set as write only

    with pytest.raises(PermissionError) as e:
        profiles.loadProfile("profiles.json")

    clean_files()


def test_load_profile_invalid_json():
    clean_files()
    with open("profiles.json", "w") as f:
        f.write("")

    with pytest.raises(Exception) as e:
        profiles.loadProfile("profiles.json")

    clean_files()


def test_load_profile_valid_json():
    clean_files()
    profiles.serializeClass({"name": "test"})

    profile = profiles.loadProfile("test")
    assert profile['name'] == "test"
    clean_files()


def test_load_profile_valid_json_invalid_name():
    clean_files()
    profiles.serializeClass({"name": "test"})

    with pytest.raises(ValueError) as e:
        profile = profiles.loadProfile("")

    assert "Profile name can't be empty" in str(e.value)

    with pytest.raises(TypeError) as e:
        profile = profiles.loadProfile(None)

    assert "Profile name must be a string" in str(e.value)

    with pytest.raises(TypeError) as e:
        profile = profiles.loadProfile(1)

    assert "Profile name must be a string" in str(e.value)

    clean_files()


def test_load_profile_valid_json_invalid_profile():
    clean_files()
    profiles.serializeClass({"name": "test"})

    with pytest.raises(ValueError) as e:
        profile = profiles.loadProfile("test2")

    assert "Profile doesn't exist" in str(e.value)

    clean_files()


def test_load_profile_invalid_file():
    clean_files()

    with pytest.raises(FileNotFoundError) as e:
        profiles.loadProfile("profiles.json")


    errorMessage = ("[Errno 2] No such file or directory: " + 
                    "'" + str("profiles.json") +  "'")
    assert errorMessage in str(e.value)

    clean_files()