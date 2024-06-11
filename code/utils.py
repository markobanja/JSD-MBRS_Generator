import logging
from os.path import join, exists, isdir

def get_path(path1, path2):
    """
    Joins two paths together using the os.path.join function.
    """
    logging.debug(f'Joining "{path2}" to "{path1}"')
    return join(path1, path2)

def folder_exists(folder_path):
    """
    Checks if a folder exists at the given path and if it is a directory.
    """
    logging.debug(f'Checking if "{folder_path}" exists')
    return exists(folder_path) and isdir(folder_path)

def file_exists(folder_path, file_name):
    """
    Checks if a file exists in a folder.
    """
    file_path = get_path(folder_path, file_name)
    logging.debug(f'Checking if "{file_name}" exists in "{folder_path}"')
    return exists(file_path)