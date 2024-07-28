# GUI
THEME_STYLE = 'plastik'
FONT = 'Courier New'
COLORS = {
    # GUI colors
    'initial_background': (240, 240, 240),
    'working_background': (255, 255, 255),
    'black': (0, 0, 0),

    # Text colors
    'ok': (27, 152, 81),
    'information': (52, 152, 219),
    'warning': (255, 102, 34),
    'error': (204, 0, 0),
    'default_font': (66, 83, 100),
    'rule_defined_signs': (129, 25, 129),
    'rule_defined': (58, 65, 211),
    'grammar_defined': (195, 142, 47),
    'type_defined': (62, 141, 96),
    'wrapper_type_defined': (9, 108, 21),
    'keyword_defined': (160, 97, 178),
    'encapsulation_defined': (78, 141, 193),
    'class_name': (131, 96, 63),
    'comment': (131, 143, 154),
    'property_value': (201, 97, 105),
}
CONSOLE_LOG_LEVEL_TAGS = {
    'OK': '[OK]',
    'INFO': '[INFO]',
    'WARN': '[WARNING]',
    'ERROR': '[ERROR]',
}
DEFAULT_CONTENT = 'Hello World!'
# Main window
MAIN_WINDOW_TITLE = 'JSD-MBRS Generator'
MAIN_WINDOW_WIDTH = 800
MAIN_WINDOW_HEIGHT = 600
# Help window
HELP_WINDOW_TITLE = 'JSD-MBRS Generator Help Information'
HELP_BUTTON_TEXT = f'{CONSOLE_LOG_LEVEL_TAGS["INFO"]} Click on the Help button to get familiar with the JSD-MBRS Generator syntax or open a Spring Boot project and generate files.'
HELP_WINDOW_WIDTH = 750
HELP_WINDOW_HEIGHT = 400
# Save window
SAVE_WINDOW_TITLE = 'Save Grammar'
SAVE_WINDOW_WIDTH = 250
SAVE_WINDOW_HEIGHT = 150
# Predefined words
RULE_DEFINED_SIGNS = [':', ';', '=', '{', '}', '[', ']', '(', ')', ',']
RULE_DEFINED_WORDS = ['Database', 'class', 'Constructors', 'Methods', 'toString']
GRAMMAR_DEFINED_WORDS = ['driver', 'database name', 'username', 'password', 'public', 'abstract', 'final', 'empty', 'default', 'static', 'id', 'identifier', 'uniqueId', 'key', 'primaryKey', 'yes', 'no', '1-1', '1-n', 'n-1', 'n-n']
TYPE_DEFINED_WORDS = ['byte', 'short', 'char', 'int', 'float', 'long', 'double', 'boolean', 'string', 'date', 'time', 'datetime']
WRAPPER_TYPE_DEFINED_WORDS = ['Integer', 'Float', 'Double', 'Boolean']
KEYWORD_DEFINED_WORDS = ['constant', 'const', 'array', 'linked', 'hashmap', 'hashset', 'treemap', 'list',  'void']
ENCAPSULATION_DEFINED_WORDS = ['getter', 'get', 'setter', 'set']

# TEXTX GRAMMAR
# Folders
JSD_MBRS_GENERATOR_FOLDER = 'jsd_mbrs_generator'
GRAMMAR_FOLDER = 'grammar'
RESOURCES_FOLDER = 'resources'
EXPORT_FOLDER = 'export'
EXPORT_DOT_FOLDER = 'dot'
EXPORT_PLANTUML_FOLDER = 'plantuml'
# Files
GRAMMAR_FILE = 'jsd_mbrs_generator_grammar.tx'
HELP_FILE = 'help.txt'
# Other
OK = 'OK'
WARNING = 'WARNING'
ERROR = 'ERROR'
DOT_FILE_EXTENSION = '.dot'
PLANTUML_FILE_EXTENSION = '.pu'
PNG_FILE_EXTENSION = '.png'
JSD_MBRS_GENERATOR_EXTENSION = '.jsdmbrs'
METAMODEL_NAME = 'metamodel'
MODEL_NAME = f'model{DOT_FILE_EXTENSION}'

# CUSTOM ERROR MESSAGES
JAVA_CLASS_NAME_ERROR = 'To create a valid Java class name, start with an uppercase letter, followed by letters, digit, dollar signs, or underscores. No spaces or special characters like @, !, # are allowed.'
JAVA_VARIABLE_NAME_ERROR = 'To create a valid Java variable name, start with a letter, dollar sign, or underscore, followed by letters, digits, dollar signs, or underscores. No spaces or special characters like @, !, # are allowed.'

# REGEX
PLANTUML_REGEX = r'^plantuml-\d+\.\d+\.\d+\.jar$'
JSD_MBRS_GENERATOR_REGEX = r'\w+\.jsdmbrs$'
DATE_REGEX = r'%Y-%m-%d'
TIME_REGEX = r'%H:%M:%S'
DATETIME_REGEX = r'%Y-%m-%d %H:%M:%S'
JAVA_CLASS_NAME_REGEX = r'^[A-Z][a-zA-Z0-9_$]*$'
JAVA_VARIABLE_NAME_REGEX = r'^[a-zA-Z_$][a-zA-Z\d_$]*$'
SYNTAX_ERROR_MESSAGE_REGEX = r'(.*?)at position.*?=>(.*)'
QUOTE_REGEX = r"'(.*?)'"
RULE_DEFINED_SIGNS_REGEX = r'[:;=\{\}\[\]\(\),]'
CLASS_NAME_REGEX = r'class\s+(\w+)\s*\{'
PROPERTY_VALUE_REGEX = r'=(.*?);'
COMMENT_REGEX = r'//(.*)'

# PROPERTY TYPES
# IDTypes
ID = 'id'
IDENTIFIER = 'identifier'
UNIQUE_ID = 'uniqueId'
KEY = 'key'
PRIMARY_KEY = 'primaryKey'
# PrimitiveDataTypes
BYTE = 'byte'
SHORT = 'short'
CHAR = 'char'
INT = 'int'
FLOAT = 'float'
LONG = 'long'
DOUBLE = 'double'
BOOLEAN = 'boolean'
# WrapperDataTypes
INTEGER_W = 'Integer'
FLOAT_W = 'Float'
DOUBLE_W = 'Double'
BOOLEAN_W = 'Boolean'
# OtherDataTypes
STRING = 'string'
# DateTypes
DATE = 'date'
TIME = 'time'
DATETIME = 'datetime'
# ListTypes
ARRAY = 'array'
LINKED = 'linked'
HASHMAP = 'hashmap'
HASHSET = 'hashset'
TREEMAP = 'treemap'
LIST = 'list'
# Custom error messages per property type
ERROR_MESSAGES = {
    # PrimitiveDataTypes
    BYTE: f'{BYTE.capitalize()} value must be a number between -128 and 127',
    SHORT: f'{SHORT.capitalize()} value must be a number between -32768 and 32767',
    CHAR: f'{CHAR.capitalize()} value must be a single character string surrounded by single quotes - \'\'',
    INT: f'{INT.capitalize()} value must be a number between -2147483648 and 2147483647',
    FLOAT: f'{FLOAT.capitalize()} value must be a float or an integer number that ends with "F"',
    LONG: f'{LONG.capitalize()} value must be a number between -9223372036854775808 and 9223372036854775807 that ends with "L"',
    DOUBLE: f'{DOUBLE.capitalize()} value must be a float or an integer number that ends with "D"',
    BOOLEAN: f'{BOOLEAN.capitalize()} value must be "true" or "false"',
    
    # WrapperDataTypes
    INTEGER_W: f'{INTEGER_W.capitalize()} value must be a number between -2147483648 and 2147483647',
    FLOAT_W: f'{FLOAT_W.capitalize()} value must be a float or an integer number that ends with "F"',
    DOUBLE_W: f'{DOUBLE_W.capitalize()} value must be a float or an integer number that ends with "D"',
    BOOLEAN_W: f'{BOOLEAN_W.capitalize()} value must be "true" or "false"',
    
    # OtherDataTypes
    STRING: f'{STRING.capitalize()} value must be surrounded by double quotes - ""',
    
    # DateTypes
    DATE: f'{DATE.capitalize()} value must be in YYYY-MM-DD format',
    TIME: f'{TIME.capitalize()} value must be in HH:MM:SS format',
    DATETIME: f'{DATETIME.capitalize()} value must be in YYYY-MM-DD HH:MM:SS format',
    
    # ListTypes
    ARRAY: f'{ARRAY.capitalize()} type must start with "[" and end with "]"',
    LINKED: f'{LINKED.capitalize()} type must start with "[" and end with "]"',
    HASHMAP: f'{HASHMAP.capitalize()} type must start with "[" and end with "]"',
    HASHSET: f'{HASHSET.capitalize()} type must start with "[" and end with "]"',
    TREEMAP: f'{TREEMAP.capitalize()} type must start with "[" and end with "]"',
    LIST: f'{LIST.capitalize()} type must start with "[" and end with "]"',
}

# OTHER
BUILD_TOOL_FILE_MAPPING = {
    'Gradle-Groovy': 'build.gradle',
    'Gradle-Kotlin': 'build.gradle.kts',
    'Maven': 'pom.xml'
}
KEYSYMS_TO_IGNORE = ['Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R', 'Left', 'Right', 'Up', 'Down']