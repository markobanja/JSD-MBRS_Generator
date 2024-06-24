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
DOT_FILE_EXTENSION = '.dot'
PLANTUML_FILE_EXTENSION = '.pu'
PNG_FILE_EXTENSION = '.png'
JSD_MBRS_GENERATOR_EXTENSION = '.jsdmbrs'
METAMODEL_NAME = 'metamodel'
MODEL_NAME = f'model{DOT_FILE_EXTENSION}'

# REGEX
PLANTUML_REGEX = r'^plantuml-\d+\.\d+\.\d+\.jar$'
JSD_MBRS_GENERATOR_REGEX = r"\w+\.jsdmbrs$"

# OTHER
BUILD_TOOL_FILE_MAPPING = {
    'Gradle-Groovy': 'build.gradle',
    'Gradle-Kotlin': 'build.gradle.kts',
    'Maven': 'pom.xml'
}
KEYSYMS_TO_IGNORE = ['Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R', 'Left', 'Right', 'Up', 'Down']
