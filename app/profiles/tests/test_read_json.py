import pytest
from profiles import profiles
import os


def clean_files():
    if os.path.exists("profiles.json"):
        os.remove("profiles.json")
    if os.path.exists("read_json_test.json"):
        os.remove("read_json_test.json")


def test_read_json_invalid_input_type():

    with pytest.raises(TypeError) as e:
        profiles.readJSONfile(1)

    assert "File must be a string" in str(e.value)

    with pytest.raises(TypeError) as e:
        profiles.readJSONfile(None)

    assert "File must be a string" in str(e.value)


def test_read_json_invalid_input_value():

    with pytest.raises(ValueError) as e:
        profiles.readJSONfile("")

    assert "File can't be None/Null or empty" in str(e.value)


def test_read_json_file_doesnt_exist():
    
    clean_files()
    with pytest.raises(FileNotFoundError) as e:
        profiles.readJSONfile("read_json_test.json")
    

def test_read_json_permission_error():
    clean_files()
    with open("read_json_test.json", "w") as f:
        f.write("")
        os.chmod("read_json_test.json", 0o222) # Set as write only

    with pytest.raises(PermissionError) as e:
        profiles.readJSONfile("read_json_test.json")

    clean_files()
    