import pytest
from file_navigation import file_navigation as fn
import os
import shutil

HIDDEN_FILES = [".test", ".test.txt", ".test.jpg", ".test.png", ".test.html", "..test.txt"]
INVALID_HIDDEN_FILES = ["test", "test.txt", "test.jpg", "test.png", "test.html"]
IMAGE_FILES = ["test.jpg", "test.png", ".test.jpg", ".test.png", "a.txt.jpg", "a.txt.png"]
INVALID_IMAGE_FILES = ["test.txt", "test.html", "test.txt", ".test.txt", ".test.html", ".test.txt", "image.jpg.txt"]
NON_HIDDEN_IMAGE_FILES = ["test.jpg", "test.png", "a.txt.jpg", "a.txt.png"]
HTML_FILES = ["test.html", ".test.html", "a.txt.html"]
INVALID_HTML_FILES = ["test.txt", "test.jpg", "test.png", "test.txt", ".test.txt", ".test.jpg", ".test.png", ".test.txt", "html.jpg", ".html.jpg"]
NON_HIDDEN_HTML_FILES = ["test.html", "a.txt.html"]
TEXT_FILES = ["test.txt", ".test.txt", "a.txt"]
INVALID_TEXT_FILES = ["test.jpg", "test.png", "test.html", ".test.txt.", "txt"]
NON_HIDDEN_TEXT_FILES = ["test.txt", "a.txt"]

DIRECTORIES = ["dir1", "dir2", "dir3"]
TEST_DIR = "test_dir"


def clean_up_test_dir():
    if (os.path.isdir(TEST_DIR)):
        shutil.rmtree(TEST_DIR)

def setup_test_dir():
    if (not os.path.isdir(TEST_DIR)):
        os.mkdir(TEST_DIR)


def create_hidden_files():
    setup_test_dir()

    for file in HIDDEN_FILES:
        f = open(TEST_DIR + "/" + file, "w+")
        f.close()


def create_invalid_hidden_files():
    setup_test_dir()

    for file in INVALID_HIDDEN_FILES:
        f = open(TEST_DIR + "/" + file, "w+")
        f.close()


def create_image_files():
    setup_test_dir()

    for file in IMAGE_FILES:
        f = open(TEST_DIR + "/" + file, "w+")
        f.close()


def create_invalid_image_files():
    setup_test_dir()

    for file in INVALID_IMAGE_FILES:
        f = open(TEST_DIR + "/" + file, "w+")
        f.close()


def create_html_files():
    setup_test_dir()

    for file in HTML_FILES:
        f = open(TEST_DIR + "/" + file, "w+")
        f.close()


def create_invalid_html_files():
    setup_test_dir()

    for file in INVALID_HTML_FILES:
        f = open(TEST_DIR + "/" + file, "w+")
        f.close()


def create_text_files():
    setup_test_dir()

    for file in TEXT_FILES:
        f = open(TEST_DIR + "/" + file, "w+")
        f.close()


def create_invalid_text_files():
    setup_test_dir()

    for file in INVALID_TEXT_FILES:
        f = open(TEST_DIR + "/" + file, "w+")
        f.close()


def create_directories():
    setup_test_dir()

    for directory in DIRECTORIES:
        os.mkdir(TEST_DIR + "/" + directory)


def test_filter_hidden_files():
    assert fn.filter_out_hidden_files(HIDDEN_FILES) == []

    assert fn.filter_out_hidden_files(INVALID_HIDDEN_FILES) == INVALID_HIDDEN_FILES


def test_filter_hidden_files_type_error():
    with pytest.raises(TypeError) as e:
        fn.filter_out_hidden_files(1)

    assert "Input should be a list, but an object of type {} was received.".format(type(1)) in str(e.value)

    with pytest.raises(TypeError) as e:
        fn.filter_out_hidden_files([1])

    assert "Input should be of type str, but an object of type {} was received.".format(type(1)) in str(e.value)


def test_filter_image_files():
    assert fn.filter_out_images(IMAGE_FILES) == []

    assert fn.filter_out_images(INVALID_IMAGE_FILES) == INVALID_IMAGE_FILES


def test_filter_image_files_type_error():
    with pytest.raises(TypeError) as e:
        fn.filter_out_images(1)

    assert "Input should be a list, but an object of type {} was received.".format(type(1)) in str(e.value)

    with pytest.raises(TypeError) as e:
        fn.filter_out_images([1])

    assert "Input should be of type str, but an object of type {} was received.".format(type(1)) in str(e.value)


def test_filter_html_files():
    assert fn.filter_out_html_files(HTML_FILES) == []

    assert fn.filter_out_html_files(INVALID_HTML_FILES) == INVALID_HTML_FILES


def test_filter_html_files_type_error():
    with pytest.raises(TypeError) as e:
        fn.filter_out_html_files(1)

    assert "Input should be a list, but an object of type {} was received.".format(type(1)) in str(e.value)

    with pytest.raises(TypeError) as e:
        fn.filter_out_html_files([1])

    assert "Input should be of type str, but an object of type {} was received.".format(type(1)) in str(e.value)


def test_filter_text_files():
    assert fn.filter_out_text_files(TEXT_FILES) == []

    assert fn.filter_out_text_files(INVALID_TEXT_FILES) == INVALID_TEXT_FILES


def test_filter_text_files_type_error():
    with pytest.raises(TypeError) as e:
        fn.filter_out_text_files(1)

    assert "Input should be a list, but an object of type {} was received.".format(type(1)) in str(e.value)

    with pytest.raises(TypeError) as e:
        fn.filter_out_text_files([1])

    assert "Input should be of type str, but an object of type {} was received.".format(type(1)) in str(e.value)


def test_filter_files_without_directories():
    clean_up_test_dir()
    create_hidden_files()
    create_image_files()
    create_html_files()
    create_text_files()


    gcwd = os.getcwd()
    os.chdir(TEST_DIR)

    assert (fn.filter_out_files(HTML_FILES + IMAGE_FILES + TEXT_FILES + HIDDEN_FILES) 
            == [])
    
    os.chdir(gcwd)
    clean_up_test_dir()
    create_invalid_hidden_files()
    create_invalid_image_files()
    create_invalid_html_files()
    create_invalid_text_files()
    os.chdir(TEST_DIR)

    assert (fn.filter_out_files(INVALID_HTML_FILES + INVALID_IMAGE_FILES + INVALID_TEXT_FILES + INVALID_HIDDEN_FILES) 
            == [])
    
    os.chdir(gcwd)
    clean_up_test_dir()


def test_filter_files_type_error():
    with pytest.raises(TypeError) as e:
        fn.filter_out_files(1)

    assert "Input should be a list, but an object of type {} was received.".format(type(1)) in str(e.value)

    with pytest.raises(TypeError) as e:
        fn.filter_out_files([1])

    assert "Expected one or two strings but received an object of a different type" in str(e.value)


def test_filter_files_empty_string():
    with pytest.raises(ValueError) as e:
        fn.filter_out_files([""])

    assert "Input should not contain empty strings" in str(e.value)


def test_filter_files_empty_list():
    assert fn.filter_out_files([]) == []


def test_filter_files_with_directories():
    clean_up_test_dir()
    create_hidden_files()
    create_image_files()
    create_html_files()
    create_text_files()
    create_directories()

    gcwd = os.getcwd()
    os.chdir(TEST_DIR)

    assert (fn.filter_out_files(HTML_FILES + IMAGE_FILES + TEXT_FILES + HIDDEN_FILES + DIRECTORIES) 
            == DIRECTORIES)
    
    os.chdir(gcwd)
    clean_up_test_dir()
    create_invalid_hidden_files()
    create_invalid_image_files()
    create_invalid_html_files()
    create_invalid_text_files()
    create_directories()
    os.chdir(TEST_DIR)

    assert (fn.filter_out_files(INVALID_HTML_FILES + INVALID_IMAGE_FILES + INVALID_TEXT_FILES + INVALID_HIDDEN_FILES + DIRECTORIES) 
            == DIRECTORIES)
    
    os.chdir(gcwd)
    clean_up_test_dir()


def test_get_directories():
    clean_up_test_dir()
    create_directories()

    gcwd = os.getcwd()
    os.chdir(TEST_DIR)

    output = fn.get_directories()
    output.sort()
    assert output == DIRECTORIES

    os.chdir(gcwd)
    clean_up_test_dir()


def test_get_directories_filter_hidden_files():
    clean_up_test_dir()
    create_directories()

    gcwd = os.getcwd()
    os.chdir(TEST_DIR)
    os.mkdir(".hidden")

    output = fn.get_directories()
    output.sort()
    assert output == DIRECTORIES

    output = fn.get_directories(ignore_hidden_files=True)
    output.sort()
    assert output == DIRECTORIES

    os.chdir(gcwd)
    clean_up_test_dir()


def test_get_directories_with_hidden_files():
    clean_up_test_dir()
    create_directories()

    gcwd = os.getcwd()
    os.chdir(TEST_DIR)
    os.mkdir(".hidden")

    output = fn.get_directories()
    output.sort()
    assert output == DIRECTORIES

    output = fn.get_directories(ignore_hidden_files=False)
    output.sort()
    result = DIRECTORIES + [".hidden"]
    result.sort()
    assert output == result

    os.chdir(gcwd)
    clean_up_test_dir()


def test_get_directories_with_provided_path():
    clean_up_test_dir()
    create_directories()

    output = fn.get_directories(path=TEST_DIR)
    output.sort()
    assert output == DIRECTORIES

    clean_up_test_dir()


def test_get_files_ignore_hidden_files():
    clean_up_test_dir()
    create_hidden_files()
    create_image_files()
    create_html_files()
    create_text_files()

    gcwd = os.getcwd()
    os.chdir(TEST_DIR)

    output = fn.get_files()
    output.sort()
    result = NON_HIDDEN_TEXT_FILES + NON_HIDDEN_HTML_FILES + NON_HIDDEN_IMAGE_FILES
    result.sort()
    assert output == result

    output = fn.get_files(ignore_hidden_files=True)
    output.sort()
    assert output == result

    os.chdir(gcwd)
    clean_up_test_dir()


def test_get_files_with_hidden_files():
    clean_up_test_dir()
    create_hidden_files()
    create_image_files()
    create_html_files()
    create_text_files()

    gcwd = os.getcwd()
    os.chdir(TEST_DIR)

    output = fn.get_files(ignore_hidden_files=False)
    output.sort()
    output = {file for file in output} # remove duplicates
    result = HIDDEN_FILES + IMAGE_FILES + HTML_FILES + TEXT_FILES
    result.sort()
    result = {file for file in result} # remove duplicates
    assert output == result

    os.chdir(gcwd)
    clean_up_test_dir()


def test_get_files_with_provided_path():
    clean_up_test_dir()
    create_hidden_files()
    create_image_files()
    create_html_files()
    create_text_files()

    output = fn.get_files(path=TEST_DIR)
    output.sort()
    result = NON_HIDDEN_TEXT_FILES + NON_HIDDEN_HTML_FILES + NON_HIDDEN_IMAGE_FILES
    result.sort()
    assert output == result

    clean_up_test_dir()