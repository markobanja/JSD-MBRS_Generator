import re
import string
import logging
import config as cfg
from os import getcwd, listdir, makedirs
from os.path import exists, isdir, basename, commonpath
from pathlib import Path


def get_current_path():
    """
    Returns the current working directory.
    """
    current_directory = getcwd()
    logging.debug(f'Getting current working directory: "{current_directory}"')
    return current_directory

def get_base_name(path):
    """
    Gets the base name of a given path.
    """
    logging.debug(f'Getting base name of path: "{path}"')
    return basename(path)

def get_path(*paths):
    """
    Joins multiple paths together using the pathlib.Path / operator.
    """
    if len(paths) < 2:
        logging.error('At least two paths must be provided')
        raise ValueError('At least two paths must be provided')
    
    combined_path = Path(paths[0])
    for path in paths[1:]:
        logging.debug(f'Joining "{path}" to "{combined_path}"')
        combined_path /= Path(path)
    
    return combined_path

def compare_paths(path1, path2):
    """
    Compares two paths and returns True if they are the same.
    """
    logging.debug(f'Comparing paths: "{path1}" and "{path2}"')
    return commonpath([path1]) == commonpath([path1, path2])

def create_folder(base_path, folder_name):
    """
    Creates a folder at the given base path with the specified name.
    """
    folder_path = get_path(base_path, folder_name)
    makedirs(str(folder_path), exist_ok=True)
    logging.debug(f'Folder "{folder_path}" created')

def folder_exists(folder_path):
    """
    Checks if a folder exists at the given path and if it is a directory.
    """
    logging.debug(f'Checking if folder "{folder_path}" exists and is a directory')
    if not (exists(folder_path) and isdir(folder_path)):
        logging.error(f'The "{folder_path}" folder does not exist in the current directory!')
        raise FileNotFoundError(f'The "{folder_path}" folder does not exist in the current directory!')

def file_exists(folder_path, file_name):
    """
    Checks if a file exists in a folder.
    """
    file_path = get_path(folder_path, file_name)
    logging.debug(f'Checking if file "{file_name}" exists in folder "{folder_path}"')
    if not exists(file_path):
        logging.error(f'The "{file_name}" file does not exist in the "{folder_path}" folder!')
        raise FileNotFoundError(f'The "{file_name}" file does not exist in the "{folder_path}" folder!')

def read_file(file_path, encoding='utf-8'):
    """
    Reads the contents of a file.
    """
    logging.debug(f'Reading file: "{file_path}"')
    with open(file_path, mode='r', encoding=encoding) as file:
        content = file.read()
    logging.debug(f'Successfully read "{file_path}" file')
    return content

def write_to_file(file_path, content, encoding='utf-8'):
    """
    Writes the given content to a file.
    """
    logging.debug(f'Writing to file: "{file_path}"')
    with open(file_path, mode='w', encoding=encoding) as file:
        file.write(content)
    logging.debug(f'Successfully wrote to "{file_path}" file')

def find_specific_file_regex(folder_path, regex):
    """
    Finds files in the given folder that match the given regular expression pattern, and returns them sorted in descending order.
    """
    result_files = []
    compiled_regex = re.compile(regex)
    logging.debug(f'Searching for file matching regex "{regex}" in folder "{folder_path}"')
    files = listdir(folder_path)
    for file_name in files:
        if compiled_regex.search(file_name):
            logging.debug(f'Found file "{file_name}" matching regex in folder')
            result_files.append(file_name)
    result_files.sort(reverse=True)
    logging.debug(f'Found {len(result_files)} files matching regex in folder')
    return result_files

def set_font(font_name, font_size, bold=False):
    """
    Sets the font properties for a widget.
    Returns a tuple containing the font name and size, with an additional 'bold' element if bold is True.
    """
    logging.debug(f'Setting font: name="{font_name}", size="{font_size}", bold="{bold}"')
    return (font_name, font_size, 'bold') if bold else (font_name, font_size)

def convert_rgb_to_hex(rgb_value):
    """
    Converts RGB color values to a hexadecimal color code.
    """
    red, green, blue = rgb_value
    hex_value = '#%02x%02x%02x' % rgb_value # Convert the RGB values to a hexadecimal color code
    logging.debug(f'Converting RGB values ({red}, {green}, {blue}) to hex: {hex_value}')
    return hex_value

def is_spring_boot_application(folder_path):
    """
    Determines if the given folder path is a Spring Boot application.
    """
    logging.debug(f'Checking if folder "{folder_path}" is a Spring Boot application')
    build_tool = detect_build_tool(folder_path)
    # Check if all required source folders exist
    has_source_folders = all(
        isdir(get_path(folder_path, source_folder))
        for source_folder in ['src/main/java', 'src/main/resources', 'src/test/java']  # Required source folders for a Spring Boot application
    )
    logging.debug(f'Source folders exist: {has_source_folders}')
    is_spring_boot = build_tool is not None and has_source_folders
    logging.debug(f'Confirmed as Spring Boot application: {is_spring_boot}. Build tool: {build_tool}')
    return build_tool, is_spring_boot

def detect_build_tool(folder_path):
    """
    Detects the Spring Boot build tool used in a given folder.
    """
    logging.debug(f'Detecting build tool in folder: "{folder_path}"')
    for tool, file_name in cfg.BUILD_TOOL_FILE_MAPPING.items():
        if file_name in listdir(folder_path):
            logging.debug(f'Build tool "{tool}" detected in folder')
            return tool
    logging.debug('No build tool detected in folder')
    return None

def add_punctuation(text, punctuation='!'):
    """
    Adds punctuation to the end of a text string after removing any existing punctuation.
    """
    logging.debug(f'Adding punctuation: "{punctuation}" to text: "{text}"')
    return text.rstrip(string.punctuation) + punctuation