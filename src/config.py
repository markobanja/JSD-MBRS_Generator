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
    'property_value': (210, 137, 137),
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
# # Save window
SAVE_WINDOW_TITLE = 'Save Grammar'
SAVE_WINDOW_WIDTH = 250
SAVE_WINDOW_HEIGHT = 150
# Predefined words
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
TEMPLATE_FOLDER = 'template'
EXPORT_FOLDER = 'export'
EXPORT_DOT_FOLDER = 'dot'
EXPORT_PLANTUML_FOLDER = 'plantuml'
PROJECT_JAVA_FOLDER = 'src/main/java'
# Files
GRAMMAR_FILE = 'jsd_mbrs_generator_grammar.tx'
HELP_FILE = 'help.txt'
SPRING_BOOT_APPLICATION_FILE = '*Application.java'
JAVA_CLASS_TEMPLATE_FILE = 'java_class.template'
JAVA_FILE_NAME = '%s.java'
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
UNIQUE_CLASS_NAMES_ERROR = 'Class name "%s" already exists! Each class name must be unique.'
DATABASE_NAME_ERROR = '%s database name "%s" is not a valid SQL database name! %s'
DATABASE_USERNAME_ERROR = '%s database username "%s" is not a valid SQL database username! %s'
DATABASE_PASSWORD_ERROR = 'Provided %s database password "%s" is not a valid SQL database password! %s'
CLASS_NAME_ERROR = 'Class name "%s" is not a valid Java class name! %s'
UNIQUE_PROPERTY_NAMES_ERROR = 'Property name "%s" already exists in the "%s" class! Each property name must be unique within a class.'
NO_ID_PROPERTY_ERROR  = 'There is no ID property in the "%s" class! An ID property is required.'
MULTIPLE_ID_PROPERTIES_ERROR = '"%s" class has more than one ID property (%s)! Only one ID property is allowed.'
EMPTY_CONSTRUCTOR_ERROR = 'There is no empty constructor in the "%s" class! An empty constructor is required.'
UNIQUE_CONSTRUCTORS_ERROR = 'The specific constructor "%s" already exists in the "%s" class! Each constructor must be unique within a class.'
UNIQUE_METHODS_ERROR = 'The method "%s"%s already exists in the "%s" class! Each method within a class must be unique, defined by both name and properties.'
PROPERTY_NAME_ERROR = 'Property name "%s" is not a valid Java variable name! %s'
ID_PROPERTY_VALUE_ERROR = 'The "%s" property of type "%s" should not have a "const" or "constant" keyword specified and/or value defined! Constant values are not allowed for ID properties.'
ID_PROPERTY_GETTER_ENCAPSULATION_ERROR = 'The "%s" property of type "%s" requires a getter method to be defined! Getter methods are mandatory for ID properties.'
ID_PROPERTY_SETTER_ENCAPSULATION_ERROR = 'The "%s" property of type "%s" should not have a setter method defined! Setter methods are not allowed for ID properties.'
ENTITY_PROPERTY_CONSTANT_ERROR = 'The "%s" property of the "%s" class type cannot be declared as a constant! Constant properties cannot have the type "%s".'
ENTITY_PROPERTY_VALUE_ERROR = 'The "%s" property of the "%s" class type cannot have a defined value. Only constant properties can have a defined value.'
ENTITY_PROPERTY_RELATIONSHIP_ERROR = 'The "%s" property of the "%s" class type must have a relationship! Supported relationships are "1-1" (one-to-one), "1-n" (one-to-many), "n-1" (many-to-one), and "n-n" (many-to-many).'
ENTITY_PROPERTY_LIST_RELATIONSHIP_ERROR = 'The "%s" list property of the "%s" class type does not support the "%s" relationship! "%s" properties support "1-n" (one-to-many), "n-1" (many-to-one), and "n-n" (many-to-many) relationships.'
ENTITY_PROPERTY_NON_LIST_RELATIONSHIP_ERROR = 'The "%s" property of the "%s" class type does not support the "%s" relationship! "%s" properties support only "1-1" (one-to-one) relationship.'
PROPERTY_RELATIONSHIP_ERROR = 'The "%s" property cannot have a relationship since it is not of a appropriate type! Only lists and classes support relationships.'
CONSTANT_AND_VALUE_ERROR = 'If "const" or "constant" keyword is specified, constant value is mandatory, and vice versa! In this case, %s is missing for "%s".'
CONSTANT_AND_ENCAPSULATION_ERROR = 'Constant property "%s" cannot have setter method! Constant properties can only have getter methods.'
CONSTANT_PROPERTY_VALUE_ERROR = 'Invalid value "%s" for property "%s" of type "%s" (%s)!'
LIST_ELEMENTS_ERROR = 'Invalid value "%s" in "%s" %s for property "%s" of type "%s" (%s)!'
CONSTRUCTOR_UNIQUE_PROPERTIES_ERROR = 'The specified constructor includes the property "%s", which is defined more than once! Constructors cannot include non-unique properties.'
CONSTRUCTOR_CONSTANT_PROPERTY_ERROR = 'The specified constructor includes the property "%s", which is defined as a constant! Constructors cannot include properties that are constants.'
METHOD_NAME_ERROR = 'Method name "%s" is not a valid Java method name! %s'
# Additional Java explanation messages
JAVA_CLASS_NAME_ERROR = 'To create a valid Java class name, start with an uppercase letter, followed by letters, digit, dollar signs, or underscores. No spaces or special characters like @, !, # are allowed.'
JAVA_PROPERTY_AND_METHOD_NAME_ERROR = 'To create a valid Java variable name, start with a letter, dollar sign, or underscore, followed by letters (uppercase or lowercase), digits, dollar signs, or underscores. No spaces or special characters like @, !, # are allowed.'
SQL_DATABASE_NAME_ERROR = 'To create an appropriate SQL database name, ensure it starts with a letter or underscore and is followed by any combination of letters, numbers, or underscores. No spaces or special characters like @, !, # are allowed.'
SQL_DATABASE_USERNAME_ERROR = 'To create a suitable SQL database username, begin with a letter and follow with any combination of letters, numbers, underscores, or hyphens. No spaces or special characters like @, !, # are allowed.'
SQL_DATABASE_PASSWORD_ERROR = 'To create a strong password, ensure it is at least 8 characters long and includes at least one uppercase letter, one lowercase letter, and one digit.'

# REGEX
PLANTUML_REGEX = r'^plantuml-\d+\.\d+\.\d+\.jar$'
JSD_MBRS_GENERATOR_REGEX = r'\w+\.jsdmbrs$'
DATE_REGEX = r'%Y-%m-%d'
TIME_REGEX = r'%H:%M:%S'
DATETIME_REGEX = r'%Y-%m-%d %H:%M:%S'
JAVA_CLASS_NAME_REGEX = r'^[A-Z][a-zA-Z0-9_$]*$'
JAVA_PROPERTY_AND_METHOD_NAME_REGEX = r'^[a-zA-Z_$][a-zA-Z\d_$]*$'
SQL_DATABASE_NAME_REGEX = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
SQL_DATABASE_USERNAME_REGEX = r'^[a-zA-Z][a-zA-Z0-9_\-]*$'
SQL_DATABASE_PASSWORD_REGEX = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d]{8,}$'
SYNTAX_ERROR_MESSAGE_REGEX = r'(.*?)at position.*?=>(.*)'
UNKNOWN_OBJECT_ERROR_MESSAGE_REGEX = r'Unknown object "(.*?)" of class "(.*?)"'
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