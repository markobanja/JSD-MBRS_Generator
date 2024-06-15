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
    logging.debug(f'Checking if folder "{folder_path}" exists and is a directory')
    return exists(folder_path) and isdir(folder_path)

def file_exists(folder_path, file_name):
    """
    Checks if a file exists in a folder.
    """
    file_path = get_path(folder_path, file_name)
    logging.debug(f'Checking if file "{file_name}" exists in folder "{folder_path}"')
    return exists(file_path)

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