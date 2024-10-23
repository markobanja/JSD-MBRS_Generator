import logging

import src.config as cfg
import src.utils as utils


class Response:
    """
    Class for creating the response object from a functions.
    """
    def __init__(self, status, message=None):
        """
        Constructor for the Response class.
        """
        self.status = status
        self.message = message


class BuildToolDependency:
    """
    Class for checking the dependencies in the build configuration file.
    """
    def __init__(self, project_name, project_path, build_tool):
        """
        Constructor for the BuildToolDependency class.
        """
        self.missing_dependencies = None
        self.build_content = None
        self.project_name = project_name
        self.project_path = project_path
        self.build_tool = build_tool
        self.config_file_name = self.get_config_file_name()
        self.build_config_path = utils.get_path(self.project_path, self.config_file_name)

    def get_config_file_name(self):
        """
        Get the name of the build tool.
        """
        config_file_name = cfg.BUILD_TOOL_FILE_MAPPING.get(self.build_tool, 'Unknown build tool')
        logging.debug(f'Retrieving build tool name: "{config_file_name}"')
        return config_file_name

    def set_missing_dependencies(self, missing_dependencies):
        """
        Set the missing dependencies.
        """
        logging.debug(f'Setting missing dependencies: "{missing_dependencies}"')
        self.missing_dependencies = dict(missing_dependencies)

    def check_dependencies(self) -> Response:
        """
        Check the dependencies in the build configuration file.
        Returns the response object.
        """
        utils.file_exists(self.project_path, self.config_file_name)
        with open(self.build_config_path, 'r') as file:
            self.build_content = file.read()

        file_name = cfg.BUILD_TOOL_FILE_MAPPING[self.build_tool]
        dependencies_to_check = cfg.DEPENDENCIES_TO_CHECK.get(self.build_tool, {})
        missing_dependencies = utils.check_dependencies(self.build_tool, dependencies_to_check, self.build_content)

        # Failed to find the dependencies section in the build.gradle configuration file
        if missing_dependencies is cfg.ERROR:
            message = f'Could not find the dependencies section in the {self.build_tool} "{file_name}" configuration file located in the selected folder "{self.project_name}"'
            return Response(status=cfg.WARNING, message=message)
        
        # There are missing dependencies
        if missing_dependencies:
            self.set_missing_dependencies(missing_dependencies)
            dependency_names_list = list(missing_dependencies.keys())
            dependency_names = f"{', '.join(dependency_names_list[:-1])}, and {dependency_names_list[-1]}" if len(dependency_names_list) > 1 else dependency_names_list[0]
            additional_text = f'Missing {dependency_names} dependencies.' if len(missing_dependencies) > 1 else f'Missing {dependency_names} dependency.'
            message = f'Selected folder "{self.project_name}" is missing mandatory dependencies in the "{file_name}" configuration file. {additional_text}'
            return Response(status=cfg.ERROR, message=message)

        # No missing dependencies
        return Response(status=cfg.OK)

    def add_missing_dependencies(self) -> None:
        """
        Adds the missing dependencies to the build configuration file.
        """
        logging.info('Adding missing dependencies to the build configuration file')
        splitter = '\n\n\t\t' if self.build_tool == cfg.MAVEN else '\n\t'
        dependencies_section = utils.get_dependencies_section(self.build_tool, self.build_content)
        for dependency in self.missing_dependencies.values():
            self.build_content = self.build_content.replace(dependencies_section, f"{dependencies_section}{splitter}{dependency}")

        # Write back the updated content to build.gradle
        with open(self.build_config_path, 'w') as file:
            file.write(self.build_content)