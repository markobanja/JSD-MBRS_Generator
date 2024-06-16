# GUI
THEME_STYLE = 'plastik'
FONT = 'Courier New'
COLORS = {
    # GUI colors
    'initial_background': (240, 240, 240),
    'working_background': (255, 255, 255),

    # Text colors
    'information': (52, 152, 219),
    'warning': (255, 102, 34),
}
CONSOLE_LOG_LEVEL_TAGS  = {
    'INFO': '[INFO]',
    'WARN': '[WARNING]',
    'ERROR': '[ERROR]',
}
# Main window
MAIN_WINDOW_TITLE = 'JSD-MBRS Generator'
MAIN_WINDOW_WIDTH = 800
MAIN_WINDOW_HEIGHT = 600
# Help window
HELP_WINDOW_TITLE = 'JSD-MBRS Generator Help Information'
HELP_BUTTON_TEXT = f'{CONSOLE_LOG_LEVEL_TAGS["INFO"]} Click on the Help button to get familiar with the JSD-MBRS Generator syntax or open a Spring Boot project and generate files.'
HELP_WINDOW_WIDTH = 750
HELP_WINDOW_HEIGHT = 400

# TEXTX GRAMMAR
GRAMMAR_FOLDER = 'grammar'
GRAMMAR_FILE = 'jsd-mbrs-generator-grammar.tx'
GRAMMAR_INPUT_FILE = 'test_input.jsdmbrs'
RESOURCES_FOLDER = 'resources'
HELP_FILE = 'help.txt'

# OTHER
BUILD_TOOL_FILE_MAPPING = {
    'Gradle-Groovy': 'build.gradle',
    'Gradle-Kotlin': 'build.gradle.kts',
    'Maven': 'pom.xml'
}
