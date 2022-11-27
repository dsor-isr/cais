import os
import re


def get_pwd():
    """Return present working directory"""

    return os.getcwd()


def change_directory(path):
    """Change current working directory to path"""
    os.chdir(path)


def build_dir(suffix, path='/'):
    if path != '/':
        # If not root directory
        path = path + '/'
    
    return path + suffix


def extend_dir(suffix):
    """Takes a string as an argument and extends the current working directory,
    by appending the input."""

    cwd = get_pwd() # Get current directory

    return build_dir(suffix, cwd)


def is_valid_file(file):
    """Takes a string and checks if it is a valid file."""

    #if not (type(file) == str):
    #    raise TypeError("Input should be of type str, but an object of type {t} was received.".format(type(file)))
    

    return os.path.isfile(file)


def is_txt_file(file):
    """Takes a string and checks if it has a .txt extension."""

    #if not (type(file) == str):
    #    raise TypeError("Input should be of type str, but an object of type {t} was received.".format(type(file)))

    return re.search("\.txt$", file) != None


def is_jpg_file(file):
    """Takes a string and checks if it has a .jpg extension."""

    #if not (type(file) == str):
    #    raise TypeError("Input should be of type str, but an object of type {t} was received.".format(type(file)))

    return re.search("\.jpg$", file) != None


def is_png_file(file):
    """Takes a string and checks if it has a .png extension."""

    #if not (type(file) == str):
    #    raise TypeError("Input should be of type str, but an object of type {t} was received.".format(type(file)))

    return re.search("\.png$", file) != None


def is_image(file):
    """Takes a string and checks if it has a .png or .jpg extension"""

    #if not (type(file) == str):
    #    raise TypeError("Input should be of type str, but an object of type {t} was received.".format(type(file)))
    
    return is_png_file(file) or is_jpg_file(file)


def is_hidden_file(file):
    """Takes a string and checks if it is a hidden file (starts with '.')"""

    #if not (type(file) == str):
    #    raise TypeError("Input should be of type str, but an object of type {t} was received.".format(type(file)))
    
    return file[0] == '.'


def is_valid_directory(file):
    """Takes a string and checks if it is a valid directory."""

    #if not (type(file) == str):
    #    raise TypeError("Input should be of type str, but an object of type {t} was received.".format(type(file)))
    
    return os.path.isdir(file)


def filter_out_hidden_files(files):
    """Takes a list of files and removes all hidden files (files whose name
    start with '.')."""

    #if not (type(files) == list):
    #    raise TypeError("Input should be a list, but an object of type {t} was received.".format(type(files)))

    return [file for file in files if not (is_hidden_file(file))]


def filter_out_text_files(files):
    """Takes a list of files and removes all files with a .txt extension"""

    #if not (type(files) == list):
    #    raise TypeError("Input should be a list, but an object of type {t} was received.".format(type(files)))
    
    return [file for file in files if not (is_txt_file(file))]


def filter_out_images(files):
    """Takes a list of files and removes all files with a jpg or png extension"""

    #if not (type(files) == list):
    #    raise TypeError("Input should be a list, but an object of type {t} was received.".format(type(files)))
    
    return [file for file in files if not (is_image(file))]


def filter_out_directories(files, filter_out_text_files=False):
    """Takes a list of files and directories and removes all directories.
    If filter_out_text_files is set to True, then .txt files are also excluded"""

    #if not (type(files) == list):
    #    raise TypeError("Input should be a list, but an object of type {t} was received.".format(type(files)))

    filtered = []
    for file in files:
        file_path = extend_dir(file)

        if not (is_valid_directory(file_path)):
            if (filter_out_text_files and is_txt_file(file)):
                continue

            filtered.append(file)

    return filtered


def filter_out_files(files):
    """Takes a list of files and directories and removes all files."""

    #if not (type(files) == list):
    #    raise TypeError("Input should be a list, but an object of type {t} was received.".format(type(files)))

    filtered = []
    for file in files:
        file_path = extend_dir(file)

        if not (is_valid_file(file_path)):
            filtered.append(file)
    
    return filtered
        

def get_directories(ignore_hidden_files=True):
    """Lists all directories in the current working directory. Default behaviour
    is to remove hidden files. To include hidden files, set ignore_hidden_files
    to False.
    
    Note: Calls os.listdir(path='.'), as such, the behaviour is unspecified if
    files are created or deleted during the call of this function. For more
    information, check the documentation for python's os module
    https://docs.python.org/3/library/os.html#"""

    files = os.listdir(path='.')

    if (ignore_hidden_files == True):
        files = filter_out_hidden_files(files)
    
    return filter_out_files(files)


def get_files(ignore_hidden_files=True):
    """Lists all files in the current working directory. Default behaviour
    is to remove hidden files. To include hidden files, set ignore_hidden_files
    to False.
    
    Note: Calls os.listdir(path='.'), as such, the behaviour is unspecified if
    files are created or deleted during the call of this function. For more
    information, check the documentation for python's os module
    https://docs.python.org/3/library/os.html#"""

    files = os.listdir(path='.')

    if (ignore_hidden_files == True):
        files = filter_out_hidden_files(files)
    
    return filter_out_directories(files)


def get_images():
    """Lists all images in the current working directory.
    
    Note: Calls os.listdir(path='.'), as such, the behaviour is unspecified if
    files are created or deleted during the call of this function. For more
    information, check the documentation for python's os module
    https://docs.python.org/3/library/os.html#"""

    files = os.listdir(path='.')
    
    return [file for file in files if (is_image(file))]


def get_txt_files():
    """Lists all .txt files in the current working directory.
    
    Note: Calls os.listdir(path='.'), as such, the behaviour is unspecified if
    files are created or deleted during the call of this function. For more
    information, check the documentation for python's os module
    https://docs.python.org/3/library/os.html#"""

    files = os.listdir(path='.')
    
    return [file for file in files if (is_txt_file(file))]


def get_directory_content(ignore_hidden_files=True, ignore_text_files=False, 
                        ignore_directories=False, ignore_files=False, ignore_images=False):
    """Lists all files and directories on the current working directory.
    Default behaviour is to remove hidden files from output. To include 
    hidden files, set ignore_hidden_files to False. Directories, .txts 
    and other files are kept, unless the respective flags are used.
    
    Note: Calls os.listdir(path='.'), as such, the behaviour is unspecified if
    files are created or deleted during the call of this function. For more
    information, check the documentation for python's os module
    https://docs.python.org/3/library/os.html#"""

    files = os.listdir(path='.')

    if (ignore_hidden_files == True):
        # Remove hidden files from output
        files = filter_out_hidden_files(files)
    if (ignore_text_files == True):
        # Remove .txt files from output
        files = filter_out_text_files
    if (ignore_directories == True):
        # Remove sub-directories from output
        files = filter_out_directories(files)
    if (ignore_files == True):
        # Remove files from output
        files = filter_out_files(files)
    if (ignore_images == True):
        # Remove images from output
        files = filter_out_images(files)

    return files


def is_part_of_path(path, sub_string):

    return re.search(sub_string, path) != None



if __name__ == "__main__":
    # Main function

    # Use this for testing purposes
    #print("Directories: ", get_directories())
    #print("Images: ", get_images())
    #print("Text Files: ", get_txt_files())
    #print("Files: ", get_files())
    #print("All: ", get_directory_content())


    exit(0)