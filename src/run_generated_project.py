import logging
import subprocess
import time
import webbrowser

import pygetwindow as gw
import psutil

import src.config as cfg


class Response:
    """
    Class for creating the response object from a functions.
    """
    def __init__(self, status, message):
        """
        Constructor for the Response class.
        """
        self.status = status
        self.message = message


class RunGeneratedProject:
    """
    Class for running the generated project.
    """
    def __init__(self, project_path, build_tool):
        """
        Constructor for the RunGeneratedProject class.
        """
        self.project_path = project_path
        self.build_tool = build_tool
        self.port = 8080

    def is_port_in_use(self):
        """
        Check if the specified port is in use.
        """
        logging.debug(f'Checking if port {self.port} is in use')
        for conn in psutil.net_connections(kind='inet'):
            if conn.laddr.port == self.port:
                logging.debug(f'Port {self.port} is in use')
                return True
        logging.debug(f'Port {self.port} is not in use')
        return False

    def kill_process_using_port(self):
        """
        Kill the process using the specified port.
        """
        logging.debug(f'Killing the process using port {self.port}')
        for proc in psutil.process_iter(['pid', 'name']):
            for conn in proc.connections(kind='inet'):
                if conn.laddr.port == self.port:
                    proc.kill()
                    logging.debug(f'Process using port {self.port} killed')
                    break

    def run_generated_project(self):
        """
        Run the generated project in a new console.
        Returns a Response object with the status and message.
        """
        try:
            logging.info('Starting to run the generated project...')
            if self.is_port_in_use():
                self.kill_process_using_port()
            
            # Open the Swagger UI
            webbrowser.open(cfg.SWAGGER_UI_URL)
            
            build_tool_command = cfg.RUN_COMMAND_MAPPING.get(self.build_tool)
            cmd_command = f'start cmd /k "title {cfg.CMD_RUN_GENERATED_PROJECT_WINDOW_NAME} && {build_tool_command}"'
            process = subprocess.Popen(cmd_command, shell=True, cwd=self.project_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            time.sleep(1)
            # Check if the CMD window is still open
            while gw.getWindowsWithTitle(cfg.CMD_RUN_GENERATED_PROJECT_WINDOW_NAME):
                time.sleep(1)
            
            return_code = process.wait()
            if return_code == 0:
                logging.info('Successfully executed the command.')
                return Response(status=cfg.OK, message='Successfully executed the command.')
            else:
                error_msg = f'Failed to build and start the project. Return code: {return_code}.'
                logging.error(error_msg)
                return Response(status=cfg.ERROR, message=error_msg)
        except Exception as e:
            error_msg = f'Failed to build and start the project: {str(e)}'
            logging.error(error_msg)
            return Response(status=cfg.ERROR, message=error_msg)
