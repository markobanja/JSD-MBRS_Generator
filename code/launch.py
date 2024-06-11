import logging
import error_handler as eh
from gui import GUI
from logging_config import setup_logging


def launch():
    """
    Function to launch the GUI.
    """
    try:
        logging.info('Launching GUI')
        gui = GUI()
        gui.run()
    except (eh.MetamodelCreationError, eh.ModelCreationError, FileNotFoundError) as e:
        raise
    except Exception as e:
        logging.error(f'An unexpected error occurred: {e}')
        raise

if __name__ == '__main__':
    setup_logging()
    launch()