import logging

import src.error_handler as eh
from src.gui import MainWindowGUI
from src.logging_config import setup_logging


def launch():
    """
    Function to launch the GUI.
    """
    try:
        logging.info('Launching GUI')
        gui = MainWindowGUI()
        gui.run()
    except (eh.MetamodelCreationError, eh.ModelCreationError, FileNotFoundError):
        raise
    except Exception as e:
        logging.error(f'An unexpected error occurred: {e}')
        raise


if __name__ == '__main__':
    setup_logging()
    launch()
