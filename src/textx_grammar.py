import logging
import subprocess

import pydot
from textx import TextXSyntaxError, TextXSemanticError, metamodel_from_file, get_location
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
            model = self.get_model(metamodel, file_path, grammar_file_name)
            logging.info('Metamodel and model generated successfully')
            self.set_metamodel(self, metamodel)
            self.set_model(self, model)
            return cfg.OK
        except TextXSyntaxError as e:
            # TODO: create syntax error message handler to display better error messages
            error_msg = f'at position ({str(e.line)},{str(e.col)}): {str(e.message)}'
            logging.error(f'Error during syntax checks: {str(e.message)}')
            return error_msg
        except TextXSemanticError as e:
            error_msg = f'at position ({str(e.line)},{str(e.col)}): {str(e.message)}'
            logging.error(f'Error during semantic checks: {str(e.message)}')
            return error_msg
        except Exception as e:
            error_msg = f'{str(e)}'
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
        
        # Register object processors to validate (or alter) the object being constructed
        metamodel.register_obj_processors({
            'EntityModel': lambda model: self.model_processor(self, model),
            'Entity': lambda entity: self.entity_processor(self, entity),
            'Property': lambda property: self.property_processor(self, property),
        })

        logging.info('Metamodel generated')
        return metamodel

    def get_model(metamodel, model_file_path, grammar_file_name):
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
                result = self.execute_dot_cmd_command(metamodel_name, metamodel_path)
            else:
                # Export the metamodel using the 'PlantUML' tool
                logging.info('Exporting metamodel using PlantUML tool')
                metamodel_name = f'{cfg.METAMODEL_NAME}{cfg.PLANTUML_FILE_EXTENSION}'
                metamodel_export_path = utils.get_path(metamodel_path, metamodel_name)
                metamodel_export(self.metamodel, metamodel_export_path, renderer=PlantUmlRenderer())
                result = self.execute_plantuml_cmd_command(metamodel_name, metamodel_path)
            
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
        result = self.execute_dot_cmd_command(cfg.MODEL_NAME, model_export_path)
        return result

    def execute_dot_cmd_command(file_name, folder_path):
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

    def execute_plantuml_cmd_command(file_name, folder_path):
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

    def model_processor(self, model):
        """
        Perform semantic checks on the model.
        """
        logging.info(f'Starting semantic checks for JSD-MBRS Generator "{model.__class__.__name__}"')
        self.check_unique_class_names(model)
        logging.info(f'Successfully finished semantic checks for JSD-MBRS Generator "{model.__class__.__name__}"')

    def entity_processor(self, entity):
        """
        Perform semantic checks on each class in the model.
        """
        logging.info(f'Starting semantic checks for class "{entity.name}"')
        self.check_class_name(entity)
        self.check_unique_property_names(entity)
        self.check_id_property(entity)
        self.check_empty_constructor(entity)
        self.check_unique_constructors(self, entity)
        self.check_unique_methods(entity)
        logging.info(f'Successfully finished semantic checks for class "{entity.name}"')

    def property_processor(self, property):
        """
        Perform semantic checks on each property in the model.
        """
        logging.info(f'Updating variables for property "{property.name}"')
        self.add_variables_to_property(property)
        logging.info(f'Starting semantic checks for property "{property.name}"')

    # MODEL SEMANTIC CHECKS
    def check_unique_class_names(model):
        """
        Check if class names are unique.
        Raise a TextXSemanticError if a class name is not unique.
        """
        class_names = set()
        for entity in model.entities:
            if entity.name in class_names:
                error_message = f'Class name "{entity.name}" already exists! Each class name must be unique.'
                logging.error(error_message)
                raise TextXSemanticError(error_message, **get_location(entity), err_type='unique_class_names_error')
            class_names.add(entity.name)

    # CLASS SEMANTIC CHECKS
    def check_class_name(entity):
        """
        Check if the class name is a valid Java class name.
        Raise a TextXSemanticError if the class name is not valid.
        """
        if not utils.check_value_regex(cfg.JAVA_CLASS_NAME_REGEX, entity.name):
            error_message = f'Class name "{entity.name}" is not a valid Java class name! {cfg.JAVA_CLASS_NAME_ERROR}'
            logging.error(error_message)
            raise TextXSemanticError(error_message, **get_location(entity), err_type='class_name_error')
        
    def check_unique_property_names(entity):
        """
        Check if property names are unique within a class.
        Raise a TextXSemanticError if a property name is not unique.
        """
        property_names = set()
        for property in entity.properties:
            if property.name in property_names:
                error_message = f'Property name "{property.name}" already exists in the "{entity.name}" class! Each property name must be unique within a class.'
                logging.error(error_message)
                raise TextXSemanticError(error_message, **get_location(property), err_type='unique_property_names_error')
            property_names.add(property.name)

    def check_id_property(entity):
        """
        Check if the class has a primary key property and if it is unique'.
        Raise a TextXSemanticError if the primary key property is not present or if it is not unique.
        """
        id_type_count = 0
        for property in entity.properties:
            if property.property_type.primary_key:
                id_type_count += 1

        if id_type_count == 0:
            error_message = f'There is no ID property in the {entity.name} class! An ID property is required.'
            logging.error(error_message)
            raise TextXSemanticError(error_message, **get_location(entity), err_type='id_property_error')
        elif id_type_count > 1:
            error_message = f'{entity.name} class has more than one ID property! Only one ID property is allowed.'
            logging.error(error_message)
            raise TextXSemanticError(error_message, **get_location(entity), err_type='id_property_error')
        
    def check_empty_constructor(entity):
        """
        Check if the empty constructor is provided.
        Raise a TextXSemanticError if the empty constructor is not provided.
        """
        empty_constructors = [constructor for constructor in entity.constructors if constructor.empty_constructor]
        last_constructor = entity.constructors[-1]
        if len(empty_constructors) == 0:
            error_message = f'There is no empty constructor in the "{entity.name}" class! An empty constructor is required.'
            logging.error(error_message)
            raise TextXSemanticError(error_message, **get_location(last_constructor), err_type='empty_constructor_error')
        
    def check_unique_constructors(self, entity):
        """
        Check if the constructors are unique within a class.
        Raise a TextXSemanticError if a constructor is not unique.
        """
        constructors = set()
        for constructor in entity.constructors:
            constructor_name = self.create_constructor_name(constructor)
            if constructor_name in constructors:
                error_message = f'The specific constructor "{constructor_name}" already exists in the "{entity.name}" class! Each constructor must be unique within a class.'
                logging.error(error_message)
                raise TextXSemanticError(error_message, **get_location(constructor), err_type='unique_constructors_error')
            constructors.add(constructor_name)

    def check_unique_methods(entity):
        """
        Check if the methods are unique within a class.
        Raise a TextXSemanticError if a method is not unique.
        """
        methods = set()
        for method in entity.methods:
            method_properties = ', '.join(property.name for property in method.property_list)
            method_name = f'{method.name}({method_properties})'
            if method_name in methods:
                additional_text = f' with properties "({method_properties})"' if method_properties else ''
                error_message = f'The method "{method.name}"{additional_text} already exists in the "{entity.name}" class! Each method within a class must be unique, defined by both name and properties.'
                logging.error(error_message)
                raise TextXSemanticError(error_message, **get_location(method), err_type='unique_methods_error')
            methods.add(method_name)

    # PROPERTY VARIABLE UPDATE
    def add_variables_to_property(property):
        """
        Add necessary variables to the property.
        """
        property_type_name = property.property_type.__class__.__name__
        if property_type_name == 'Entity':
            property.property_type.primary_key = False

    def create_constructor_name(constructor):
        """
        Creates a constructor name from the provided constructor object.
        """
        logging.debug(f'Creating constructor name from the provided constructor')
        if constructor.default_constructor:
            # A default constructor contains all non-constant properties from the class
            constructor.property_list = [property for property in constructor.parent.properties if not property.constant]
            return "default"
        elif constructor.empty_constructor:
            return "empty"
        elif constructor.property_list:
            constructor_property_names = ', '.join(property.name for property in constructor.property_list)
            return f"[{constructor_property_names}]"
        else:
            return None
