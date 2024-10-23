import logging
import subprocess

import jinja2

import src.config as cfg
import src.grammar_classes as gc
import src.utils as utils


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

    @classmethod
    def execute_templates(self, model, project_path):
        """
        Execute the Jinja templates for the given model and save the generated files at the given location.
        """
        logging.info('Starting to execute Jinja templates')
        utils.folder_exists(cfg.TEMPLATE_FOLDER)
        utils.file_exists(cfg.TEMPLATE_FOLDER, cfg.JAVA_CLASS_TEMPLATE_FILE)
        jinja_env = self.create_jinja_environment(cfg.TEMPLATE_FOLDER)  # Initialize template engine
        self.register_jinja_filters(jinja_env)
        self.set_jinja_env(self, jinja_env)
        self.set_project_path(self, project_path)
        for entity in model.entities:
            self.execute_template(self, model, entity)
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

    def execute_template(self, model, entity):
        """
        Execute Jinja templates for the given entity and save the generated Java files.
        """
        logging.info(f'Starting to execute Jinja templates for entity "{entity.name}"')
        java_folder = utils.get_path(self.project_path, cfg.PROJECT_JAVA_FOLDER)
        java_app_file_path = utils.find_java_app_file(java_folder)
        java_app_folder_path = java_app_file_path.parent
        utils.create_folder(java_app_folder_path, entity.name)
        self.render_template(self, model, entity, java_app_folder_path, cfg.JAVA_CLASS_TEMPLATE_FILE, cfg.JAVA_FILE_NAME)
        logging.info(f'Jinja templates executed successfully for entity "{entity.name}"')

    def render_template(self, model, entity, folder_path, template_name, file_name):
        """
        Load the Jinja template for the given entity and save the generated Java file.
        """
        logging.debug(f'Loading Jinja template "{template_name}" and rendering it with entity "{entity.name}"')
        template = self.jinja_env.get_template(template_name)
        content = template.render(model=model, entity=entity)
        java_file_name = file_name % entity.name
        file_path = utils.get_path(folder_path, entity.name, java_file_name)
        logging.info(f'Writing content to file "{java_file_name}"')
        utils.write_to_file(file_path, content)
        self.format_java_file(folder_path, file_path)

    def format_java_file(folder_path, file_path):
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
        command = f'java -jar {google_format_jar_path} --replace {file_path}'
        subprocess.run(command, shell=True, check=True, cwd=folder_path, capture_output=True, text=True)


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
            'lowercase': self.lowercase,
            'uppercase_first': self.uppercase_first,
            'description': self.description,
            'method_type': self.method_type,
            'method_default_value': self.method_default_value,
            'java_type': self.java_type,
            'map_list_type': self.map_list_type,
            'map_relationship_type': self.map_relationship_type,
            'get_default_value': self.get_default_value,
            'constructor_properties': self.constructor_properties
        }
        self.jinja_env.filters.update(filters)

    def lowercase(self, word):
        """
        Converts the given word to lowercase.
        """
        logging.debug(f'Converting "{word}" to lowercase')
        return str(word).lower()
    
    def uppercase_first(self, word):
        """
        Capitalizes the first letter of the given word leaving the rest.
        """
        logging.debug(f'Capitalizing first letter of "{word}" leaving the rest')
        return str(word[0]).upper() + word[1:]
    
    def description(self, word):
        """
        Returns the description of the given word.
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
                cfg.ID: cfg.STRING.capitalize(),
                cfg.IDENTIFIER: cfg.STRING.capitalize(),
                cfg.UNIQUE_ID: cfg.STRING.capitalize(),
                cfg.KEY: cfg.STRING.capitalize(),
                cfg.PRIMARY_KEY: cfg.STRING.capitalize(),
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
        Maps a list type to the corresponding Java type.
        """
        mapped_list_type = cfg.LIST_TYPE_MAPPING.get(list_type.type, '{}')
        logging.debug(f'Mapping list type "{list_type.type}" to "{mapped_list_type}"')
        return mapped_list_type
    
    def map_method_list_type(self, list_type):
        """
        Maps a method list type to the corresponding Java type.
        """
        mapped_list_type = cfg.METHOD_LIST_TYPE_MAPPING.get(list_type.type, '{}')
        logging.debug(f'Mapping list type "{list_type.type}" to "{mapped_list_type}"')
        return mapped_list_type
    
    def map_method_list_default_value(self, list_type):
        """
        Maps a method list default value to the corresponding Java value.
        """
        mapped_list_type = cfg.METHOD_LIST_DEFAULT_VALUE_MAPPING.get(list_type.type, '{}')
        logging.debug(f'Mapping list type "{list_type.type}" to "{mapped_list_type}"')
        return mapped_list_type

    def map_relationship_type(self, relationship_type):
        """
        Maps a relationship type to the corresponding Java type.
        """
        mapped_relationship_type = cfg.RELATIONSHIP_TYPE_MAPPING.get(relationship_type)
        logging.debug(f'Mapping relationship type "{relationship_type}" to "{mapped_relationship_type}"')
        return mapped_relationship_type
    
    def get_default_value(self, property):
        """
        Returns the default value for a given property.
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
        Returns a list of properties that are eligible for inclusion in a constructor.
        """
        constructor_properties = []
        for property in property_list:
            property_type_obj = property.property_type
            property_type_class = property_type_obj.__class__.__name__
            if not property.constant and property_type_class != 'IDType':
                logging.debug(f'Adding property "{property.name}" to constructor properties')
                constructor_properties.append(property)
        return constructor_properties