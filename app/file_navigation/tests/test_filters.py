import pytest
from file_navigation import file_navigation as fn
import os
import shutil

HIDDEN_FILES = [".test", ".test.txt", ".test.jpg", ".test.png", ".test.html", "..test.txt"]
INVALID_HIDDEN_FILES = ["test", "test.txt", "test.jpg", "test.png", "test.html"]
IMAGE_FILES = ["test.jpg", "test.png", ".test.jpg", ".test.png", "a.txt.jpg", "a.txt.png"]
INVALID_IMAGE_FILES = ["test.txt", "test.html", "test.txt", ".test.txt", ".test.html", ".test.txt", "image.jpg.txt"]
HTML_FILES = ["test.html", ".test.html", "a.txt.html"]
INVALID_HTML_FILES = ["test.txt", "test.jpg", "test.png", "test.txt", ".test.txt", ".test.jpg", ".test.png", ".test.txt", "html.jpg", ".html.jpg"]
TEXT_FILES = ["test.txt", ".test.txt", "a.txt"]
INVALID_TEXT_FILES = ["test.jpg", "test.png", "test.html", ".test.txt.", "txt"]

DIRECTORIES = ["dir1", "dir2", "dir3"]


def clean_up_test_dir():
    if (os.path.isdir("test_dir")):
        shutil.rmtree("test_dir")

def setup_test_dir():
    if (not os.path.isdir("test_dir")):
        os.mkdir("test_dir")


def create_hidden_files():
    setup_test_dir()

    for file in HIDDEN_FILES:
        f = open("test_dir/" + file, "w+")
        f.close()


def create_invalid_hidden_files():
    setup_test_dir()

    for file in INVALID_HIDDEN_FILES:
        f = open("test_dir/" + file, "w+")
        f.close()


def create_image_files():
    setup_test_dir()

    for file in IMAGE_FILES:
        f = open("test_dir/" + file, "w+")
        f.close()


def create_invalid_image_files():
    setup_test_dir()

    for file in INVALID_IMAGE_FILES:
        f = open("test_dir/" + file, "w+")
        f.close()


def create_html_files():
    setup_test_dir()

    for file in HTML_FILES:
        f = open("test_dir/" + file, "w+")
        f.close()


def create_invalid_html_files():
    setup_test_dir()

    for file in INVALID_HTML_FILES:
        f = open("test_dir/" + file, "w+")
        f.close()


def create_text_files():
    setup_test_dir()

    for file in TEXT_FILES:
        f = open("test_dir/" + file, "w+")
        f.close()


def create_invalid_text_files():
    setup_test_dir()

    for file in INVALID_TEXT_FILES:
        f = open("test_dir/" + file, "w+")
        f.close()


def create_directories():
    setup_test_dir()

    for directory in DIRECTORIES:
        os.mkdir("test_dir/" + directory)


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
    os.chdir("test_dir")

    assert (fn.filter_out_files(HTML_FILES + IMAGE_FILES + TEXT_FILES + HIDDEN_FILES) 
            == [])
    
    os.chdir(gcwd)
    clean_up_test_dir()
    create_invalid_hidden_files()
    create_invalid_image_files()
    create_invalid_html_files()
    create_invalid_text_files()
    os.chdir("test_dir")

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
    os.chdir("test_dir")

    assert (fn.filter_out_files(HTML_FILES + IMAGE_FILES + TEXT_FILES + HIDDEN_FILES + DIRECTORIES) 
            == DIRECTORIES)
    
    os.chdir(gcwd)
    clean_up_test_dir()
    create_invalid_hidden_files()
    create_invalid_image_files()
    create_invalid_html_files()
    create_invalid_text_files()
    create_directories()
    os.chdir("test_dir")

    assert (fn.filter_out_files(INVALID_HTML_FILES + INVALID_IMAGE_FILES + INVALID_TEXT_FILES + INVALID_HIDDEN_FILES + DIRECTORIES) 
            == DIRECTORIES)
    
    os.chdir(gcwd)
    clean_up_test_dir()