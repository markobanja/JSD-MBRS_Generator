import utils
import logging
import config as cfg
import error_handler as eh
import grammar_classes as gc
from textx import metamodel_from_file

def get_metamodel(grammar_path):
    """
    Get the metamodel from the given grammar file path.
    """
    logging.info(f'Getting metamodel from grammar file: "{grammar_path}"')
    type_builtins = gc.get_type_builtins()
    # Generate the metamodel from the textx grammar file
    metamodel = metamodel_from_file(grammar_path, classes=[gc.IDType, gc.DataType], builtins=type_builtins)

    # Raise an exception if the metamodel is not generated
    if metamodel is None:
        raise eh.MetamodelCreationError('Failed to generate metamodel from textx grammar file!')

    logging.info('Metamodel generated')
    return metamodel

def get_model(metamodel, model_file_path):
    """
    Get the model from the given metamodel and model file path.
    """
    logging.info(f'Getting model from file: "{model_file_path}"')
    # Generate the model from the model file
    model = metamodel.model_from_file(model_file_path)

    # Raise an exception if the metamodel is not generated
    if model is None:
        raise eh.ModelCreationError('Failed to generate model from model file!')

    logging.info('Model generated')
    return model

def test_run():
    """
    Test run to verify the functionality of the textx_grammar module.
    """
    logging.info('Test run started')
    grammar_folder = utils.folder_exists(cfg.GRAMMAR_FOLDER)

    # Check if the grammar folder exists and the grammar file exists in it
    if not grammar_folder or not utils.file_exists(cfg.GRAMMAR_FOLDER, cfg.GRAMMAR_FILE):
        logging.error('The grammar folder or the grammar textx file does not exist in the current directory!')
        raise FileNotFoundError

    entity_metamodel = get_metamodel(utils.get_path(cfg.GRAMMAR_FOLDER, cfg.GRAMMAR_FILE))
    entity_model = get_model(entity_metamodel, utils.get_path(cfg.GRAMMAR_FOLDER, cfg.GRAMMAR_INPUT_FILE))
    print(*[entity.name for entity in entity_model.entities], sep=', ')
    logging.info('Test run finished')
