import logging
import subprocess

import pydot
from textx import TextXSyntaxError, TextXSemanticError, metamodel_from_file, get_location
from textx.export import PlantUmlRenderer, metamodel_export, model_export

import src.config as cfg
import src.error_handler as eh
import src.grammar_classes as gc
import src.utils as utils
from src.jinja import Jinja as jinja


class Response:
    """
    Class for creating the response object from a functions.
    """
    def __init__(self, status, error=None, error_msg=None, near_part=None, found_part=None, error_class=None):
        """
        Constructor for the Response class.
        """
        self.status = status
        self.error = error
        self.error_msg = error_msg
        self.near_part = near_part
        self.found_part = found_part
        self.error_class = error_class


class ValidationResponse:
    """
    Class for creating the response object for the validation check.
    """
    def __init__(self, status, message=None, type=None, search_value=None):
        """
        Constructor for the ValidationResponse class.
        """
        self.status = status
        self.message = message
        self.type = type
        self.search_value = search_value


class SemanticError(TextXSemanticError):
    """
    Class representing a semantic error in TextX.
    Inherits from TextXSemanticError.
    """
    def __init__(self, message, line=None, col=None, err_type=None, expected_obj_cls=None, filename=None, search_value=None):
        """
        Constructor for the SemanticError class.
        """
        super().__init__(message, line, col, err_type, filename)
        self.expected_obj_cls = expected_obj_cls
        self.search_value = search_value


class TextXGrammar:
    """
    Class for handling all kind of work regarding textX grammar files, such as
    generating the metamodel and model, exporting the dot and PlantUML files, doing syntax and semantic checks etc.
    """
    def __init__(self):
        """
        Constructor for the TextXGrammar class.
        """
        self.metamodel = None
        self.model = None
        self.project_path = None
        self.database_driver = None

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

    def set_project_path(self, project_path):
        """
        Set the project path.
        """
        logging.debug(f'Setting project path variable to "{project_path}"')
        self.project_path = project_path

    def set_database_driver(self, database_driver):
        """
        Set the database driver.
        """
        logging.debug(f'Setting database driver variable to "{database_driver}"')
        self.database_driver = database_driver

    @classmethod
    def generate(self, project_path, grammar_file_name, database_driver) -> Response:
        """
        Generate the metamodel and model from the given project path and grammar file name.
        """
        try:
            logging.info('Generating metamodel and model')
            utils.folder_exists(cfg.GRAMMAR_FOLDER)
            self.set_project_path(self, project_path)
            self.set_database_driver(self, database_driver)
            project_grammar_folder_path = utils.get_path(self.project_path, cfg.JSD_MBRS_GENERATOR_FOLDER, cfg.GRAMMAR_FOLDER)
            current_grammar_folder_path = utils.get_path(utils.get_current_path(), cfg.GRAMMAR_FOLDER)
            utils.file_exists(current_grammar_folder_path, cfg.GRAMMAR_FILE)
            utils.file_exists(project_grammar_folder_path, grammar_file_name)
            file_path = utils.get_path(project_grammar_folder_path, grammar_file_name)
            metamodel = self.get_metamodel(self, utils.get_path(cfg.GRAMMAR_FOLDER, cfg.GRAMMAR_FILE))
            model = self.get_model(metamodel, file_path, grammar_file_name)
            self.set_metamodel(self, metamodel)
            self.set_model(self, model)
            logging.info('Metamodel and model generated successfully')
            jinja.generate(model, self.project_path)
            return Response(status=cfg.OK)
        except TextXSyntaxError as e:
            error_msg, near_part, found_part = utils.create_syntax_error_message(e)
            return Response(status=cfg.ERROR, error=e, error_msg=error_msg, near_part=near_part, found_part=found_part, error_class='TextXSyntaxError')
        except (SemanticError, TextXSemanticError) as e:
            error_msg = f'at position ({str(e.line)},{str(e.col)}): {str(e.message)}'
            error_class = type(e).__name__

            # Determine if the error is due to an unknown object
            if e.err_type == 'Unknown object':
                e.search_value = utils.get_unknown_object_name(e)
                error_msg = cfg.UNKNOWN_OBJECT_ERROR % (error_msg, e.search_value)
                return Response(status=cfg.ERROR, error=e, error_msg=error_msg, error_class=error_class)
            
            # Determine if the error is due to an is not unique object
            if str(e.message).endswith('is not unique.'):
                property_name = utils.get_is_not_unique_name(e)
                error_explanation = cfg.IS_NOT_UNIQUE_ERROR % (property_name)
                error_msg = f'at position ({str(e.line)},{str(e.col)}): {error_explanation}'
                return Response(status=cfg.ERROR, error=e, error_msg=error_msg, error_class=error_class)

            return Response(status=cfg.ERROR, error=e, error_msg=error_msg, error_class=error_class)
        except subprocess.CalledProcessError as e:
            jinja_error = utils.extract_jinja_subprocess_output(e.stderr)
            error_msg = f'Error while formatting Jinja template: {jinja_error}'
            logging.error(error_msg)
            return Response(status=cfg.ERROR, error=e, error_msg=error_msg, error_class='CalledProcessError')
        except Exception as e:
            error_msg = f'{str(e)}'
            logging.error(error_msg)
            return Response(status=cfg.ERROR, error=e, error_msg=error_msg, error_class='Exception')

    @classmethod
    def export(self) -> Response:
        """
        Export the metamodel and model files to specified paths using different (dot and PlantUML) tools.
        NOTE: PlantUML output is not yet available for model files.
        """
        try:
            metamodel_export_response = self.export_metamodel(self)
            model_export_response = self.export_model(self)
            
            # Return 'WARNING' if either metamodel or model export failed with warnings
            if metamodel_export_response == cfg.WARNING or model_export_response == cfg.WARNING:
                logging.info('Export completed successfully with warnings')
                return Response(status=cfg.WARNING)
            
            # Return 'OK' if both metamodel and model export succeeded
            logging.info('Export completed successfully')
            return Response(status=cfg.OK)
        except Exception as e:
            error_msg = f'Failed to export the textX grammar metamodel and/or model: {str(e)}'
            logging.error(error_msg)
            return Response(status=cfg.ERROR, error=e, error_msg=error_msg, error_class='Exception')

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
            'Database': lambda database: self.database_processor(self, database),
            'Entity': lambda entity: self.entity_processor(self, entity),
            'Property': lambda property: self.property_processor(self, property),
            'Constructor': lambda constructor: self.constructor_processor(self, constructor),
            'Method': lambda method: self.method_processor(self, method),
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
    
    def export_metamodel(self):
        """
        Export the metamodel files to specified path using the 'dot' and 'PlantUML' tools.
        """
        has_warning = False
        export_folders = [cfg.EXPORT_DOT_FOLDER, cfg.EXPORT_PLANTUML_FOLDER]
        for folder in export_folders:
            export_folder = utils.get_path(cfg.JSD_MBRS_GENERATOR_FOLDER, cfg.EXPORT_FOLDER, folder)  # e.g. 'export/dot'
            utils.create_folder(self.project_path, export_folder)
            metamodel_path = utils.get_path(self.project_path, export_folder)
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

    def export_model(self):
        """
        Export the model files to specified path using the 'dot' tool (PlantUML output is not yet available for model files).
        """
        logging.info('Exporting model using dot tool')
        model_export_path = utils.get_path(self.project_path, cfg.JSD_MBRS_GENERATOR_FOLDER, cfg.EXPORT_FOLDER, cfg.EXPORT_DOT_FOLDER)
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
        class_name = model.__class__.__name__
        logging.info(f'Setting variables for class "{class_name}"')
        self.set_package_tree(self, model)
        self.set_build_tool(self, model)
        self.set_database_driver_flag(self, model)
        self.set_project_name(self, model)
        self.set_app_file_name(self, model)
        logging.info(f'Successfully set variables for class "{class_name}"')
        logging.info(f'Starting semantic checks for JSD-MBRS Generator "{class_name}"')
        self.check_unique_class_names(model)
        self.check_entity_relationships(self, model)
        logging.info(f'Successfully finished semantic checks for JSD-MBRS Generator "{class_name}"')

    def database_processor(self, database):
        """
        Perform semantic checks on the database.
        """
        logging.info(f'Starting semantic checks for the database parameters')
        self.check_database_name(database)
        self.check_database_driver(self, database)
        self.check_database_username(database)
        self.check_database_password(database)
        logging.info(f'Successfully finished semantic checks for the database parameters')

    def entity_processor(self, entity):
        """
        Perform semantic checks on each class in the model.
        """
        logging.info(f'Setting variables for class "{entity.name}"')
        self.set_entity_id_property_value(entity)
        self.set_entity_relationships(entity)
        logging.info(f'Successfully set variables for class "{entity.name}"')
        logging.info(f'Starting semantic checks for class "{entity.name}"')
        self.check_class_name(entity)
        self.check_unique_property_names(entity)
        self.check_id_property(entity)
        self.check_empty_and_default_constructor(self, entity)
        self.check_properties_inside_constructors(entity),
        self.check_unique_constructors(self, entity)
        self.check_unique_methods(self, entity)
        logging.info(f'Successfully finished semantic checks for class "{entity.name}"')

    def property_processor(self, property):
        """
        Perform semantic checks on each property in the model.
        """
        logging.info(f'Setting variables for property "{property.name}"')
        self.set_primary_key_flag_to_entity_property(property)
        logging.info(f'Successfully set variables for property "{property.name}"')
        logging.info(f'Starting semantic checks for property "{property.name}"')
        self.check_property_name(property)
        self.check_id_property_value(property)
        self.check_id_property_encapsulation(property)
        self.check_entity_property(property)
        self.check_property_relationship(property)
        self.check_list_type_and_relationship(property)
        self.check_property_type_and_list_type(property)
        self.check_constant_and_value(property)
        self.check_constant_and_encapsulation(property)
        self.check_value_of_constant_property(property)
        self.check_value_of_list_elements(property)
        logging.info(f'Successfully finished semantic checks for property "{property.name}"')
        logging.info(f'Updating property value for property "{property.name}"')
        self.update_property_value(property)
        logging.info(f'Successfully updated property value for property "{property.name}"')

    def constructor_processor(self, constructor):
        """
        Perform semantic checks on each constructor in the model.
        """
        constructor_name = self.get_constructor_name(constructor)
        logging.info(f'Starting semantic checks for "{constructor_name}" constructor')
        self.check_constructor_unique_properties(constructor)
        self.check_constructor_constant_property(constructor)
        logging.info(f'Successfully finished semantic checks for constructor "{constructor_name}"')

    def method_processor(self, method):
        """
        Perform semantic checks on each method in the model.
        """
        logging.info(f'Starting semantic checks for method "{method.name}"')
        self.check_method_name(self, method)
        self.check_method_type_in_list_type(method)
        logging.info(f'Successfully finished semantic checks for method "{method.name}"')

    # MODEL SET FUNCTIONS
    def set_package_tree(self, model):
        """
        Create and add the package tree to the model.
        """
        logging.debug('Finding package tree for JSD-MBRS model')
        java_folder = utils.get_path(self.project_path, cfg.PROJECT_JAVA_FOLDER)
        java_app_file_path = utils.find_java_app_file(java_folder)
        java_app_folder_path = java_app_file_path.parent
        package_tree = utils.get_import_package_tree(java_app_folder_path, cfg.PROJECT_JAVA_FOLDER)
        logging.debug(f'Package tree for JSD-MBRS model: "{package_tree}"')
        model.package_tree = package_tree

    def set_build_tool(self, model):
        """
        Set the build tool to the model.
        """
        logging.debug('Setting build tool for JSD-MBRS model')
        build_tool = utils.detect_build_tool(self.project_path)
        model.build_tool = build_tool
        logging.debug(f'Build tool for JSD-MBRS model: "{build_tool}"')

    def set_database_driver_flag(self, model):
        """
        Set the database driver flag to the model used for indicating if the dependency should be added.
        """
        logging.debug('Setting database driver flag for JSD-MBRS model')
        grammar_database_driver = cfg.DATABASE_MAPPINGS[model.database.driver]['name']
        model.add_database_dependency = False if self.database_driver is not None and self.database_driver == grammar_database_driver else True
        logging.debug(f'Add database driver for JSD-MBRS model: "{model.add_database_dependency}"')

    def set_project_name(self, model):
        """
        Set the project name to the model.
        """
        logging.debug('Setting project name for JSD-MBRS model')
        model.project_name = self.project_path.name
        logging.debug(f'Project name for JSD-MBRS model: "{model.project_name}"')

    def set_app_file_name(self, model):
        """
        Set the app file name to the model.
        """
        logging.debug('Setting app file name for JSD-MBRS model')
        java_folder = utils.get_path(self.project_path, cfg.PROJECT_JAVA_FOLDER)
        java_app_file_path = utils.find_java_app_file(java_folder)
        model.app_file_name = java_app_file_path.stem
        logging.debug(f'App file name for JSD-MBRS model: "{java_app_file_path.name}"')

    # CONSTRUCTOR FUNCTIONS
    def validate_entity_relationships(model, entity, property):
        """
        Validate the relationship between an entity and a property in the given model.
        """
        def validate_relationship_type(first_type, second_type):
            """
            Validate the relationship type between two types.
            """
            logging.debug(f'Validating relationship type "{first_type}" and "{second_type}"')
            is_valid_relationship_type = cfg.VALID_RELATIONSHIP_TYPE_MAPPING[first_type] != second_type
            return is_valid_relationship_type
        
        property_type_name = property.property_type.name
        relationship_owner = property.relationship.owner
        relationship_type = property.relationship.type

        matching_entity = next((e for e in model.entities if e.name == property_type_name), None)
        matching_property = next((p for p in matching_entity.properties if p.property_type.name == entity.name), None)
        if not matching_property:
            error_message = cfg.ENTITY_RELATIONSHIP_PROPERTY_ERROR % (property.property_type.name, entity.name)
            return ValidationResponse(cfg.ERROR, error_message, type=property.property_type, search_value=property_type_name)

        # Check if the relationship owner is correct
        if matching_property.relationship.owner == relationship_owner:
            additional_search = {matching_entity.name: f'{matching_property.name}: {matching_property.property_type.name} {matching_property.relationship.type}'}
            search_value = [property.name, property.property_type.name, property.relationship.type, additional_search]
            error_message = cfg.ENTITY_RELATIONSHIP_OWNER_ERROR % (entity.name, property.property_type.name)
            return ValidationResponse(cfg.ERROR, error_message, type=property, search_value=search_value)
        
        # Check if the relationship types are valid
        if validate_relationship_type(matching_property.relationship.type, relationship_type):
            additional_search = {matching_entity.name: f'{matching_property.name}: {matching_property.property_type.name} {matching_property.relationship.type}'}
            search_value = [property.name, property.property_type.name, property.relationship.type, additional_search]
            error_message = cfg.ENTITY_RELATIONSHIP_TYPE_ERROR % (entity.name, matching_property.relationship.type, property.property_type.name, relationship_type)
            return ValidationResponse(cfg.ERROR, error_message, type=property, search_value=search_value)
        
        logging.debug('Entity relationship is valid')
        return ValidationResponse(cfg.OK)

    # MODEL SEMANTIC CHECKS
    def check_unique_class_names(model):
        """
        Check if class names are unique.
        Raise a SemanticError if a class name is not unique.
        """
        class_names = set()
        for entity in model.entities:
            if entity.name in class_names:
                error_message = cfg.UNIQUE_CLASS_NAMES_ERROR % (entity.name)
                logging.error(error_message)
                raise SemanticError(error_message, **get_location(entity), search_value=entity.name, err_type='unique_class_names_error')
            class_names.add(entity.name)

    def check_entity_relationships(self, model):
        """
        Check if the entity relationships are valid.
        Raise a SemanticError if the entity relationships are invalid.
        """
        for entity in model.entities:
            for property in entity.relationships:
                response = self.validate_entity_relationships(model, entity, property)
                if response.status == cfg.ERROR:
                    error_message = response.message
                    logging.error(error_message)
                    raise SemanticError(error_message, **get_location(response.type), search_value=response.search_value, err_type='entity_relationships_error')

    # DATABASE SEMANTIC CHECKS
    def check_database_name(database):
        """
        Check if the database name is a valid SQL database name.
        Raise a SemanticError if the database name is not valid.
        """
        if not utils.check_value_regex(cfg.SQL_DATABASE_NAME_REGEX, database.name):
            error_message = cfg.DATABASE_NAME_ERROR % (str(database.driver).capitalize(), database.name, cfg.SQL_DATABASE_NAME_ERROR)
            logging.error(error_message)
            raise SemanticError(error_message, **get_location(database), search_value=database.name, err_type='database_name_error')
        
    def check_database_driver(self, database):
        """
        Check if the database driver is a valid SQL database driver.
        Raise a SemanticError if the database driver is not valid.
        """
        grammar_database_driver = cfg.DATABASE_MAPPINGS[database.driver]['name']
        if self.database_driver and grammar_database_driver is not self.database_driver:
            error_message = cfg.DATABASE_DRIVER_ERROR % (self.database_driver, grammar_database_driver)
            logging.error(error_message)
            raise SemanticError(error_message, **get_location(database), search_value=database.driver, err_type='database_driver_error')

    def check_database_username(database):
        """
        Check if the database username (if provided) is a valid SQL database username.
        Raise a SemanticError if the database username is not valid.
        """
        if database.credentials and not utils.check_value_regex(cfg.SQL_DATABASE_USERNAME_REGEX, database.credentials.username):
            error_message = cfg.DATABASE_USERNAME_ERROR % (str(database.driver).capitalize(), database.credentials.username, cfg.SQL_DATABASE_USERNAME_ERROR)
            logging.error(error_message)
            raise SemanticError(error_message, **get_location(database), search_value=database.credentials.username, err_type='database_username_error')
        
    def check_database_password(database):
        """
        Check if the database password (if provided) is a valid SQL database password.
        Raise a SemanticError if the database password is not valid.
        """
        if database.credentials and not utils.check_value_regex(cfg.SQL_DATABASE_PASSWORD_REGEX, database.credentials.password):
            error_message = cfg.DATABASE_PASSWORD_ERROR % (str(database.driver).capitalize(), database.credentials.password, cfg.SQL_DATABASE_PASSWORD_ERROR)
            logging.error(error_message)
            raise SemanticError(error_message, **get_location(database), search_value=database.credentials.password, err_type='database_password_error')
        
    # CLASS SET FUNCTIONS
    def set_entity_id_property_value(entity):
        """
        Set the primary key property value for the entity.
        """
        logging.debug(f'Setting primary key property value for entity "{entity.name}"')
        for property in entity.properties:
            if property.property_type.is_primary_key:
                entity.id_property = property.name
                break

    def set_entity_relationships(entity):
        """
        Set the relationships for the entity.
        """
        logging.debug(f'Setting relationships for entity "{entity.name}"')
        entity_relationships = list()
        for property in entity.properties:
            if property.relationship:
                entity_relationships.append(property)
        entity.relationships = entity_relationships

    # CLASS SEMANTIC CHECKS
    def check_class_name(entity):
        """
        Check if the class name is a valid Java class name.
        Raise a SemanticError if the class name is not valid.
        """
        if not utils.check_value_regex(cfg.JAVA_CLASS_NAME_REGEX, entity.name):
            error_message = cfg.CLASS_NAME_ERROR % (entity.name, cfg.JAVA_CLASS_NAME_ERROR)
            logging.error(error_message)
            raise SemanticError(error_message, **get_location(entity), search_value=entity.name, err_type='class_name_error')
        
    def check_unique_property_names(entity):
        """
        Check if property names are unique within a class.
        Raise a SemanticError if a property name is not unique.
        """
        property_names = set()
        for property in entity.properties:
            if property.name in property_names:
                error_message = cfg.UNIQUE_PROPERTY_NAMES_ERROR % (property.name, entity.name)
                logging.error(error_message)
                raise SemanticError(error_message, **get_location(property), search_value=property.name, err_type='unique_property_names_error')
            property_names.add(property.name)

    def check_id_property(entity):
        """
        Check if the class has a primary key property and if it is unique'.
        Raise a SemanticError if the primary key property is not present or if it is not unique.
        """
        id_type_count = 0
        id_property_list = list()
        for property in entity.properties:
            if property.property_type.is_primary_key:
                id_type_count += 1
                id_property_list.append(property.name)

        if id_type_count == 0:
            error_message = cfg.NO_ID_PROPERTY_ERROR % (entity.name)
            logging.error(error_message)
            raise SemanticError(error_message, **get_location(entity), search_value=entity.name, err_type='no_id_property_error')
        elif id_type_count > 1:
            id_property_names = ', '.join(f'"{item}"' for item in id_property_list)
            error_message = cfg.MULTIPLE_ID_PROPERTIES_ERROR % (entity.name, id_property_names)
            logging.error(error_message)
            raise SemanticError(error_message, **get_location(entity), search_value=id_property_list, err_type='multiple_id_property_error')
        
    def check_empty_and_default_constructor(self, entity):
        """
        Check if the empty and default constructors are provided.
        Raise a SemanticError if the empty and default constructors are not provided.
        """
        empty_constructors = [constructor for constructor in entity.constructors if constructor.empty_constructor]
        default_constructors = [constructor for constructor in entity.constructors if constructor.default_constructor]
        last_constructor = entity.constructors[-1]
        last_constructor_name = self.get_constructor_name(last_constructor)
        if len(empty_constructors) == 0:
            error_message = cfg.EMPTY_CONSTRUCTOR_ERROR % (entity.name)
            logging.error(error_message)
            raise SemanticError(error_message, **get_location(last_constructor), search_value=last_constructor_name, err_type='empty_constructor_error')
        elif len(default_constructors) == 0:
            error_message = cfg.DEFAULT_CONSTRUCTOR_ERROR % (entity.name)
            logging.error(error_message)
            raise SemanticError(error_message, **get_location(last_constructor), search_value=last_constructor_name, err_type='default_constructor_error')
        
    def check_properties_inside_constructors(entity):
        """
        Check if the provided constructor properties are part of specific class.
        Raise a SemanticError if a constructor property is not part of the class.
        """
        for constructor in entity.constructors:
            for property in constructor.property_list:
                if property not in entity.properties:
                    error_message = cfg.CONSTRUCTOR_PROPERTY_ERROR % (property.name, entity.name)
                    logging.error(error_message)
                    raise SemanticError(error_message, **get_location(constructor), search_value=property.name, err_type='constructor_property_error')
        
    def check_unique_constructors(self, entity):
        """
        Check if the constructors are unique within a class.
        Raise a SemanticError if a constructor is not unique.
        """
        constructors = set()
        for constructor in entity.constructors:
            constructor_name = self.get_constructor_name(constructor)
            if constructor_name in constructors:
                error_message = cfg.UNIQUE_CONSTRUCTORS_ERROR % (constructor_name, entity.name)
                logging.error(error_message)
                raise SemanticError(error_message, **get_location(constructor), search_value=constructor_name, err_type='unique_constructors_error')
            constructors.add(constructor_name)

    def check_unique_methods(self, entity):
        """
        Check if the methods are unique within a class by checking method name and property types.
        Raise a SemanticError if a method is not unique.
        """
        methods = set()
        for method in entity.methods:
            method_types_obj = []
            if method.method_properties is None:
                continue
            for property in method.method_properties.property_list:
                if property.__class__.__name__ == 'Entity':
                    type_value = property.name
                elif not property.property_type.__class__.__name__ == 'Entity':
                    type_value = property.property_type.type
                else:
                    type_value = property.property_type.name
                method_types_obj.append(type_value)

            # Sort properties alphabetically by name for consistent comparison
            method_types_obj.sort(key=lambda x: x[0])
            method_types = ', '.join(type for type in method_types_obj)
            method_name = f'{method.name}({method_types})' if method_types else method.name
            if method_name in methods:
                additional_text = f' with property types "({method_types})"' if method_types else ''
                error_message = cfg.UNIQUE_METHODS_ERROR % (method.name, additional_text, entity.name)
                logging.error(error_message)
                raise SemanticError(error_message, **get_location(method), search_value=method.name, err_type='unique_methods_error')
            methods.add(method_name)

    # PROPERTY SET FUNCTIONS
    def set_primary_key_flag_to_entity_property(property):
        """
        Set the primary key flag to the entity property.
        """
        property_type_class = property.property_type.__class__.__name__
        if property_type_class == 'Entity':
            property.property_type.is_primary_key = False
    
    # PROPERTY SEMANTIC CHECKS
    def check_property_name(property):
        """
        Check if the property name is a valid Java variable name.
        Raise a SemanticError if the property name is not valid.
        """
        if not utils.check_value_regex(cfg.JAVA_PROPERTY_AND_METHOD_NAME_REGEX, property.name):
            error_message = cfg.PROPERTY_NAME_ERROR % (property.name, cfg.JAVA_PROPERTY_AND_METHOD_NAME_ERROR)
            logging.error(error_message)
            raise SemanticError(error_message, **get_location(property), search_value=property.name, err_type='property_name_error')
        
        if str(property.name).lower() == 'id':
            error_message = cfg.ID_PROPERTY_NAME_ERROR % (property.name, cfg.JAVA_PROPERTY_AND_METHOD_NAME_ERROR)
            logging.error(error_message)
            raise SemanticError(error_message, **get_location(property), search_value=property.name, err_type='property_name_error')
        
    def check_id_property_value(property):
        """
        Check if the primary key property is declared as constant.
        Raise a SemanticError if the property value is defined or if the constant keyword is specified.
        """
        if property.property_type.is_primary_key and (property.property_value or property.constant):
            search_values = [property.name, 'const', 'constant']
            search_values.extend(property.property_value.value) if property.property_value else None
            error_message = cfg.ID_PROPERTY_VALUE_ERROR % (property.name, property.property_type.type)
            logging.error(error_message)
            raise SemanticError(error_message, **get_location(property), search_value=search_values, err_type='id_property_value_error')
        
    def check_id_property_encapsulation(property):
        """
        Check getter and setter methods for the primary key property.
        Raise a SemanticError if the conditions are not met.
        """
        if property.property_type.is_primary_key:
            if not property.encapsulation or not property.encapsulation.getter:
                error_message = cfg.ID_PROPERTY_GETTER_ENCAPSULATION_ERROR % (property.name, property.property_type.type)
                logging.error(error_message)
                raise SemanticError(error_message, **get_location(property), search_value=property.name, err_type='id_property_encapsulation_error')
            elif property.encapsulation.setter:
                search_values = [property.name, 'set', 'setter']
                error_message = cfg.ID_PROPERTY_SETTER_ENCAPSULATION_ERROR % (property.name, property.property_type.type)
                logging.error(error_message)
                raise SemanticError(error_message, **get_location(property), search_value=search_values, err_type='id_property_encapsulation_error')

    def check_entity_property(property):
        """
        Check if a class property is valid.
        Raise a SemanticError if the conditions are not met.
        """
        property_type_class = property.property_type.__class__.__name__
        if property_type_class == 'Entity':
            if property.constant:
                search_values = [property.name, 'const', 'constant']
                error_message = cfg.ENTITY_PROPERTY_CONSTANT_ERROR % (property.name, property.property_type.name, property_type_class)
                logging.error(error_message)
                raise SemanticError(error_message, **get_location(property), search_value=search_values, err_type='entity_property_error')
            elif property.property_value:
                search_values = [property.name, property.property_value.value]
                error_message = cfg.ENTITY_PROPERTY_VALUE_ERROR % (property.name, property.property_type.name)
                logging.error(error_message)
                raise SemanticError(error_message, **get_location(property), search_value=search_values, err_type='entity_property_error')
            elif not property.relationship:
                error_message = cfg.ENTITY_PROPERTY_RELATIONSHIP_ERROR % (property.name, property.property_type.name)
                logging.error(error_message)
                raise SemanticError(error_message, **get_location(property), search_value=property.name, err_type='entity_property_error')
    
    def check_property_relationship(property):
        """
        Check if the property relationship is valid for the list type and/or class.
        Raise a SemanticError if the relationship is not valid.
        """
        property_type_class = property.property_type.__class__.__name__
        if property.relationship and not property.list_type and property_type_class not in ['ListType', 'Entity']:
            search_values = [property.name, property.relationship.type]
            error_message = cfg.PROPERTY_RELATIONSHIP_ERROR % (property.name)
            logging.error(error_message)
            raise SemanticError(error_message, **get_location(property), search_value=search_values, err_type='property_relationship_error')
        
    def check_list_type_and_relationship(property):
        """
        Check if the list type and property relationship are valid.
        Raise a SemanticError if the conditions are not met.
        """
        property_type_class = property.property_type.__class__.__name__
        if property.list_type and property.relationship and not property_type_class == 'Entity':
            search_values = [property.name, property.list_type.type, property.relationship.type]
            error_message = cfg.LIST_TYPE_AND_RELATIONSHIP_ERROR % (property.name)
            logging.error(error_message)
            raise SemanticError(error_message, **get_location(property), search_value=search_values, err_type='list_type_and_relationship_error')
        
    def check_property_type_and_list_type(property):
        """
        Check if the property type and list type are valid.
        Raise a SemanticError if the conditions are not met.
        """
        property_type_class = property.property_type.__class__.__name__
        if property.list_type and property.list_type.type in [cfg.ARRAY, cfg.LINKED, cfg.HASHMAP, cfg.HASHSET, cfg.TREEMAP] and property_type_class not in ['Entity', 'OtherDataType', 'WrapperDataType']:
            search_values = [property.name, property.property_type.type, property.list_type.type]
            error_message = cfg.PROPERTY_TYPE_AND_LIST_TYPE_ERROR % (property.name, property.property_type.type, property.list_type.type)
            logging.error(error_message)
            raise SemanticError(error_message, **get_location(property), search_value=search_values, err_type='property_type_and_list_type')
    
    def check_constant_and_value(property):
        """
        Check if either const (or constant) keyword or property value is set and the other is not.
        Raise a SemanticError if the condition is met.
        """
        if property.constant ^ bool(property.property_value):  # ^ is the XOR operator
            missing_element = 'constant keyword' if not property.constant else f'constant property {property.property_type.type} value'
            error_message = cfg.CONSTANT_AND_VALUE_ERROR % (missing_element, property.name)
            logging.error(error_message)
            raise SemanticError(error_message, **get_location(property), search_value=property.name, err_type='constant_and_value')
        
    def check_constant_and_encapsulation(property):
        """
        Check if property is constant and has setter encapsulation.
        Raise a SemanticError if the condition is met.
        """
        if property.constant and property.encapsulation and property.encapsulation.setter:
            search_values = [property.name, 'set', 'setter']
            error_message = cfg.CONSTANT_AND_ENCAPSULATION_ERROR % (property.name)
            logging.error(error_message)
            raise SemanticError(error_message, **get_location(property.encapsulation), search_value=search_values, err_type='constant_and_encapsulation_error')

    def check_value_of_constant_property(property):
        """
        Check if the constant value of a property is valid for its type.
        Raise a SemanticError if the value is invalid.
        """
        try:
            # Skip if property is not constant
            if not property.constant:
                return
            
            checking_type = property.list_type.type if property.list_type else property.property_type.type
            value = property.property_value.value.rstrip()
            logging.debug(f'Checking property "{property.name}" with type "{checking_type}" and value "{value}"')
            response = utils.check_property_value(checking_type, value)
            if response is not cfg.OK:
                search_value = [property.name, value]
                error_message = cfg.CONSTANT_PROPERTY_VALUE_ERROR % (value, property.name, checking_type, response)
                logging.error(error_message)
                raise SemanticError(error_message, **get_location(property), search_value=search_value, err_type='property_value_error')
        except SemanticError as e:
            raise
        except Exception as e:
            logging.error(f'Error checking property "{property.name}": {str(e)}')
            raise

    def check_value_of_list_elements(property):
        """
        Check if the each value of a list type property is valid for its type.
        Raise a SemanticError if an element is invalid.
        """
        # Skip if property is not constant or list type is not set
        if not property.constant or not property.list_type:
            return
        
        value = property.property_value.value.rstrip()
        list_type = property.list_type.type
        property_type = property.property_type.type
        logging.debug(f'Checking list elements for property "{property.name}" with type "{property_type}" and value "{value}"')
        elements = value.strip('[]').split(',')
        for element in elements:
            element = element.strip()
            response = utils.check_property_value(property_type, element)
            if response is not cfg.OK:
                search_value = [property.name, element]
                error_message = cfg.LIST_ELEMENTS_ERROR % (element, value, list_type, property.name, property_type, response)
                logging.error(error_message)
                raise SemanticError(error_message, **get_location(property), search_value=search_value, err_type='list_value_error')

    # PROPERTY UPDATE FUNCTIONS
    def update_property_value(property):
        """
        Updates the value of a property based on its type.
        """
        def format_statement(index, value, key_value_pair=False):
            method = 'add' if not key_value_pair else 'put'
            if property_type in [cfg.STR, cfg.STRING, cfg.STRING_C]:
                return f'{method}("{index}", "{value}")' if key_value_pair else f'{method}("{value}")'
            elif property_type in [cfg.CHAR, cfg.CHARACTER_W]:
                return f"{method}(\"{index}\", '{value}')" if key_value_pair else f"{method}('{value}')"
            else:
                return f'{method}("{index}", {value})' if key_value_pair else f'{method}({value})'

        def generate_method_statements(property_type, property_value_list, key_value_pair=False):
            """
            Generates a string of method statements (add or put) for a given property type and property value list.
            """
            logging.debug(f'Generating method statements for property type "{property_type}" and property value list "{property_value_list}"')
            return '; '.join([format_statement(index, value, key_value_pair) for index, value in enumerate(property_value_list)])
        
        def update_property_list_value(mapped_list_type, property_type, property_value, key_value_pair=False):
            """
            Updates the value of a property with a list type.
            """
            logging.debug(f'Updating property list value for property "{property.name}" with mapped list type "{mapped_list_type}" and property type "{property_type}"')
            property_value = str(property_value).replace("'", '"')
            property_value_list = utils.convert_string_to_list(property_value)
            method_statements = generate_method_statements(property_type, property_value_list, key_value_pair)
            if key_value_pair:
                updated_property_value = f'new {mapped_list_type}<String, {property_type.capitalize()}>() {{{{ {method_statements}; }}}}'
            else:
                updated_property_value = f'new {mapped_list_type}<{property_type.capitalize()}>() {{{{ {method_statements}; }}}}'
            return updated_property_value

        def handle_list_type_property(property, property_type, property_value):
            """
            Handles list type properties by updating the property value based on the list type and property type.
            """
            list_type = property.list_type.type
            if list_type == cfg.LIST:
                logging.debug(f'Handling list type property "{property.name}" with list type "{list_type}" and property value "{property_value}"')
                property.property_value.value = property_value.replace('[', '{').replace(']', '}')
            elif list_type in [cfg.ARRAY, cfg.LINKED, cfg.HASHSET,]:
                mapped_list_type = cfg.MAP_JAVA_TYPES[list_type]
                updated_value = update_property_list_value(mapped_list_type, property_type, property_value)
                logging.debug(f'Updating property value for property "{property.name}" with mapped list type "{mapped_list_type}" and updated value "{updated_value}"')
                property.property_value.value = updated_value
            elif list_type in [cfg.HASHMAP, cfg.TREEMAP]:
                mapped_list_type = cfg.MAP_JAVA_TYPES[list_type]
                updated_value = update_property_list_value(mapped_list_type, property_type, property_value, key_value_pair=True)
                logging.debug(f'Updating property value for property "{property.name}" with mapped list type "{mapped_list_type}" and updated value "{updated_value}"')
                property.property_value.value = updated_value

        logging.debug(f'Updating property value for property "{property.name}"')
        if not property.property_value:
            return
        property_type = property.property_type.type
        property_value = str(property.property_value.value)
        list_type_class = property.list_type.__class__.__name__

        if list_type_class == 'ListType':
            handle_list_type_property(property, property_type, property_value)
        elif property_type in [cfg.BOOLEAN, cfg.BOOLEAN_W]:
            property.property_value.value = property_value.lower()

    # CONSTRUCTOR FUNCTIONS
    def get_constructor_name(constructor):
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

    # CONSTRUCTOR SEMANTIC CHECKS
    def check_constructor_unique_properties(constructor):
        """
        Check if a constructor contains properties that are defined more than once.
        Raise a SemanticError if a constructor contains non-unique properties.
        """
        constructor_property_names = set()
        for constructor_property in constructor.property_list:
            if constructor_property.name in constructor_property_names:
                search_value = 'default' if constructor.default_constructor else constructor_property.name
                error_message = cfg.CONSTRUCTOR_UNIQUE_PROPERTIES_ERROR % (constructor_property.name)
                logging.error(error_message)
                raise SemanticError(error_message, **get_location(constructor), search_value=search_value, err_type='constructor_unique_properties_error')
            constructor_property_names.add(constructor_property.name)

    def check_constructor_constant_property(constructor):
        """
        Check if constructor contain constant properties.
        Raise a SemanticError if a constructor contains constant properties.
        """
        for constructor_property in constructor.property_list:
            if constructor_property.constant:
                error_message = cfg.CONSTRUCTOR_CONSTANT_PROPERTY_ERROR % (constructor_property.name)
                logging.error(error_message)
                raise SemanticError(error_message, **get_location(constructor), search_value=constructor_property.name, err_type='constructor_constant_property_error')

    # METHOD SEMANTIC CHECKS
    def check_method_name(self, method):
        """
        Check if the method name is a valid Java method name.
        Raise a SemanticError if the method name is invalid.
        """
        if not utils.check_value_regex(cfg.JAVA_PROPERTY_AND_METHOD_NAME_REGEX, method.name):
            method_properties = ', '.join(property.name for property in method.property_list)
            method_name = f'{method.name}({method_properties})' if method_properties else method.name
            error_message = cfg.METHOD_NAME_ERROR % (method.name, cfg.JAVA_PROPERTY_AND_METHOD_NAME_ERROR)
            logging.error(error_message)
            raise SemanticError(error_message, **get_location(method), search_value=method_name, err_type='method_name_error')

    def check_method_type_in_list_type(method):
        """
        Check if the method type inside the list type is valid.
        Raise a SemanticError if it is not valid.
        """
        method_declaration = method.method_declaration
        is_valid_type = isinstance(method_declaration.method_type, gc.WrapperDataType) or isinstance(method_declaration.method_type, gc.OtherDataType)
        is_entity = type(method_declaration.method_type).__name__ == 'Entity'
        if hasattr(method_declaration, 'list_type') and not (is_valid_type or is_entity):
            search_value = [method_declaration.method_type.type, method_declaration.list_type.type]
            error_message = cfg.METHOD_TYPE_IN_LIST_TYPE_ERROR % (method_declaration.method_type.type, method_declaration.list_type.type)
            logging.error(error_message)
            raise SemanticError(error_message, **get_location(method), search_value=search_value, err_type='method_type_in_list_type_error')
