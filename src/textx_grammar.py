import logging
import subprocess

import pydot
from textx import metamodel_from_file
from textx.export import PlantUmlRenderer, metamodel_export, model_export

import src.config as cfg
import src.error_handler as eh
import src.grammar_classes as gc
import src.utils as utils


class TextXGrammar():
    """
    Class for generating and exporting the metamodel and model files from the textX grammar file.
    """
    def __init__(self):
        """
        Constructor for the TextXGrammar class.
        """
        self.metamodel = None
        self.model = None

    @classmethod
    def generate(self, project_path, grammar_file_name):
        """
        Generate the metamodel and model from the given project path and grammar file name.
        """
        try:
            logging.info('Generating metamodel and model')
            project_grammar_folder_path = utils.get_path(project_path, cfg.JSD_MBRS_GENERATOR_FOLDER, cfg.GRAMMAR_FOLDER)
            current_grammar_folder_path = utils.get_path(utils.get_current_path(), cfg.GRAMMAR_FOLDER)
            utils.file_exists(current_grammar_folder_path, cfg.GRAMMAR_FILE)
            utils.file_exists(project_grammar_folder_path, grammar_file_name)
            file_path = utils.get_path(project_grammar_folder_path, grammar_file_name)
            metamodel = self.get_metamodel(self, utils.get_path(cfg.GRAMMAR_FOLDER, cfg.GRAMMAR_FILE))
            model = self.get_model(self, metamodel, file_path, grammar_file_name)
            logging.info('Metamodel and model generated successfully')
            self.set_metamodel(self, metamodel)
            self.set_model(self, model)
            return cfg.OK
        except Exception as e:
            error_msg = f'Failed to generate metamodel and model: {str(e)}'
            logging.error(error_msg)
            return error_msg
    
    @classmethod
    def export(self, project_path):
        """
        Export the metamodel and model files to specified paths using different (dot and PlantUML) tools.
        NOTE: PlantUML output is not yet available for model files.
        """
        try:
            metamodel_export_response = self.export_metamodel(self, project_path)
            model_export_response = self.export_model(self, project_path)
            
            # Return 'WARNING' if either metamodel or model export failed with warnings
            if metamodel_export_response == cfg.WARNING or model_export_response == cfg.WARNING:
                logging.info('Export completed successfully with warnings')
                return cfg.WARNING
            
            # Return 'OK' if both metamodel and model export succeeded
            logging.info('Export completed successfully')
            return cfg.OK
        except Exception as e:
            error_msg = f'Failed to export the textX grammar metamodel and/or model: {str(e)}'
            logging.error(error_msg)
            return error_msg

    def get_metamodel(self, grammar_path):
        """
        Get the metamodel from the given grammar file path.
        """
        logging.info(f'Getting metamodel from textX file')
        type_builtins = gc.get_type_builtins()
        # Generate the metamodel from the textX grammar file
        metamodel = metamodel_from_file(grammar_path, 
                                        classes=[gc.IDType, gc.PrimitiveDataType, gc.WrapperDataType, gc.OtherDataType, gc.DateType, gc.ListType],
                                        builtins=type_builtins)

        # Raise an exception if the metamodel is not generated
        if metamodel is None:
            raise eh.MetamodelCreationError('Failed to generate metamodel from textX grammar file!')
        
        logging.info('Metamodel generated')
        return metamodel

    def get_model(self, metamodel, model_file_path, grammar_file_name):
        """
        Get the model from the given metamodel and model file path.
        """
        logging.info(f'Getting model from file: "{grammar_file_name}"')
        # Generate the model from the model file
        model = metamodel.model_from_file(model_file_path)

        # Raise an exception if the metamodel is not generated
        if model is None:
            raise eh.ModelCreationError('Failed to generate model from model file!')
        
        logging.info('Model generated')
        return model
    
    def set_metamodel(self, metamodel):
        """
        Set the metamodel.
        """
        logging.debug('Setting metamodel')
        self.metamodel = metamodel

    def set_model(self, model):
        """
        Set the model.
        """
        logging.debug('Setting model')
        self.model = model

    def export_metamodel(self, project_path):
        """
        Export the metamodel files to specified path using the 'dot' and 'PlantUML' tools.
        """
        has_warning = False
        export_folders = [cfg.EXPORT_DOT_FOLDER, cfg.EXPORT_PLANTUML_FOLDER]
        for folder in export_folders:
            export_folder = utils.get_path(cfg.JSD_MBRS_GENERATOR_FOLDER, cfg.EXPORT_FOLDER, folder)  # e.g. 'export/dot'
            utils.create_folder(project_path, export_folder)
            metamodel_path = utils.get_path(project_path, export_folder)
            if folder == cfg.EXPORT_DOT_FOLDER:
                # Export the metamodel using the 'dot' tool
                logging.info('Exporting metamodel using dot tool')
                metamodel_name = f'{cfg.METAMODEL_NAME}{cfg.DOT_FILE_EXTENSION}'
                metamodel_export_path = utils.get_path(metamodel_path, metamodel_name)
                metamodel_export(self.metamodel, metamodel_export_path)
                result = self.execute_dot_cmd_command(self, metamodel_name, metamodel_path)
            else:
                # Export the metamodel using the 'PlantUML' tool
                logging.info('Exporting metamodel using PlantUML tool')
                metamodel_name = f'{cfg.METAMODEL_NAME}{cfg.PLANTUML_FILE_EXTENSION}'
                metamodel_export_path = utils.get_path(metamodel_path, metamodel_name)
                metamodel_export(self.metamodel, metamodel_export_path, renderer=PlantUmlRenderer())
                result = self.execute_plantuml_cmd_command(self, metamodel_name, metamodel_path)
            
            # Set the flag if the export has warnings
            if result == cfg.WARNING:
                has_warning = True
        
        # Return 'WARNING' if export succeeded with warnings else 'OK'
        return cfg.WARNING if has_warning else cfg.OK

    def export_model(self, project_path):
        """
        Export the model files to specified path using the 'dot' tool (PlantUML output is not yet available for model files).
        """
        logging.info('Exporting model using dot tool')
        model_export_path = utils.get_path(project_path, cfg.JSD_MBRS_GENERATOR_FOLDER, cfg.EXPORT_FOLDER, cfg.EXPORT_DOT_FOLDER)
        model_path = utils.get_path(model_export_path, cfg.MODEL_NAME)
        model_export(self.model, model_path)
        result = self.execute_dot_cmd_command(self, cfg.MODEL_NAME, model_export_path)
        return result

    def execute_dot_cmd_command(self, file_name, folder_path):
        """
        Execute the dot command to convert the dot file to PNG format.
        """
        try:
            logging.info(f'Converting DOT file "{file_name}" to PNG')
            dot_file_path = utils.get_path(folder_path, file_name)
            graphs = pydot.graph_from_dot_file(dot_file_path)
            if graphs:
                graph = graphs[0]
                png_file_name = f'{file_name}{cfg.PNG_FILE_EXTENSION}'
                output_file_path = utils.get_path(folder_path, png_file_name)
                graph.write_png(output_file_path)
                logging.info(f'DOT file "{file_name}" converted to "{png_file_name}" successfully')
                return cfg.OK
            else:
                logging.warning(f'No graphs found in "{dot_file_path}"')
                return cfg.WARNING
        except Exception as e:
            logging.error(f'Failed to convert DOT file "{file_name}" to PNG: {str(e)}')
            raise

    def execute_plantuml_cmd_command(self, file_name, folder_path):
        """
        Execute the PlantUML command to convert the PlantUML file to PNG format.
        """
        try:
            logging.info(f'Converting PlantUML file "{file_name}" to PNG')
            utils.folder_exists(cfg.RESOURCES_FOLDER)

            # Find the PlantUML jar file in the resources folder
            plantuml_file_name = utils.find_specific_file_regex(cfg.RESOURCES_FOLDER, cfg.PLANTUML_REGEX)
            if not plantuml_file_name:
                logging.warning(f'No PlantUML jar file found in the "{cfg.RESOURCES_FOLDER}" folder')
                return
            elif len(plantuml_file_name) > 1:
                logging.warning(f'More than one PlantUML jar file found in the "{cfg.RESOURCES_FOLDER}" folder. Using the newest one: {plantuml_file_name[0]}')
            
            current_directory = utils.get_current_path()
            plantuml_path = utils.get_path(current_directory, cfg.RESOURCES_FOLDER, plantuml_file_name[0])
            command = f'java -jar {plantuml_path} -Tpng {file_name}'
            subprocess.run(command, shell=True, check=True, cwd=folder_path, capture_output=True, text=True)
            png_file_name = f'{file_name}{cfg.PNG_FILE_EXTENSION}'
            logging.info(f'PlantUML file "{file_name}" converted to "{png_file_name}" successfully')
            return cfg.OK
        except subprocess.CalledProcessError as e:
            error_message = str(e.stderr).replace('\n', '. ').rstrip('. ')
            logging.warning(f'{error_message}')
            return cfg.WARNING
        except FileNotFoundError as e:
            raise
        except Exception as e:
            logging.error(f'Failed to convert PlantUML file "{file_name}" to PNG: {str(e)}')
            raise