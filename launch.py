import logging
from config.logging_config import setup_logging
from code.gui import GUI


def launch():
    """
    Function to launch the GUI.
    """
    try:
        logging.info('Launching GUI')
        GUI().run()  # Create and run the GUI
    except Exception as e:
        logging.error(f'An unexpected error occurred while launching the GUI: {e}', exc_info=True)


if __name__ == '__main__':
    setup_logging()  # Set up logging
    launch()