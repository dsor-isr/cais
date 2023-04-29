import pytest
from file_navigation import file_navigation as fn


def test_is_txt_file():
    assert fn.is_txt_file("test.txt") == True
    assert fn.is_txt_file("txt") == False
    assert fn.is_txt_file("test.py") == False
    assert fn.is_txt_file(".txttest") == False
    assert fn.is_txt_file("test.txt.test") == False

    with pytest.raises(TypeError) as e:
        fn.is_txt_file(1)

    assert "Input should be of type str, but an object of type {} was received.".format(type(1)) in str(e.value)


def test_is_jpg_file():
    assert fn.is_jpg_file("test.jpg") == True
    assert fn.is_jpg_file("jpg") == False
    assert fn.is_jpg_file("test.py") == False
    assert fn.is_jpg_file(".jpgtest") == False
    assert fn.is_jpg_file("test.jpg.test") == False

    with pytest.raises(TypeError) as e:
        fn.is_jpg_file(1)

    assert "Input should be of type str, but an object of type {} was received.".format(type(1)) in str(e.value)


def test_is_png_file():
    assert fn.is_png_file("test.png") == True
    assert fn.is_png_file("png") == False
    assert fn.is_png_file("test.py") == False
    assert fn.is_png_file(".pngtest") == False
    assert fn.is_png_file("test.png.test") == False

    with pytest.raises(TypeError) as e:
        fn.is_png_file(1)

    assert "Input should be of type str, but an object of type {} was received.".format(type(1)) in str(e.value)


def test_is_html_file():
    assert fn.is_html_file("test.html") == True
    assert fn.is_html_file("html") == False
    assert fn.is_html_file("test.py") == False
    assert fn.is_html_file(".htmltest") == False
    assert fn.is_html_file("test.html.test") == False

    with pytest.raises(TypeError) as e:
        fn.is_html_file(1)

    assert "Input should be of type str, but an object of type {} was received.".format(type(1)) in str(e.value)


def test_is_hidden_file():
    assert fn.is_hidden_file(".test") == True
    assert fn.is_hidden_file("test") == False

    with pytest.raises(TypeError) as e:
        fn.is_hidden_file(1)

    assert "Input should be of type str, but an object of type {} was received.".format(type(1)) in str(e.value)


def test_is_image():
    assert fn.is_image("test.jpg") == True
    assert fn.is_image("test.png") == True
    assert fn.is_image("test.html") == False
    assert fn.is_image("jpg") == False
    assert fn.is_image("png") == False
    assert fn.is_image(".hidden.jpg") == True
    assert fn.is_image(".hidden.png") == True


    with pytest.raises(TypeError) as e:
        fn.is_image(1)

    assert "Input should be of type str, but an object of type {} was received.".format(type(1)) in str(e.value)