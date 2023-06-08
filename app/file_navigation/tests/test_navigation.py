import pytest
from file_navigation import file_navigation as fn
import os


def create_file():
    with open("test.txt", "w") as f:
        f.write("test")


def create_dir():
    os.mkdir("test")


def remove_file():
    os.remove("test.txt")


def remove_dir():
    os.rmdir("test")


def test_get_pwd():
    pwd_sys_call = os.getcwd()
    pwd_fn = fn.get_pwd()

    assert pwd_fn == pwd_sys_call


def test_build_dir_invalid_suffix():
    with pytest.raises(TypeError) as e:
        fn.build_dir(1)

    assert "Expected one or two strings but received an object of a different type" in str(e.value)


def test_build_dir_without_path():
    path = fn.build_dir("home")

    assert path == "/home"


def test_build_dir_with_path():
    path = fn.build_dir("home", "/path/to")

    assert path == "/path/to/home"


def test_extend_dir_invalid_input():
    with pytest.raises(TypeError) as e:
        fn.extend_dir(1)

    assert "Expected one or two strings but received an object of a different type" in str(e.value)


def test_extend_dir_valid_input():
    path = fn.extend_dir("extension")
    real_path = os.getcwd() + "/extension"

    assert path == real_path


def test_is_valid_file_invalid_input():
    with pytest.raises(TypeError) as e:
        fn.is_valid_file(1)

    assert "Input should be of type str, but an object of type {} was received.".format(type(1)) in str(e.value)

    with pytest.raises(ValueError) as e:
        fn.filter_out_files([""])

    assert "Input should not contain empty strings" in str(e.value)


def test_is_valid_file_valid_input():
    path = os.getcwd() + "/test.txt"
    create_file()

    assert fn.is_valid_file(path) == True

    remove_file()


def test_is_valid_dir_invalid_input():
    with pytest.raises(TypeError) as e:
        fn.is_valid_directory(1)

    assert "Input should be of type str, but an object of type {} was received.".format(type(1)) in str(e.value)


def test_is_valid_dir_valid_input():
    path = os.getcwd() + "/test"
    create_dir()

    assert fn.is_valid_directory(path) == True

    remove_dir()


def test_is_valid_dir_invalid_dir():
    path = "/invalid"

    assert fn.is_valid_directory(path) == False


def test_change_dir():
    path = os.getcwd()
    create_dir()

    fn.change_directory(path + "/test")

    assert os.getcwd() == (path + "/test")

    fn.change_directory(path)

    assert os.getcwd() == path

    remove_dir()