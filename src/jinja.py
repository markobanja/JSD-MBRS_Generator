import logging
import subprocess

import jinja2

import src.config as cfg
import src.grammar_classes as gc
import src.utils as utils
from src.build_tool_dependency import BuildToolDependency


class Jinja:
    """
    Class for executing Jinja templates and writing grammar elements into the Java files
    """
    def __init__(self):
        """
        Constructor for the Jinja class.
        """
        self.jinja_env = None
        self.project_path = None
        self.java_app_folder_path = None
        self.java_app_file_path = None

    def set_jinja_env(self, jinja_env):
        """
        Set the Jinja environment.
        """
        logging.debug(f'Setting Jinja environment variable')
        self.jinja_env = jinja_env

    def set_project_path(self, project_path):
        """
        Set the project path.
        """
        logging.debug(f'Setting project path variable to "{project_path}"')
        self.project_path = project_path

    def set_java_app_file_path(self, java_app_file_path):
        """
        Set the Java app file path.
        """
        logging.debug('Setting Java app file path')
        self.java_app_file_path = java_app_file_path

    def set_java_app_folder_path(self):
        """
        Set the Java app folder path.
        """
        logging.debug('Setting Java app folder path')
        java_folder = utils.get_path(self.project_path, cfg.PROJECT_JAVA_FOLDER)
        java_app_file_path = utils.find_java_app_file(java_folder)
        self.set_java_app_file_path(self, java_app_file_path)
        self.java_app_folder_path = java_app_file_path.parent

    @classmethod
    def generate(self, model, project_path):
        """
        Generate the grammar elements from the given model and project path.
        Save the generated Java files in the specified folder.
        """
        logging.info('Starting to execute Jinja templates')
        utils.folder_exists(cfg.TEMPLATE_FOLDER)
        utils.file_exists(cfg.TEMPLATE_FOLDER, cfg.JAVA_CLASS_TEMPLATE_FILE)
        jinja_env = self.create_jinja_environment(cfg.TEMPLATE_FOLDER)  # Initialize template engine
        self.register_jinja_filters(jinja_env)
        self.set_jinja_env(self, jinja_env)
        self.set_project_path(self, project_path)
        self.set_java_app_folder_path(self)

        # Add database dependency and render template for application.properties file
        if model.add_database_dependency:
            self.add_database_dependency(self, model)

        # Render template for each entity
        for entity in model.entities:
            self.execute_templates(self, model, entity)
        
        # Render template for repository configuration
        self.render_template(self, model, entity, self.java_app_folder_path, cfg.JAVA_REPOSITORY_CONFIGURATION_TEMPLATE_FILE, cfg.JAVA_REPOSITORY_CONFIGURATION_FILE_NAME)
        
        # Render template for Application
        if utils.check_app_file_content(self.java_app_file_path):
            self.render_template(self, model, entity, self.java_app_folder_path, cfg.JAVA_APPLICATION_TEMPLATE_FILE, cfg.JAVA_APPLICATION_FILE_NAME)
        logging.info('Jinja templates executed successfully')

    def create_jinja_environment(template_folder):
        """
        Initialize Jinja environment with templates from the specified folder.
        """
        logging.debug(f'Initializing Jinja environment with templates from folder "{template_folder}"')
        return jinja2.Environment(loader=jinja2.FileSystemLoader(template_folder), trim_blocks=True, lstrip_blocks=True)
    
    def register_jinja_filters(jinja_env):
        """
        Register Jinja filters.
        """
        logging.debug('Registering Jinja filters')
        JinjaFilters(jinja_env)
        logging.debug('Jinja filters registered successfully')

    def add_database_dependency(self, model):
        """
        Add database dependency to the project.
        """
        logging.info('Adding database dependency to the project')
        project_name = utils.get_base_name(self.project_path)
        build_tool_dependency = BuildToolDependency(project_name, self.project_path, model.build_tool, model.database)
        build_tool_dependency.add_driver_dependency()
        resources_path = utils.get_path(self.project_path, cfg.PROJECT_RESOURCES_FOLDER)
        utils.folder_exists(resources_path)
        self.render_template(self, model, None, resources_path, cfg.APPLICATION_PROPERTIES_TEMPLATE_FILE, cfg.APPLICATION_PROPERTIES_FILE_NAME)

    def execute_templates(self, model, entity):
        """
        Execute Jinja templates for the given entity and save the generated Java files.
        """
        logging.info(f'Starting to execute Jinja templates for entity "{entity.name}"')
        utils.create_folder(self.java_app_folder_path, entity.name)
        self.execute_template(self, model, entity, self.java_app_folder_path)
        logging.info(f'Jinja templates executed successfully for entity "{entity.name}"')

    def execute_template(self, model, entity, folder_path):
        """
        Execute the Jinja template for the given entity and save the generated Java file in the specified folder.
        """
        logging.debug(f'Executing Jinja template for entity "{entity.name}"')
        self.render_template(self, model, entity, folder_path, cfg.JAVA_CLASS_TEMPLATE_FILE, cfg.JAVA_CLASS_FILE_NAME)
        self.render_template(self, model, entity, folder_path, cfg.JAVA_CONTROLLER_TEMPLATE_FILE, cfg.JAVA_CONTROLLER_FILE_NAME)
        self.render_template(self, model, entity, folder_path, cfg.JAVA_SERVICE_TEMPLATE_FILE, cfg.JAVA_SERVICE_FILE_NAME)
        self.render_template(self, model, entity, folder_path, cfg.JAVA_REPOSITORY_TEMPLATE_FILE, cfg.JAVA_REPOSITORY_FILE_NAME)

    def render_template(self, model, entity, folder_path, template_name, file_name):
        """
        Load the Jinja template for the given entity and save the generated Java file.
        """
        logging.debug(f'Loading Jinja template "{template_name}"')
        template = self.jinja_env.get_template(template_name)
        content = template.render(model=model, entity=entity)
        file_path = self.get_render_file_path(entity, folder_path, file_name)
        logging.info(f'Writing content to file "{file_path.name}"')
        utils.write_to_file(file_path, content)
        self.format_java_file(folder_path, file_path)

    def get_render_file_path(entity, folder_path, file_name):
        """
        Get the path to the rendered Java file.
        """
        java_file_name = file_name
        if 'Application' in file_name:
            java_file_name = file_name % entity.parent.build_tool
        elif '%s' in file_name:
            java_file_name = file_name % entity.name
            folder_path = utils.get_path(folder_path, entity.name)
        file_path = utils.get_path(folder_path, java_file_name)
        return file_path

    def format_java_file(folder_path, file_path):
        """
        Format the Java file using Google Java Format.
        """
        try:
            logging.debug(f'Formatting file "{file_path}" using Google Java Format')
            utils.folder_exists(cfg.RESOURCES_FOLDER)

            # Find the Google Java Format jar file in the resources folder
            google_format_file_name = utils.find_specific_file_regex(cfg.RESOURCES_FOLDER, cfg.GOOGLE_FORMAT_REGEX)
            if not google_format_file_name:
                logging.warning(f'No Google Java Format jar file found in the "{cfg.RESOURCES_FOLDER}" folder')
                return
            elif len(google_format_file_name) > 1:
                logging.warning(f'More than one Google Java Format jar file found in the "{cfg.RESOURCES_FOLDER}" folder. Using the newest one: {google_format_file_name[0]}')

            current_directory = utils.get_current_path()
            google_format_jar_path = utils.get_path(current_directory, cfg.RESOURCES_FOLDER, google_format_file_name[0])
            command = f'java -jar {google_format_jar_path} --skip-reflowing-long-strings --skip-javadoc-formatting --aosp --replace {file_path}'
            subprocess.run(command, shell=True, check=True, cwd=folder_path, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            error_message = str(e.stderr).replace('\n', '. ').rstrip('. ')
            logging.error(f'Failed to format file "{file_path}" using Google Java Format: {error_message}')
            raise
        except Exception as e:
            raise
        

class JinjaFilters:
    """
    Class for handling Jinja filters
    """
    def __init__(self, jinja_env):
        """
        Constructor for the JinjaFilters class.
        """
        self.jinja_env = jinja_env
        filters = {
            'constructor_properties': self.constructor_properties,
            'default_constructor_properties': self.default_constructor_properties,
            'description': self.description,
            'dialect': self.dialect,
            'driver': self.driver,
            'generated_objects_names': self.generated_objects_names,
            'get_default_value': self.get_default_value,
            'java_type': self.java_type,
            'url': self.url,
            'lowercase': self.lowercase,
            'map_list_type': self.map_list_type,
            'map_relationship_type': self.map_relationship_type,
            'method_default_value': self.method_default_value,
            'method_type': self.method_type,
            'plural_capitalize': self.plural_capitalize,
            'plural_lowercase': self.plural_lowercase,
            'repository_configuration_value': self.repository_configuration_value,
            'uppercase_first': self.uppercase_first,
        }
        self.jinja_env.filters.update(filters)

    def lowercase(self, word):
        """
        Convert the given word to lowercase.
        """
        logging.debug(f'Converting "{word}" to lowercase')
        return str(word).lower()
    
    def plural_lowercase(self, word):
        """
        Pluralize the given word and convert it to lowercase.
        """
        logging.debug(f'Pluralize "{word}" and convert it to lowercase')
        return utils.pluralize_word(word, lowercase=True)
    
    def plural_capitalize(self, word):
        """
        Pluralize the given word and capitalize it.
        """
        logging.debug(f'Pluralize "{word}" and capitalize it')
        return utils.pluralize_word(word)
    
    def uppercase_first(self, word):
        """
        Capitalize the first letter of the given word leaving the rest.
        """
        logging.debug(f'Capitalizing first letter of "{word}" leaving the rest')
        return f'{str(word[0]).upper()}{word[1:]}'
    
    def url(self, database_name):
        """
        Get the url.
        """
        logging.debug(f'Getting url')
        url = cfg.DATABASE_MAPPINGS[database_name]['url']
        logging.debug(f'url: {url}')
        return url
    
    def driver(self, database_name):
        """
        Get the driver.
        """
        logging.debug(f'Getting driver')
        driver = cfg.DATABASE_MAPPINGS[database_name]['driver']
        logging.debug(f'Driver: {driver}')
        return driver
    
    def dialect(self, database_name):
        """
        Get the dialect.
        """
        logging.debug(f'Getting dialect')
        dialect = cfg.DATABASE_MAPPINGS[database_name]['dialect']
        logging.debug(f'Dialect: {dialect}')
        return dialect
    
    def default_constructor_properties(self, constructors):
        """
        Get the default constructor properties.
        """
        logging.debug(f'Getting default constructor properties')
        for constructor in constructors:
            if not constructor.default_constructor:
                continue
            constructor_properties = []
            for property in constructor.property_list:
                if not property.constant and property.property_type.__class__.__name__ != 'IDType':
                    constructor_properties.append(property)
            return constructor_properties
            
    def generated_objects_names(self, entity_name):
        """
        Get the generated objects names.
        """
        logging.debug(f'Getting generated objects names')
        return ', '.join([f'{entity_name}_{i}' for i in range(1, 4)])
    
    def repository_configuration_value(self, property):
        """
        Get the repository configuration value.
        """
        logging.debug(f'Getting repository configuration value for property "{property.name}"')
        list_type = property.list_type
        property_type = property.property_type
        if isinstance(list_type, gc.ListType):
            java_list_type = self.map_repository_configuration_list_type(list_type)
            java_method_type = self.java_type(property_type)
            list_type = java_list_type.format(java_method_type)
            return list_type
        elif type(property_type).__name__ == 'Entity':
            return 'null'
        elif property_type.type in [cfg.BYTE, cfg.BYTE_W, cfg.SHORT, cfg.SHORT_W]:
            return f'({str(property_type.type).lower()}) {property_type.default_value}'
        return property_type.default_value
    
    def description(self, word):
        """
        Return the description of the given word.
        """
        prefix = 'An' if word[0] in cfg.VOWELS else 'A'
        description = f'{prefix} {word} entity'
        logging.debug(f'Returning description "{description}"')
        return description
    
    def method_type(self, method):
        """
        Convert the given method type to Java type.
        """
        method_declaration = method.method_declaration
        method_type = method_declaration.method_type
        logging.debug(f'Converting method type "{method_type}" to Java type')
        if isinstance(method_type, gc.IDType):
            return 'UUID'
        if type(method_declaration).__name__ == 'ListMethodType':
            java_list_type = self.map_method_list_type(method_declaration.list_type)
            java_method_type = self.java_type(method_declaration)
            list_type = java_list_type.format(java_method_type)
            return list_type
        if type(method_type).__name__ == 'Entity':
            return method_type.name
        return self.java_type(method_type)
        
    def method_default_value(self, method):
        """
        Return the default value of the given method.
        """
        method_declaration = method.method_declaration
        method_type = method_declaration.method_type
        logging.debug(f'Returning default value for method "{method_type}"')
        if type(method_declaration).__name__ == 'ListMethodType':
            java_list_type = self.map_method_list_default_value(method_declaration.list_type)
            java_method_type = self.java_type(method_declaration)
            list_type = java_list_type.format(java_method_type)
            return list_type
        if type(method_type).__name__ == 'Entity':
            return f'new {method_type.name}()'
        return method_type.default_value
    
    def java_type(self, type_object):
        """
        Convert the given type from provided object to Java type.
        """
        logging.debug(f'Converting data type "{type_object}" to Java type')
        if type_object == 'void': return type_object

        if isinstance(type_object, gc.IDType):
            return {
                cfg.ID: cfg.LONG.capitalize(),
                cfg.IDENTIFIER: cfg.LONG.capitalize(),
                cfg.UNIQUE_ID: cfg.LONG.capitalize(),
                cfg.KEY: cfg.LONG.capitalize(),
                cfg.PRIMARY_KEY: cfg.LONG.capitalize(),
            }.get(type_object.type, type_object.type)
        
        elif isinstance(type_object, gc.OtherDataType):
            return {
                cfg.STR: cfg.STRING.capitalize(),
                cfg.STRING: cfg.STRING.capitalize(),
                cfg.STRING_C: cfg.STRING.capitalize(),
            }.get(type_object.type, type_object.type)
        
        elif isinstance(type_object, gc.DateType):
            return {
                cfg.DATE: cfg.MAP_JAVA_TYPES[cfg.DATE],
                cfg.TIME: cfg.MAP_JAVA_TYPES[cfg.TIME],
                cfg.DATETIME: cfg.MAP_JAVA_TYPES[cfg.DATETIME],
            }.get(type_object.type, type_object.type)
        
        elif isinstance(type_object, gc.ListType):
            return {
                cfg.ARRAY: cfg.MAP_JAVA_TYPES[cfg.ARRAY],
                cfg.LINKED: cfg.MAP_JAVA_TYPES[cfg.LINKED],
                cfg.HASHMAP: cfg.MAP_JAVA_TYPES[cfg.HASHMAP],
                cfg.HASHSET: cfg.MAP_JAVA_TYPES[cfg.HASHSET],
                cfg.TREEMAP: cfg.MAP_JAVA_TYPES[cfg.TREEMAP],
                cfg.LIST: cfg.LIST.capitalize(),
            }.get(type_object.type, type_object.type)
        
        elif type(type_object).__name__ == 'Entity':
            return {}.get(type_object.name, type_object.name)
        
        elif type(type_object).__name__ == 'ListMethodType':
            if type(type_object.method_type).__name__ == 'Entity':
                return {}.get(type_object.method_type.name, type_object.method_type.name)
            return {
                cfg.BYTE: cfg.BYTE_W,
                cfg.SHORT: cfg.SHORT_W,
                cfg.CHAR: cfg.CHARACTER_W,
                cfg.INT: cfg.INTEGER_W,
                cfg.FLOAT: cfg.FLOAT_W,
                cfg.LONG: cfg.LONG_W,
                cfg.DOUBLE: cfg.DOUBLE_W,
                cfg.BOOLEAN: cfg.BOOLEAN_W,
                cfg.STR: cfg.STRING.capitalize(),
                cfg.STRING: cfg.STRING.capitalize(),
                cfg.STRING_C: cfg.STRING.capitalize(),
            }.get(type_object.method_type.type, type_object.method_type.type)
        
        else:
            return {}.get(type_object.type, type_object.type)

    def map_list_type(self, list_type):
        """
        Map a list type to the corresponding Java type.
        """
        mapped_list_type = cfg.LIST_TYPE_MAPPING.get(list_type.type, '{}')
        logging.debug(f'Mapping list type "{list_type.type}" to "{mapped_list_type}"')
        return mapped_list_type
    
    def map_method_list_type(self, list_type):
        """
        Map a method list type to the corresponding Java type.
        """
        mapped_list_type = cfg.METHOD_LIST_TYPE_MAPPING.get(list_type.type, '{}')
        logging.debug(f'Mapping list type "{list_type.type}" to "{mapped_list_type}"')
        return mapped_list_type
    
    def map_method_list_default_value(self, list_type):
        """
        Map a method list default value to the corresponding Java value.
        """
        mapped_list_type = cfg.METHOD_LIST_DEFAULT_VALUE_MAPPING.get(list_type.type, '{}')
        logging.debug(f'Mapping list type "{list_type.type}" to "{mapped_list_type}"')
        return mapped_list_type
    
    def map_repository_configuration_list_type(self, list_type):
        """
        Map a repository configuration list type to the corresponding Java type.
        """
        mapped_list_type = cfg.REPOSITORY_CONFIGURATION_LIST_TYPE_MAPPING.get(list_type.type, '{}')
        logging.debug(f'Mapping list type "{list_type.type}" to "{mapped_list_type}"')
        return mapped_list_type

    def map_relationship_type(self, relationship_type):
        """
        Map a relationship type to the corresponding Java type.
        """
        mapped_relationship_type = cfg.RELATIONSHIP_TYPE_MAPPING.get(relationship_type)
        logging.debug(f'Mapping relationship type "{relationship_type}" to "{mapped_relationship_type}"')
        return mapped_relationship_type
    
    def get_default_value(self, property):
        """
        Return the default value for a given property.
        """
        logging.debug(f'Getting default value for property "{property.name}"')
        property_type = property.property_type
        list_type = property.list_type
        property_type_class = property_type.__class__.__name__
        list_type_class = list_type.__class__.__name__

        if property_type_class == 'Entity':
            if list_type_class == 'ListType':
                default_value = str(list_type.default_value)
                if list_type.type == 'list':
                    default_value = 'new {}[0]'  # Change the default value to an empty list for Entities
                return str(default_value).format(property_type.name)
            return f'new {property_type.name}()'

        if list_type_class == 'ListType':
            default_value = str(list_type.default_value)
            return default_value if list_type.type == 'list' else default_value.format(property_type.type)

        return property_type.default_value

    def constructor_properties(self, property_list):
        """
        Return a list of properties that are eligible for inclusion in a constructor.
        """
        constructor_properties = []
        for property in property_list:
            property_type_obj = property.property_type
            property_type_class = property_type_obj.__class__.__name__
            if not property.constant and property_type_class != 'IDType':
                logging.debug(f'Adding property "{property.name}" to constructor properties')
                constructor_properties.append(property)
        return constructor_properties