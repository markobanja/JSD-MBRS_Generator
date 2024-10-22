import logging
import jinja2

import src.config as cfg
import src.utils as utils


class Jinja:
    """
    Class for executing jinja templates and writing grammar elements into the Java files
    """
    def __init__(self):
        """
        Constructor for the Jinja class.
        """
        self.jinja_env = None
        self.project_path = None

    def set_jinja_env(self, jinja_env):
        """
        Set the jinja environment.
        """
        logging.debug(f'Setting jinja environment variable')
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
        Execute the jinja templates for the given model and save the generated files at the given location.
        """
        logging.info('Starting to execute jinja templates')
        utils.folder_exists(cfg.TEMPLATE_FOLDER)
        utils.file_exists(cfg.TEMPLATE_FOLDER, cfg.JAVA_CLASS_TEMPLATE_FILE)
        jinja_env = self.create_jinja_environment(cfg.TEMPLATE_FOLDER)  # Initialize template engine
        self.set_jinja_env(self, jinja_env)
        self.set_project_path(self, project_path)
        for entity in model.entities:
            self.execute_template(self, entity)
        logging.info('Jinja templates executed successfully')

    def create_jinja_environment(template_folder):
        """
        Initialize jinja environment with templates from the specified folder.
        """
        logging.debug(f'Initializing jinja environment with templates from folder "{template_folder}"')
        return jinja2.Environment(loader=jinja2.FileSystemLoader(template_folder), trim_blocks=True, lstrip_blocks=True)

    def execute_template(self, entity):
        """
        Execute Jinja templates for the given entity and save the generated Java files.
        """
        logging.info(f'Starting to execute Jinja templates for entity "{entity.name}"')
        java_folder = utils.get_path(self.project_path, cfg.PROJECT_JAVA_FOLDER)
        java_app_file_path = utils.find_java_app_file(java_folder)
        java_app_folder_path = java_app_file_path.parent
        utils.create_folder(java_app_folder_path, entity.name)
        self.render_template(self, entity, java_app_folder_path, cfg.JAVA_CLASS_TEMPLATE_FILE, cfg.JAVA_FILE_NAME)
        logging.info(f'Jinja templates executed successfully for entity "{entity.name}"')

    def render_template(self, entity, folder_path, template_name, file_name):
        """
        Load the Jinja template for the given entity and save the generated Java file.
        """
        logging.debug(f'Loading jinja template "{template_name}" and rendering it with entity "{entity.name}"')
        template = self.jinja_env.get_template(template_name)
        content = template.render(entity=entity)
        java_file_name = file_name % entity.name
        file_path = utils.get_path(folder_path, entity.name, java_file_name)
        logging.info(f'Writing content to file "{file_path}"')
        utils.write_to_file(file_path, content)