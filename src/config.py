# GUI
THEME_STYLE = 'plastik'
FONT = 'Courier New'
CODE_FONT = 'Cascadia Code'
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
LOADING_SYMBOLS = ["⠋", "⠙", "⠚", "⠞", "⠖", "⠦", "⠴", "⠲", "⠳", "⠓"]
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
GRAMMAR_DEFINED_WORDS = ['DB driver', 'DB name', 'DB username', 'DB password', 'public', 'abstract', 'final', 'private', 'protected', 'empty', 'default', 'static', 'id', 'identifier', 'uniqueId', 'key', 'primaryKey', 'yes', 'no', '1..1', '1..*', '*..1', '*..*', '+']
TYPE_DEFINED_WORDS = ['byte', 'short', 'char', 'int', 'float', 'long', 'double', 'boolean', 'str', 'string', 'String', 'date', 'time', 'datetime']
WRAPPER_TYPE_DEFINED_WORDS = ['Byte', 'Short', 'Character', 'Integer', 'Float', 'Long', 'Double', 'Boolean']
KEYWORD_DEFINED_WORDS = ['constant', 'const', 'array', 'linked', 'hashmap', 'hashset', 'treemap', 'list',  'void', 'postgresql', 'mysql', 'sqlserver', 'oracle']
ENCAPSULATION_DEFINED_WORDS = ['getter', 'get', 'setter', 'set']
# Other
KEYSYMS_TO_IGNORE = ['Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R', 'Left', 'Right', 'Up', 'Down']

# BUILD TOOLS DEFINITION AND DEPENDENCIES
# Build tool file names
MAVEN = 'Maven'
GRADLE_GROOVY = 'Gradle-Groovy'
GRADLE_KOTLIN = 'Gradle-Kotlin'
BUILD_TOOL_FILE_MAPPING = {
    MAVEN: 'pom.xml',
    GRADLE_GROOVY: 'build.gradle',
    GRADLE_KOTLIN: 'build.gradle.kts',
}
# Build tool dependencies
DEPENDENCIES_TO_CHECK = {
    GRADLE_GROOVY: {
        'Spring Web': "implementation 'org.springframework.boot:spring-boot-starter-web'",
        'Spring Data JPA': "implementation 'org.springframework.boot:spring-boot-starter-data-jpa'",
        'Swagger UI': "implementation 'org.springdoc:springdoc-openapi-starter-webmvc-ui:2.6.0'",
    },
    GRADLE_KOTLIN: {
        'Spring Web': 'implementation("org.springframework.boot:spring-boot-starter-web")',
        'Spring Data JPA': 'implementation("org.springframework.boot:spring-boot-starter-data-jpa")',
        'Swagger UI': 'implementation("org.springdoc:springdoc-openapi-starter-webmvc-ui:2.6.0")',
    },
    MAVEN: {
        'Spring Web': '<dependency>\n\t\t\t<groupId>org.springframework.boot</groupId>\n\t\t\t<artifactId>spring-boot-starter-web</artifactId>\n\t\t</dependency>',
        'Spring Data JPA': '<dependency>\n\t\t\t<groupId>org.springframework.boot</groupId>\n\t\t\t<artifactId>spring-boot-starter-data-jpa</artifactId>\n\t\t</dependency>',
        'Swagger UI': '<dependency>\n\t\t\t<groupId>org.springdoc</groupId>\n\t\t\t<artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>\n\t\t\t<version>2.6.0</version>\n\t\t</dependency>',
    },
}
DATABASE_MAPPINGS = {
    'postgresql':{
        'name': 'PostgreSQL',
        'url': 'jdbc:postgresql://localhost:5432/',
        'driver': 'org.postgresql.Driver',
        'dialect': 'org.hibernate.dialect.PostgreSQLDialect',
    },
    'mysql':{
        'name': 'MySQL',
        'url': 'jdbc:mysql://localhost:3306/',
        'driver': 'com.mysql.cj.jdbc.Driver',
        'dialect': 'org.hibernate.dialect.MySQL8Dialect',
    },
    'sqlserver':{
        'name': 'MS SQL Server',
        'url': 'jdbc:sqlserver://localhost:1433;databaseName=',
        'driver': 'com.microsoft.sqlserver.jdbc.SQLServerDriver',
        'dialect': 'org.hibernate.dialect.SQLServer2012Dialect',
    },
    'oracle':{
        'name': 'Oracle',
        'url': 'jdbc:oracle:thin:@localhost:1521:',
        'driver': 'oracle.jdbc.OracleDriver',
        'dialect': 'org.hibernate.dialect.Oracle12cDialect',
    }
}
DATABASE_DEPENDENCY_MAPPING = {
    GRADLE_GROOVY: {
        'PostgreSQL': "runtimeOnly 'org.postgresql:postgresql'",
        'MySQL': "runtimeOnly 'com.mysql:mysql-connector-j'",
        'MS SQL Server': "runtimeOnly 'com.microsoft.sqlserver:mssql-jdbc'",
        'Oracle': "runtimeOnly 'com.oracle.database.jdbc:ojdbc11'",
    },
    GRADLE_KOTLIN: {
        'PostgreSQL': 'runtimeOnly("org.postgresql:postgresql")',
        'MySQL': 'runtimeOnly("com.mysql:mysql-connector-j")',
        'MS SQL Server': 'runtimeOnly("com.microsoft.sqlserver:mssql-jdbc")',
        'Oracle': 'runtimeOnly("com.oracle.database.jdbc:ojdbc11")',
    },
    MAVEN: {
        'PostgreSQL': '<dependency>\n\t\t\t<groupId>org.postgresql</groupId>\n\t\t\t<artifactId>postgresql</artifactId>\n\t\t\t<scope>runtime</scope>\n\t\t</dependency>',
        'MySQL': '<dependency>\n\t\t\t<groupId>com.mysql</groupId>\n\t\t\t<artifactId>mysql-connector-j</artifactId>\n\t\t\t<scope>runtime</scope>\n\t\t</dependency>',
        'MS SQL Server': '<dependency>\n\t\t\t<groupId>com.microsoft.sqlserver</groupId>\n\t\t\t<artifactId>mssql-jdbc</artifactId>\n\t\t\t<scope>runtime</scope>\n\t\t</dependency>',
        'Oracle': '<dependency>\n\t\t\t<groupId>com.oracle.database.jdbc</groupId>\n\t\t\t<artifactId>ojdbc11</artifactId>\n\t\t\t<scope>runtime</scope>\n\t\t</dependency>',
    },
}
# Build tool regex
GRADLE_REGEX = r"dependencies\s*{\s*([\s\S]*?)\s*}"
MAVEN_REGEX = r"<dependencies>\s*([\s\S]*?)\s*</dependencies>"
BUILD_TOOL_PATTER_REGEX = {
    MAVEN: MAVEN_REGEX,
    GRADLE_GROOVY: GRADLE_REGEX,
    GRADLE_KOTLIN: GRADLE_REGEX,
}
# Spring Boot run commands
CMD_RUN_GENERATED_PROJECT_WINDOW_NAME = 'Run generated JSD-MBR project'
SWAGGER_UI_URL = 'http://localhost:8080/swagger-ui/index.html'
RUN_COMMAND_MAPPING = {
    'Gradle-Groovy': 'gradlew bootRun',
    'Gradle-Kotlin': 'gradlew bootRun',
    'Maven': 'mvnw spring-boot:run',
}

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
PROJECT_RESOURCES_FOLDER = 'src/main/resources'
PROJECT_TEST_JAVA_FOLDER = 'src/test/java'
# Files
GRAMMAR_FILE = 'jsd_mbrs_generator_grammar.tx'
HELP_FILE = 'help.txt'
SPRING_BOOT_APPLICATION_FILE = '*Application.java'
JAVA_CLASS_TEMPLATE_FILE = 'java_class.template'
JAVA_CONTROLLER_TEMPLATE_FILE = 'java_controller.template'
JAVA_SERVICE_TEMPLATE_FILE = 'java_service.template'
JAVA_REPOSITORY_TEMPLATE_FILE = 'java_repository.template'
JAVA_REPOSITORY_CONFIGURATION_TEMPLATE_FILE = 'java_repository_configuration.template'
JAVA_APPLICATION_TEMPLATE_FILE = 'java_application.template'
APPLICATION_PROPERTIES_TEMPLATE_FILE = 'application_properties.template'
JAVA_CLASS_FILE_NAME = '%s.java'
JAVA_CONTROLLER_FILE_NAME = '%sController.java'
JAVA_SERVICE_FILE_NAME = '%sService.java'
JAVA_REPOSITORY_FILE_NAME = '%sRepository.java'
JAVA_REPOSITORY_CONFIGURATION_FILE_NAME = 'RepositoryConfiguration.java'
JAVA_APPLICATION_FILE_NAME = '%sApplication.java'
APPLICATION_PROPERTIES_FILE_NAME = 'application.properties'
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
VALID_RELATIONSHIP_TYPE_MAPPING = {
    '1..1': '1..1',
    '*..*': '*..*',
    '1..*': '*..1',
    '*..1': '1..*'
}

# TEXTX PROPERTY TYPES
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
BYTE_W = 'Byte'
SHORT_W = 'Short'
CHARACTER_W = 'Character'
INTEGER_W = 'Integer'
FLOAT_W = 'Float'
LONG_W = 'Long'
DOUBLE_W = 'Double'
BOOLEAN_W = 'Boolean'
# OtherDataTypes
STR = 'str'
STRING = 'string'
STRING_C = 'String'
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

# CUSTOM ERROR MESSAGES
UNIQUE_CLASS_NAMES_ERROR = 'Class name "%s" already exists! Each class name must be unique.'
DATABASE_NAME_ERROR = '%s database name "%s" is not a valid SQL database name! %s'
DATABASE_DRIVER_ERROR = 'The "%s" database driver dependency is already specified in the Application file and it does not match the provided "%s" database driver! Please either update the database driver in the grammar or modify the existing driver dependency in the Application file.'
DATABASE_USERNAME_ERROR = '%s database username "%s" is not a valid SQL database username! %s'
DATABASE_PASSWORD_ERROR = 'Provided %s database password "%s" is not a valid SQL database password! %s'
CLASS_NAME_ERROR = 'Class name "%s" is not a valid Java class name! %s'
UNIQUE_PROPERTY_NAMES_ERROR = 'Property name "%s" already exists in the "%s" class! Each property name must be unique within a class.'
NO_ID_PROPERTY_ERROR  = 'There is no ID property in the "%s" class! An ID property is required.'
MULTIPLE_ID_PROPERTIES_ERROR = '"%s" class has more than one ID property (%s)! Only one ID property is allowed.'
ENTITY_RELATIONSHIP_PROPERTY_ERROR = 'Class "%s" is missing a bidirectional relationship with the "%s" class. Both classes must have reciprocal relationships defined.'
ENTITY_RELATIONSHIP_OWNER_ERROR = 'The relationship between classes "%s" and "%s" is not properly defined. Ensure that each class correctly specifies its owner and non-owner side for the relationship.'
ENTITY_RELATIONSHIP_TYPE_ERROR = 'The relationship between classes "%s" (%s) and "%s" (%s) is not properly defined. Ensure that each class correctly specifies its relationship type for the relationship.'
EMPTY_CONSTRUCTOR_ERROR = 'There is no empty constructor in the "%s" class! An empty and default constructors are required.'
DEFAULT_CONSTRUCTOR_ERROR = 'There is no default constructor in the "%s" class! An empty and default constructors are required.'
CONSTRUCTOR_PROPERTY_ERROR = 'The "%s" property does not exist in the "%s" class! Only properties defined in the current class can be used in the constructor.'
UNIQUE_CONSTRUCTORS_ERROR = 'The specific constructor "%s" already exists in the "%s" class! Each constructor must be unique within a class.'
UNIQUE_METHODS_ERROR = 'The method "%s"%s already exists in the "%s" class! Each method within a class must be unique, defined by both method name and property types.'
PROPERTY_NAME_ERROR = 'Property name "%s" is not a valid Java variable name! %s'
ID_PROPERTY_NAME_ERROR = '"%s" is defined keyword so it cannot be used as a property name! %s'
ID_PROPERTY_VALUE_ERROR = 'The "%s" property of type "%s" should not have a "const" or "constant" keyword specified and/or value defined! Constant values are not allowed for ID properties.'
ID_PROPERTY_GETTER_ENCAPSULATION_ERROR = 'The "%s" property of type "%s" requires a getter method to be defined! Getter methods are mandatory for ID properties.'
ID_PROPERTY_SETTER_ENCAPSULATION_ERROR = 'The "%s" property of type "%s" should not have a setter method defined! Setter methods are not allowed for ID properties.'
ENTITY_PROPERTY_CONSTANT_ERROR = 'The "%s" property of the "%s" class type cannot be declared as a constant! Constant properties cannot have the type "%s".'
ENTITY_PROPERTY_VALUE_ERROR = 'The "%s" property of the "%s" class type cannot have a defined value. Only constant properties can have a defined value.'
ENTITY_PROPERTY_RELATIONSHIP_ERROR = 'The "%s" property of the "%s" class type must have a relationship! Supported relationships are "1..1" (one-to-one), "1..*" (one-to-many), "*..1" (many-to-one), and "*..*" (many-to-many).'
PROPERTY_RELATIONSHIP_ERROR = 'The "%s" property cannot have a relationship since it is not of a appropriate type! Relationships are only supported by types such as lists and classes.'
LIST_TYPE_AND_RELATIONSHIP_ERROR = 'The "%s" list property does not support the relationships! Relationships are designed to establish relationships between classes, not for basic data types or collections of basic data types.'
PROPERTY_TYPE_AND_LIST_TYPE_ERROR = 'The "%s" property cannot have both a "%s" property type and "%s" list type simultaneously. Only reference types (objects) such as "Byte", "Short", "Character", "Integer", "Float", "Long", "Double", "Boolean", or "String" can be used.'
CONSTANT_AND_VALUE_ERROR = 'If "const" or "constant" keyword is specified, constant value is mandatory, and vice versa! In this case, %s is missing for "%s".'
CONSTANT_AND_ENCAPSULATION_ERROR = 'Constant property "%s" cannot have setter method! Constant properties can only have getter methods.'
CONSTANT_PROPERTY_VALUE_ERROR = 'Invalid value "%s" for property "%s" of type "%s" (%s)!'
LIST_ELEMENTS_ERROR = 'Invalid value "%s" in "%s" %s for property "%s" of type "%s" (%s)!'
CONSTRUCTOR_UNIQUE_PROPERTIES_ERROR = 'The specified constructor includes the property "%s", which is defined more than once! Constructors cannot include non-unique properties.'
CONSTRUCTOR_CONSTANT_PROPERTY_ERROR = 'The specified constructor includes the property "%s", which is defined as a constant! Constructors cannot include properties that are constants.'
METHOD_NAME_ERROR = 'Method name "%s" is not a valid Java method name! %s'
METHOD_TYPE_IN_LIST_TYPE_ERROR = 'The method type "%s" is not valid for the list type "%s"! Only wrapper types such as "Byte", "Short", "Character", "Integer", "Float", "Long", "Double", "Boolean", or "String" can be used for list methods.'
UNKNOWN_OBJECT_ERROR = '%s! Please ensure that "%s" is a valid grammar object or check for any typos.'
IS_NOT_UNIQUE_ERROR = 'Please ensure that the "%s" property is unique across all classes. Unfortunately, the JSD-MBRS Generator currently supports only unique properties across all classes.'
# Additional Java explanation messages
JAVA_CLASS_NAME_ERROR = 'To create a valid Java class name, start with an uppercase letter, followed by letters, digit, dollar signs, or underscores. No spaces or special characters like @, !, # are allowed.'
JAVA_PROPERTY_AND_METHOD_NAME_ERROR = 'To create a valid Java variable name, start with a letter, dollar sign, or underscore, followed by letters (uppercase or lowercase), digits, dollar signs, or underscores. No spaces or special characters like @, !, # are allowed.'
SQL_DATABASE_NAME_ERROR = 'To create an appropriate SQL database name, ensure it starts with a letter or underscore and is followed by any combination of letters, numbers, or underscores. No spaces or special characters like @, !, # are allowed.'
SQL_DATABASE_USERNAME_ERROR = 'To create a suitable SQL database username, begin with a letter and follow with any combination of letters, numbers, underscores, or hyphens. No spaces or special characters like @, !, # are allowed.'
SQL_DATABASE_PASSWORD_ERROR = 'To create a strong password, ensure it is at least 8 characters long and includes at least one uppercase letter, one lowercase letter, and one digit.'

# REGEX
PLANTUML_REGEX = r'^plantuml-\d+\.\d+\.\d+\.jar$'
GOOGLE_FORMAT_REGEX = r'^google-java-format-\d+\.\d+\.\d+\-all-deps.jar$'
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
IS_NOT_UNIQUE_ERROR_MESSAGE_REGEX = r'name (.+?) is not unique\.'
JINJA_SUBPROCESS_ERROR_REGEX = r'src\\main\\java.*'
QUOTE_REGEX = r"'(.*?)'"
RULE_DEFINED_SIGNS_REGEX = r'[:;=\{\}\[\]\(\),]'
CLASS_NAME_REGEX = r'class\s+(\w+)\s*\{'
PROPERTY_VALUE_REGEX = r'=(.*?);'
COMMENT_REGEX = r'//(.*)'
OPEN_API_DEFINITION_REGEX = r'@OpenAPIDefinition'

# JINJA MAPPINGS
VOWELS = ['a', 'e', 'i', 'o', 'u']
# Java type mappings
MAP_JAVA_TYPES = {
    DATE: 'LocalDate',
    TIME: 'LocalTime',
    DATETIME: 'LocalDateTime',
    ARRAY: 'ArrayList',
    LINKED: 'LinkedList',
    HASHMAP: 'HashMap',
    HASHSET: 'HashSet',
    TREEMAP: 'TreeMap'
}
LIST_TYPE_MAPPING = {
    LIST: '{}[]',
    ARRAY: 'List<{}>',
    LINKED: 'List<{}>',
    HASHMAP: 'Map<String, {}>',
    HASHSET: 'Set<{}>',
    TREEMAP: 'Map<String, {}>',
}
METHOD_LIST_TYPE_MAPPING = {
    LIST: 'List<{}>',
    ARRAY: 'ArrayList<{}>',
    LINKED: 'LinkedList<{}>',
    HASHMAP: 'HashMap<String, {}>',
    HASHSET: 'HashSet<{}>',
    TREEMAP: 'TreeMap<String, {}>',
}
METHOD_LIST_DEFAULT_VALUE_MAPPING = {
    LIST: 'new ArrayList<{}>()',
    ARRAY: 'new ArrayList<{}>()',
    LINKED: 'new LinkedList<{}>()',
    HASHMAP: 'new HashMap<String, {}>()',
    HASHSET: 'new HashSet<{}>()',
    TREEMAP: 'new TreeMap<String, {}>()',
}
REPOSITORY_CONFIGURATION_LIST_TYPE_MAPPING = {
    LIST: 'new {}[] {{}}',
    ARRAY: 'new ArrayList<{}>()',
    LINKED: 'new LinkedList<{}>()',
    HASHMAP: 'new HashMap<String, {}>()',
    HASHSET: 'new HashSet<{}>()',
    TREEMAP: 'new TreeMap<String, {}>()',
}
RELATIONSHIP_TYPE_MAPPING = {
    '1..1': '@OneToOne',
    '1..*': '@OneToMany',
    '*..1': '@ManyToOne',
    '*..*': '@ManyToMany',
}

# CUSTOM ERROR MESSAGES PER PROPERTY TYPE
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
    BYTE_W: f'{BYTE_W} value must be a number between -128 and 127',
    SHORT_W: f'{SHORT_W} value must be a number between -32768 and 32767',
    CHARACTER_W: f'{CHARACTER_W} value must be a single character string surrounded by single quotes - \'\'',
    INTEGER_W: f'{INTEGER_W} value must be a number between -2147483648 and 2147483647',
    FLOAT_W: f'{FLOAT_W} value must be a float or an integer number that ends with "F"',
    LONG_W: f'{LONG_W} value must be a number between -9223372036854775808 and 9223372036854775807 that ends with "L"',
    DOUBLE_W: f'{DOUBLE_W} value must be a float or an integer number that ends with "D"',
    BOOLEAN_W: f'{BOOLEAN_W} value must be "true" or "false"',
    
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
