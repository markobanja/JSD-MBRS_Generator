import glob
import json
import logging
import re
import string
from datetime import datetime
from os import getcwd, listdir, makedirs
from os.path import basename, commonpath, exists, isdir, join
from pathlib import Path

import src.config as cfg


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
    result_files = list()
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

def find_java_app_file(folder_path):
    """
    Searches for a specific Java application file in the given folder and its subfolders.
    """
    pattern = join(folder_path, '**', cfg.SPRING_BOOT_APPLICATION_FILE)
    logging.debug(f'Searching for Java application file in folder "{folder_path}"')
    files = glob.glob(pattern, recursive=True)
    if not files:
        raise FileNotFoundError(f'Java application file not found in folder "{folder_path}"')
    elif len(files) > 1:
        raise Exception(f'Found multiple Java application files in folder "{folder_path}"')
    logging.debug(f'Found Java application file "{files[0]}" in folder')
    return Path(files[0])

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
        for source_folder in [cfg.PROJECT_JAVA_FOLDER, cfg.PROJECT_RESOURCES_FOLDER, cfg.PROJECT_TEST_JAVA_FOLDER]  # Required source folders for a Spring Boot application
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

def check_dependencies(build_tool, dependencies_to_check, build_content):
    """
    Checks if the specified dependencies are present in the build configuration.
    """
    logging.debug(f'Checking dependencies in "{build_tool}" build configuration')
    dependencies_section = get_dependencies_section(build_tool, build_content)
    if dependencies_section:
        # Iterate over the dependencies to check and check if they are in the dependencies block
        missing_dependencies = {key: value for key, value in dict(dependencies_to_check).items() if value not in dependencies_section}
        logging.debug(f'Missing dependencies: "{missing_dependencies}"')
        return missing_dependencies
    logging.warning(f'Could not find the dependencies section in the "{build_tool}" configuration file')
    return cfg.ERROR

def get_database_driver_dependency(build_tool, build_content):
    """
    Extracts the database driver dependency from the build configuration content.
    """
    logging.debug(f'Finding database driver dependency in "{build_tool}" build configuration')
    dependencies_section = get_dependencies_section(build_tool, build_content)
    if not dependencies_section:
        logging.warning(f'Could not find the dependencies section in the "{build_tool}" configuration file')
        return cfg.ERROR
    
    for driver_name, dependency in cfg.DATABASE_DEPENDENCY_MAPPING[build_tool].items():
        if dependency in dependencies_section:
            logging.debug(f'Database driver dependency found: "{driver_name}"')
            return driver_name
    
    logging.debug('Database driver dependency not found')
    return None

def get_dependencies_section(build_tool, build_content):
    """
    Extracts the dependencies section from the build configuration content.
    """
    logging.debug(f'Finding dependencies section in "{build_tool}" build configuration')
    pattern = cfg.BUILD_TOOL_PATTER_REGEX[build_tool]
    match = re.search(pattern, build_content)
    if match:
        logging.debug('Dependencies section found')
        dependencies_section = match.group(1)
        return dependencies_section
    logging.warning(f'Could not find the dependencies section in the "{build_tool}" configuration file')
    return None

def get_import_package_tree(project_path, pattern):
    """
    Extracts the import package tree from the given project path.
    """
    logging.debug(f'Finding import package tree for project path: "{project_path.as_posix()}"')
    project_path_str = project_path.as_posix()
    # Create the regex pattern with a capturing group for everything after the pattern/
    regex_pattern = rf'{re.escape(pattern)}/(.*)'
    match = re.search(regex_pattern, project_path_str)
    if match:
        package_tree = match.group(1).replace('/', '.')
        logging.debug(f'Found import package tree: "{package_tree}"')
        return package_tree
    logging.debug(f'Failed to find import package tree')
    return None

def convert_string_to_list(text_value):
    """
    Converts a string value to a list.
    """
    logging.debug(f'Converting string to list: "{text_value}"')
    return json.loads(text_value)

def check_words_in_string(first_string, second_string):
    """
    Checks if all the words in the first string are present in the second string.
    """
    logging.debug(f'Checking if all words in "{first_string}" are present in "{second_string}"')
    first_words = first_string.split()
    all_present = all(word in second_string for word in first_words)
    logging.debug(f'All words in "{first_string}" are present in "{second_string}": {all_present}')
    return all_present

def add_punctuation(text, punctuation='!'):
    """
    Adds punctuation to the end of a text string after removing any existing punctuation.
    """
    logging.debug(f'Adding punctuation: "{punctuation}" to text: "{text}"')
    if text.endswith('.'):
        logging.debug('Text already ends with a period, no need to add punctuation')
        return text
    elif text and text[-1] in string.punctuation:
        logging.debug('Removing existing punctuation from text')
        text = text[:-1]
    text += punctuation
    logging.debug(f'Added punctuation: "{punctuation}" to text: "{text}"')
    return text

def pluralize_word(word):
    """
    Pluralize a singular English word based on common rules.
    Rules:
    - If the word ends with 's', 'x', 'z', or a consonant followed by 'h', add 'es'.
    - If the word ends with 'y' preceded by a consonant, replace 'y' with 'ies'.
    - For other cases, add 's' to the word.
    """
    plural = None
    if re.search('[sxz]$', word) or re.search('[^aeiou]h$', word):
        plural = re.sub('$', 'es', word)
    elif re.search('[^aeiou]y$', word):
        plural = re.sub('y$', 'ies', word)
    else:
        plural = f'{word}s'
    logging.debug(f"Pluralized '{word}' to '{plural}'")
    return plural

def create_syntax_error_message(error):
    """
    Creates a message for a syntax error.
    """
    try:
        logging.debug(f'Parsing syntax error message: "{error.message}"')
        pattern = cfg.SYNTAX_ERROR_MESSAGE_REGEX
        match = re.match(pattern, error.message, re.DOTALL)
        expected_value, found_value = match.group(1, 2) if match else (error.message, None)
        expected_value = expected_value.strip().replace('\'', '"')
        if not found_value:
            logging.debug(f'Failed to parse syntax error message: "{error.message}". Returning original error message')
            message = f'at position ({error.line},{error.col}): Context of the syntax error: "{error.context}"! {expected_value} but not found.'
            return message, None, None
        found_value = extract_between_quotes(found_value.strip())
        near_part, found_part = found_value.split('*', 1)
        near_part = near_part.strip()
        found_part = found_part.strip()
        message = f'at position ({error.line},{error.col}): Syntax error near "{near_part}". {expected_value} but found "{found_part}"!'
        logging.debug(f'Parsed syntax error message: "{message}"')
        return message, near_part, found_part
    except Exception as e:
        logging.debug(f'Failed to parse syntax error message: "{e}"')
        return error.message
    
def get_unknown_object_name(error):
    """
    Extracts the unknown object name from the error message.
    """
    try:
        logging.debug(f'Parsing "Unknown object" error message: "{error.message}"')
        pattern = cfg.UNKNOWN_OBJECT_ERROR_MESSAGE_REGEX
        unknown_object, class_name = re.match(pattern, error.message, re.DOTALL).group(1, 2)
        logging.debug(f'Parsed Unknown object: "{unknown_object}", class name: "{class_name}"')
        return unknown_object
    except Exception as e:
        logging.debug(f'Failed to parse "Unknown object" error message: "{e}"')
        return error.message
    
def get_is_not_unique_name(error):
    """
    Extracts the property name from the 'is not unique' error message.
    """
    try:
        logging.debug(f'Parsing "is not unique" error message: "{error.message}"')
        pattern = cfg.IS_NOT_UNIQUE_ERROR_MESSAGE_REGEX
        is_not_unique = re.match(pattern, error.message, re.DOTALL).group(1)
        logging.debug(f'Parsed is not unique: "{is_not_unique}"')
        return is_not_unique
    except Exception as e:
        logging.debug(f'Failed to parse "is not unique" error message: "{e}"')

def extract_jinja_subprocess_output(output):
    """
    Extracts the content from the jinja subprocess output.
    """
    logging.debug(f'Extracting content from jinja subprocess output: "{output}"')
    matches = re.findall(cfg.JINJA_SUBPROCESS_ERROR_REGEX, output)
    if matches:
        first_line = matches[0]
        additional_errors_count = len(matches) - 1
        return f'{first_line}, and {additional_errors_count} more error(s) found.' if additional_errors_count > 0 else first_line
    return None
    
def extract_between_quotes(text):
    """
    Find and return content between single quotes.
    """
    logging.debug(f'Extracting content between quotes from text: "{text}"')
    match = re.search(cfg.QUOTE_REGEX, text)
    return match.group(1) if match else None

def extract_rule_defined_signs_regex(content):
    """
    Extract rule defined signs from the provided content using regex.
    """
    logging.debug(f'Extracting rule defined signs from text editor content')
    rule_defined_sign_pattern = re.compile(cfg.RULE_DEFINED_SIGNS_REGEX)
    rule_defined_signs = [match.group(0) for match in rule_defined_sign_pattern.finditer(content)]
    unique_signs = list(set(rule_defined_signs))  # Convert to set and back to list for uniqueness
    logging.debug(f'Found unique rule defined signs: "{unique_signs}"')
    return unique_signs

def extract_class_names_regex(content):
    """
    Extract class names from the provided content using regex.
    """
    logging.debug(f'Extracting class names from text editor content')
    class_pattern = re.compile(cfg.CLASS_NAME_REGEX)
    class_names = [match.group(1) for match in class_pattern.finditer(content)]
    logging.debug(f'Found class names: "{class_names}"')
    return class_names

def extract_property_values_regex(content):
    """
    Extract property values from the provided content using regex.
    """
    logging.debug(f'Extracting property values from text editor content')
    property_pattern = re.compile(cfg.PROPERTY_VALUE_REGEX)
    group_values = [match.group(1) for match in property_pattern.finditer(content)]
    property_values = [value for value in group_values if value]  # Remove empty values
    unique_property_values = list(set(property_values))  # Convert to set and back to list for uniqueness
    logging.debug(f'Found property values: "{unique_property_values}"')
    return unique_property_values

def extract_comments_regex(content):
    """
    Extract comments from the provided content using regex.
    """
    logging.debug(f'Extracting comments from text editor content')
    comment_pattern = re.compile(cfg.COMMENT_REGEX)
    comments = [match.group(0) for match in comment_pattern.finditer(content)]
    logging.debug(f'Found comments: "{comments}"')
    return comments

def check_value_regex(regex_pattern, value_to_check):
    """
    Checks if the provided value matches the provided regex pattern.
    """
    logging.debug(f'Checking if value "{value_to_check}" matches regex pattern "{regex_pattern}"')
    return bool(re.match(regex_pattern, value_to_check))

def check_app_file_content(file_path):
    """
    Checks if the provided file contains the OpenAPI definition.
    """
    logging.debug(f'Checking if file "{file_path}" contains the OpenAPI definition')
    content = read_file(file_path)
    pattern_info = re.compile(cfg.OPEN_API_DEFINITION_REGEX, re.DOTALL)
    # Returns True if the pattern is not found in the content
    return not pattern_info.search(content)

def check_property_value(property_type, property_value):
    """
    Checks if the provided value is appropriate for the given property type.
    """
    def error(message):
        """
        Returns an error message.
        """
        logging.debug(f'{message} ({property_type} type)')
        return message
    
    def check_datetime(date_str, format):
        """
        Check if the provided string is a valid datetime in specific format.
        """
        try:
            datetime.strptime(date_str, format)
            return True
        except ValueError:
            return False
    
    property_checking_rules = {
        # PrimitiveDataTypes
        cfg.BYTE: lambda value: cfg.OK if isinstance(int(value), int) and -128 <= int(value) <= 127 else error(cfg.ERROR_MESSAGES[cfg.BYTE]),
        cfg.SHORT: lambda value: cfg.OK if isinstance(int(value), int) and -32768 <= int(value) <= 32767 else error(cfg.ERROR_MESSAGES[cfg.SHORT]),
        cfg.CHAR: lambda value: cfg.OK if isinstance(value, str) and len(value) == 3 and value[0] == '\'' and value[-1] == '\'' else error(cfg.ERROR_MESSAGES[cfg.CHAR]),
        cfg.INT: lambda value: cfg.OK if isinstance(int(value), int) and -2147483648 <= int(value) <= 2147483647 else error(cfg.ERROR_MESSAGES[cfg.INT]),
        cfg.FLOAT: lambda value: cfg.OK if isinstance(float(value[:-1]), (int, float)) and value.upper().endswith('F') else error(cfg.ERROR_MESSAGES[cfg.FLOAT]),
        cfg.LONG: lambda value: cfg.OK if isinstance(int(value[:-1]), int) and -9223372036854775808 <= int(value[:-1]) <= 9223372036854775807 and value.upper().endswith('L') else error(cfg.ERROR_MESSAGES[cfg.LONG]),
        cfg.DOUBLE: lambda value: cfg.OK if isinstance(float(value[:-1]), (int, float)) and value.upper().endswith('D') else error(cfg.ERROR_MESSAGES[cfg.DOUBLE]),
        cfg.BOOLEAN: lambda value: cfg.OK if isinstance(value, str) and value.lower() in ('true', 'false') else error(cfg.ERROR_MESSAGES[cfg.BOOLEAN]),

        # WrapperDataTypes
        cfg.BYTE_W: lambda value: cfg.OK if isinstance(int(value), int) and -128 <= int(value) <= 127 else error(cfg.ERROR_MESSAGES[cfg.BYTE_W]),
        cfg.SHORT_W: lambda value: cfg.OK if isinstance(int(value), int) and -32768 <= int(value) <= 32767 else error(cfg.ERROR_MESSAGES[cfg.SHORT_W]),
        cfg.CHARACTER_W: lambda value: cfg.OK if isinstance(value, str) and len(value) == 3 and value[0] == '\'' and value[-1] == '\'' else error(cfg.ERROR_MESSAGES[cfg.CHARACTER_W]),
        cfg.INTEGER_W: lambda value: cfg.OK if isinstance(int(value), int) and -2147483648 <= int(value) <= 2147483647 else error(cfg.ERROR_MESSAGES[cfg.INTEGER_W]),
        cfg.FLOAT_W: lambda value: cfg.OK if isinstance(float(value[:-1]), (int, float)) and value.upper().endswith('F') else error(cfg.ERROR_MESSAGES[cfg.FLOAT_W]),
        cfg.LONG_W: lambda value: cfg.OK if isinstance(int(value[:-1]), int) and -9223372036854775808 <= int(value[:-1]) <= 9223372036854775807 and value.upper().endswith('L') else error(cfg.ERROR_MESSAGES[cfg.LONG_W]),
        cfg.DOUBLE_W: lambda value: cfg.OK if isinstance(float(value[:-1]), (int, float)) and value.upper().endswith('D') else error(cfg.ERROR_MESSAGES[cfg.DOUBLE_W]),
        cfg.BOOLEAN_W: lambda value: cfg.OK if isinstance(value, str) and value.lower() in ('true', 'false') else error(cfg.ERROR_MESSAGES[cfg.BOOLEAN_W]),
        
        # OtherDataTypes
        cfg.STR: lambda value: cfg.OK if isinstance(value, str) and value.startswith('"') and value.endswith('"') else error(cfg.ERROR_MESSAGES[cfg.STRING]),
        cfg.STRING: lambda value: cfg.OK if isinstance(value, str) and value.startswith('"') and value.endswith('"') else error(cfg.ERROR_MESSAGES[cfg.STRING]),
        cfg.STRING_C: lambda value: cfg.OK if isinstance(value, str) and value.startswith('"') and value.endswith('"') else error(cfg.ERROR_MESSAGES[cfg.STRING]),

        # DateTypes
        cfg.DATE: lambda value: cfg.OK if isinstance(value, str) and check_datetime(value, cfg.DATE_REGEX) else error(cfg.ERROR_MESSAGES[cfg.DATE]),
        cfg.TIME: lambda value: cfg.OK if isinstance(value, str) and check_datetime(value, cfg.TIME_REGEX) else error(cfg.ERROR_MESSAGES[cfg.TIME]),
        cfg.DATETIME: lambda value: cfg.OK if isinstance(value, str) and check_datetime(value, cfg.DATETIME_REGEX) else error(cfg.ERROR_MESSAGES[cfg.DATETIME]),

        # ListTypes
        cfg.ARRAY: lambda value: cfg.OK if isinstance(value, str) and value.startswith('[') and value.endswith(']') else error(cfg.ERROR_MESSAGES[cfg.ARRAY]),
        cfg.LINKED: lambda value: cfg.OK if isinstance(value, str) and value.startswith('[') and value.endswith(']') else error(cfg.ERROR_MESSAGES[cfg.LINKED]),
        cfg.HASHMAP: lambda value: cfg.OK if isinstance(value, str) and value.startswith('[') and value.endswith(']') else error(cfg.ERROR_MESSAGES[cfg.HASHMAP]),
        cfg.HASHSET: lambda value: cfg.OK if isinstance(value, str) and value.startswith('[') and value.endswith(']') else error(cfg.ERROR_MESSAGES[cfg.HASHSET]),
        cfg.TREEMAP: lambda value: cfg.OK if isinstance(value, str) and value.startswith('[') and value.endswith(']') else error(cfg.ERROR_MESSAGES[cfg.TREEMAP]),
        cfg.LIST: lambda value: cfg.OK if isinstance(value, str) and value.startswith('[') and value.endswith(']') else error(cfg.ERROR_MESSAGES[cfg.LIST]),
    }

    if property_type not in property_checking_rules:
        logging.error(f'Unknown property type: "{property_type}"')
        raise ValueError(f"Unknown property type: {property_type}")

    try:
        result = property_checking_rules[property_type](property_value)
        logging.debug(f'"{property_value}" is a valid value for "{property_type}" type')
        return result
    except ValueError:
        logging.error(f'"{property_value}" is NOT a valid value for "{property_type}" type: {cfg.ERROR_MESSAGES[property_type]}')
        return error(f'{cfg.ERROR_MESSAGES[property_type]}')
