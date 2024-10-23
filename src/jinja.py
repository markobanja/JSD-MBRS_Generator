import logging

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
        jinja_env.filters['lowercase'] = JinjaFilters.lowercase
        jinja_env.filters['uppercase_first'] = JinjaFilters.uppercase_first
        jinja_env.filters['java_type'] = JinjaFilters.java_type
        jinja_env.filters['map_list_type'] = JinjaFilters.map_list_type
        jinja_env.filters['map_relationship_type'] = JinjaFilters.map_relationship_type
        jinja_env.filters['get_default_value'] = JinjaFilters.get_default_value
        jinja_env.filters['constructor_properties'] = JinjaFilters.constructor_properties
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


class JinjaFilters:
    """
    Class for handling Jinja filters
    """
    def lowercase(word):
        """
        Converts the given word to lowercase.
        """
        logging.debug(f'Converting "{word}" to lowercase')
        return str(word).lower()
    
    def uppercase_first(word):
        """
        Capitalizes the first letter of the given word leaving the rest.
        """
        logging.debug(f'Capitalizing first letter of "{word}" leaving the rest')
        return str(word[0]).upper() + word[1:]
    
    def java_type(property_type):
        """
        Convert the given property type to Java type.
        """
        logging.debug(f'Converting data type "{property_type}" to Java type')
        if property_type == 'void': return property_type

        if isinstance(property_type, gc.IDType):
            return {
                cfg.ID: cfg.STRING.capitalize(),
                cfg.IDENTIFIER: cfg.STRING.capitalize(),
                cfg.UNIQUE_ID: cfg.STRING.capitalize(),
                cfg.KEY: cfg.STRING.capitalize(),
                cfg.PRIMARY_KEY: cfg.STRING.capitalize(),
            }.get(property_type.type, property_type.type)
        
        elif isinstance(property_type, gc.OtherDataType):
            return {
                cfg.STRING: cfg.STRING.capitalize(),
            }.get(property_type.type, property_type.type)
        
        elif isinstance(property_type, gc.DateType):
            return {
                cfg.DATE: cfg.MAP_JAVA_TYPES[cfg.DATE],
                cfg.TIME: cfg.MAP_JAVA_TYPES[cfg.TIME],
                cfg.DATETIME: cfg.MAP_JAVA_TYPES[cfg.DATETIME],
            }.get(property_type.type, property_type.type)
        
        elif isinstance(property_type, gc.ListType):
            return {
                cfg.ARRAY: cfg.MAP_JAVA_TYPES[cfg.ARRAY],
                cfg.LINKED: cfg.MAP_JAVA_TYPES[cfg.LINKED],
                cfg.HASHMAP: cfg.MAP_JAVA_TYPES[cfg.HASHMAP],
                cfg.HASHSET: cfg.MAP_JAVA_TYPES[cfg.HASHSET],
                cfg.TREEMAP: cfg.MAP_JAVA_TYPES[cfg.TREEMAP],
                cfg.LIST: cfg.LIST.capitalize(),
            }.get(property_type.type, property_type.type)
        
        elif type(property_type).__name__ == 'Entity':
            return {}.get(property_type.name, property_type.name)
        
        else:
            return {}.get(property_type.type, property_type.type)

    def map_list_type(list_type):
        """
        Maps a list type to the corresponding Java type.
        """
        list_type_mapping = {
            'list': '{}[]',
            'array': 'List<{}>',
            'linked': 'List<{}>',
            'hashmap': 'Map<String, {}>',
            'hashset': 'Set<{}>',
            'treemap': 'Map<String, {}>'
        }
        mapped_list_type = list_type_mapping.get(list_type.type, '{}')
        logging.debug(f'Mapping list type "{list_type.type}" to "{mapped_list_type}"')
        return mapped_list_type
    
    def map_relationship_type(relationship_type):
        """
        Maps a relationship type to the corresponding Java type.
        """
        relationship_type_mapping = {
            '1-1': '@OneToOne',
            '1-n': '@OneToMany',
            'n-1': '@ManyToOne',
            'n-n': '@ManyToMany',
        }
        mapped_relationship_type = relationship_type_mapping.get(relationship_type)
        logging.debug(f'Mapping relationship type "{relationship_type}" to "{mapped_relationship_type}"')
        return mapped_relationship_type
    
    def get_default_value(property):
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
                return str(list_type.default_value).format(property_type.name)
            return f'new {property_type.name}()'

        if list_type_class == 'ListType':
            default_value = str(list_type.default_value)
            return default_value if list_type.type == 'list' else default_value.format(property_type.type)

        return property_type.default_value

    def constructor_properties(property_list):
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