import logging
import threading

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from ttkthemes import ThemedStyle

import src.config as cfg
import src.utils as utils
from src.build_tool_dependency import BuildToolDependency
from src.run_generated_project import RunGeneratedProject
from src.textx_grammar import TextXGrammar


INITIAL_BACKGROUND_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['initial_background'])
WORKING_BACKGROUND_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['working_background'])
BLACK_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['black'])
OK_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['ok'])
INFORMATION_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['information'])
WARNING_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['warning'])
ERROR_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['error'])
DEFAULT_FONT_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['default_font'])
RULE_DEFINED_SIGNS_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['rule_defined_signs'])
RULE_DEFINED_WORDS_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['rule_defined'])
GRAMMAR_DEFINED_WORDS_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['grammar_defined'])
TYPE_DEFINED_WORDS_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['type_defined'])
WRAPPER_TYPE_DEFINED_WORDS_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['wrapper_type_defined'])
KEYWORD_DEFINED_WORDS_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['keyword_defined'])
ENCAPSULATION_DEFINED_WORDS_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['encapsulation_defined'])
CLASS_NAME_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['class_name'])
COMMENT_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['comment'])
PROPERTY_VALUE_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['property_value'])


def position_window(window, width, height):
    """
    Computes the geometry string for positioning a window at the center of the screen.
    """
    logging.info(f'Positioning "{window.title()}" window')
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_position = (screen_width - width) // 2
    y_position = (screen_height - height) // 2
    window_geometry = f'{width}x{height}+{x_position}+{y_position}'
    return window_geometry

def config_style(window, font):
    """
    Configures the style of the main window.
    """
    logging.info(f'Configuring "{window.title()}" window style')
    style = ThemedStyle(window)
    style.set_theme(cfg.THEME_STYLE)
    style.configure('Toolbar.TButton', font=font)


class MainWindowGUI:
    """
    Class for creating the JSD-MBRS Generator application main window.
    """
    def __init__(self):
        """
        Constructor for the MainWindowGUI class.
        """
        logging.info('Creating MainWindowGUI instance')
        self.init_variables()
        self.init_window()

    def init_variables(self):
        """
        Initialize the variables used in the main window.
        """
        logging.debug('Initializing main window variables')
        self.save_window_instance = None  # To track the instance of the save window
        self.help_window_instance = None  # To track the instance of the help window
        self.project_path = None
        self.project_name = None
        self.build_tool = None
        self.grammar_file_name = None
        self.grammar_file_content = None
        self.database_driver = None
        self.busy = False
        self.save_event = threading.Event()  # Event for synchronization
        self.symbol_index = 0
        self.periodic_update_interval = 3000  # 3 seconds
        self.color_mappings = [
            (cfg.RULE_DEFINED_WORDS, RULE_DEFINED_WORDS_COLOR),
            (cfg.GRAMMAR_DEFINED_WORDS, GRAMMAR_DEFINED_WORDS_COLOR),
            (cfg.TYPE_DEFINED_WORDS, TYPE_DEFINED_WORDS_COLOR),
            (cfg.WRAPPER_TYPE_DEFINED_WORDS, WRAPPER_TYPE_DEFINED_WORDS_COLOR),
            (cfg.KEYWORD_DEFINED_WORDS, KEYWORD_DEFINED_WORDS_COLOR),
            (cfg.ENCAPSULATION_DEFINED_WORDS, ENCAPSULATION_DEFINED_WORDS_COLOR),
        ]

    def init_window(self):
        """
        Initialize the main window.
        """
        logging.info('Initializing main window')
        self.window = tk.Tk()
        self.window.title(cfg.MAIN_WINDOW_TITLE)
        self.window.resizable(False, False)
        self.window.protocol('WM_DELETE_WINDOW', self.on_window_close)
        self.default_font = utils.set_font(cfg.FONT, 11, True)
        self.window.geometry(position_window(self.window, cfg.MAIN_WINDOW_WIDTH, cfg.MAIN_WINDOW_HEIGHT))
        self.window.after(1, lambda: config_style(self.window, self.default_font))
        self.init_window_components()
        self.init_window_binds()
        self.initial_state()
        
    def init_window_components(self):
        """
        Initializes the components of the main window.
        """
        logging.info('Initializing main window components')
        self.init_toolbar()
        self.init_console_frame()
        self.init_line_number_text()
        self.init_text_editor()
        self.init_canvas_circle()
        self.set_window_weights()

    def init_window_binds(self):
        """
        Initialize the binds for the main window.
        """
        self.window.bind('<ButtonRelease-1>', self.on_mouse_click)
        self.window.bind('<MouseWheel>', self.on_scroll)
        self.window.bind('<B1-Motion>', self.on_scroll)

    def init_toolbar(self):
        """
        Initialize the toolbar with a generate button.
        """
        toolbar = ttk.Frame(self.window)
        self.open_button = ttk.Button(toolbar, text='Open Project', command=self.open_project_action, compound=tk.TOP, style='Toolbar.TButton')
        self.save_button = ttk.Button(toolbar, text='Save Grammar', command=self.save_grammar_action, compound=tk.TOP, style='Toolbar.TButton', state=tk.DISABLED)
        self.generate_button = ttk.Button(toolbar, text='Generate', command=self.generate_action, compound=tk.TOP, style='Toolbar.TButton', state=tk.DISABLED)
        self.export_button = ttk.Button(toolbar, text='Export', command=self.export_action, compound=tk.TOP, style='Toolbar.TButton', state=tk.DISABLED)
        self.help_button = ttk.Button(toolbar, text='Help', command=self.help_action, compound=tk.TOP, style='Toolbar.TButton')

        # Pack the buttons in the toolbar
        self.open_button.pack(side=tk.LEFT, padx=5)
        self.save_button.pack(side=tk.LEFT, padx=5)
        self.generate_button.pack(side=tk.LEFT, padx=5)
        self.export_button.pack(side=tk.LEFT, padx=5)
        self.help_button.pack(side=tk.RIGHT, padx=5)

        # Configure the toolbar
        toolbar.pack(fill=tk.X)
        logging.info('Toolbar initialized')

    def init_console_frame(self):
        """
        Initialize the console frame and its label component.
        """
        console_frame = ttk.Frame(self.window, borderwidth=2, relief='groove')
        console_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False, padx=10, pady=5)
        self.console_output = tk.Label(console_frame, text=cfg.HELP_BUTTON_TEXT, font=self.default_font, height=2, wraplength=650, fg=INFORMATION_COLOR)
        self.console_output.pack(padx=10, pady=10, ipady=20, fill=tk.BOTH, expand=False)
        logging.info('Console frame initialized')

    def init_line_number_text(self):
        """
        Initialize line number text widget.
        """
        self.line_number_text = tk.Text(self.window, font=self.default_font, width=5, padx=5, wrap=tk.NONE, state=tk.DISABLED, cursor='arrow', background=INITIAL_BACKGROUND_COLOR)
        self.line_number_text.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.Y)
        self.line_number_text.bind('<Key>', lambda event: 'break')
        self.line_number_text.bind('<MouseWheel>', lambda event: 'break')
        self.line_number_text.bind('<B1-Motion>', lambda event: ('break', self.line_number_text.event_generate('<ButtonRelease-1>')))
        self.line_number_text.tag_configure('right_align', justify='right')
        logging.info('Line number text widget initialized')

    def init_text_editor(self):
        """
        Initialize the text editor widget.
        """
        self.text_editor = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, font=self.default_font, height=30, width=80, undo=True, maxundo=-1, cursor='arrow', background=INITIAL_BACKGROUND_COLOR)
        self.text_editor.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=False)
        self.text_editor.after(self.periodic_update_interval, self.periodic_update)
        self.text_editor.bind('<KeyPress>', self.on_scroll)
        self.text_editor.bind('<MouseWheel>', self.on_scroll)
        self.text_editor.bind('<B1-Motion>', self.on_scroll)
        self.text_editor.bind('<KeyRelease>', self.on_type_text)
        self.text_editor.bind('<Control-s>', self.on_save)
        self.text_editor.bind('<Control-v>', self.on_paste)
        self.text_editor.bind('<Control-l>', self.on_remove_line)
        self.text_editor.bind('<Tab>', self.on_tab)
        logging.info('Text editor widget initialized')

    def init_canvas_circle(self):
        """
        Initialize the canvas circle widget.
        """
        self.circle_canvas = tk.Canvas(self.text_editor, width=10, height=10)
        self.circle = self.circle_canvas.create_oval(2, 2, 10, 10, outline=BLACK_COLOR, fill=OK_COLOR)
        self.circle_canvas.place(relx=1, rely=1, anchor=tk.SE)
        logging.info('Canvas circle widget initialized for text editor')

    def set_window_weights(self):
        """
        Set the column and row weights for the main window.
        """
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)
        self.window.rowconfigure(2, weight=1)
        logging.info('Main window weights set')

    def open_project_action(self):
        """
        Opens a folder and checks if it is a valid Spring Boot application.
        If it is, sets the working state otherwise sets the initial state.
        """
        try:
            # Check if there is any action running
            if self.busy:
                return
        
            logging.info('Opening project folder')
            project_path = filedialog.askdirectory(title='Select Spring Boot project folder')
            if not project_path:
                logging.warning('No project path selected')
                return
            
            self.init_variables()
            self.project_path = utils.get_path(project_path, '')
            self.project_name = utils.get_base_name(self.project_path)
            logging.info(f'Checking if folder "{self.project_name}" is a valid Spring Boot application')
            self.build_tool, is_spring_boot = utils.is_spring_boot_application(self.project_path)
            if not is_spring_boot:
                self.console_output.config(text=f'{cfg.CONSOLE_LOG_LEVEL_TAGS["WARN"]} The selected folder "{self.project_name}" is NOT a valid Spring Boot application!', fg=WARNING_COLOR)
                logging.warning(f'Folder "{self.project_name}" is NOT a valid Spring Boot application')
                self.initial_state()
                return

            # Check if the project dependencies are valid
            if not self.check_project_dependencies():
                return

            self.working_state()
            self.create_necessary_folders()
            content = self.get_grammar_file_content()
            self.text_editor.insert(tk.INSERT, content)
            self.update_line_numbers()
            self.set_color_to_text()
            self.console_output.config(text=f'{cfg.CONSOLE_LOG_LEVEL_TAGS["INFO"]} The selected folder "{self.project_name}" is a valid {self.build_tool} Spring Boot application.', fg=INFORMATION_COLOR)
            logging.info(f'Folder "{self.project_name}" is a valid Spring Boot application')
        except Exception as e:
            error_message = f'Failed to open project: {str(e)}'
            logging.error(error_message)
            self.console_output.config(text=f'{cfg.CONSOLE_LOG_LEVEL_TAGS["ERROR"]} {utils.add_punctuation(error_message)}', fg=ERROR_COLOR)

    def save_grammar_action(self, event=None):
        """
        Save the grammar file using the current file name if set; otherwise, prompt for a new file name using SaveWindowGUI.
        """
        def run_save_action():
            """
            Run the save action in a separate thread.
            """
            try:
                # If the file name is already set, save it
                if self.grammar_file_name is not None:
                    logging.info(f'Saving to "{self.grammar_file_name}" grammar file')
                    self.save_file_name(event)
                    self.save_event.set()  # Signal save completion
                    return
                
                if self.save_window_instance is None or not self.save_window_instance.winfo_exists():
                    logging.info('Creating new SaveWindowGUI instance')
                    self.save_window_instance = SaveWindowGUI(self)
                else:
                    logging.info('Bringing existing SaveWindowGUI instance to the front')
                    self.save_window_instance.lift()
            except Exception as e:
                error_message = f'Failed to save grammar: {str(e)}'
                logging.error(error_message)
                self.console_output.config(text=f'{cfg.CONSOLE_LOG_LEVEL_TAGS["ERROR"]} {utils.add_punctuation(error_message)}', fg=ERROR_COLOR)
            finally:
                # Reset flag for the next action
                self.busy = False
        # Check if there is any action running
        if self.busy:
            return
        # Run the save action in a separate thread
        self.busy = True
        threading.Thread(target=run_save_action).start()

    def generate_action(self, event=None):
        """
        Handles the action of generating metamodel and model.
        """
        def run_generate_action():
            """
            Run the generate action in a separate thread.
            """
            try:
                # Check if the grammar file name is set
                if self.grammar_file_name is None:
                    messagebox.showwarning(title='Warning', message='Please save the grammar file first!')
                    self.generate_button.config(state=tk.DISABLED)
                    return
                
                # Check if the project dependencies are valid
                if not self.check_project_dependencies():
                    return

                logging.info('Starting generate action')
                self.window.update_idletasks()

                # Wait for save action to complete
                self.save_grammar_action(event=True)
                self.save_event.wait()

                self.busy = True
                self.remove_error_color()
                loading_text = f'{cfg.CONSOLE_LOG_LEVEL_TAGS["INFO"]} Generating, please wait...'
                self.update_loading_animation(loading_text)
                response = TextXGrammar.generate(self.project_path, self.grammar_file_name, self.database_driver)
                if response.status is cfg.OK:
                    self.busy = False
                    self.export_button.config(state=tk.NORMAL)
                    response_color = OK_COLOR
                    response_text = f'{cfg.CONSOLE_LOG_LEVEL_TAGS["OK"]} Successfully executed generate action.'
                    self.console_output.config(text=response_text, fg=response_color)
                    self.run_generated_project()
                else:
                    response_color = ERROR_COLOR
                    self.set_error_color(response)
                    response_text = f'{cfg.CONSOLE_LOG_LEVEL_TAGS["ERROR"]} {utils.add_punctuation(response.error_msg)}'
                    logging.error(f'Error during generate: {response.error_msg}')
                    self.console_output.config(text=response_text, fg=response_color)
            except Exception as e:
                error_message = f'Failed to generate metamodel and model: {str(e)}'
                logging.error(error_message)
                self.console_output.config(text=f'{cfg.CONSOLE_LOG_LEVEL_TAGS["ERROR"]} {utils.add_punctuation(error_message)}', fg=ERROR_COLOR)
            finally:
                # Reset flag for the next action
                self.busy = False
                self.save_event.clear()  # Reset event for next use

        # Check if there is any action running
        if self.busy:
            return
        # Run the generate action in a separate thread
        threading.Thread(target=run_generate_action).start()

    def export_action(self):
        """
        Export the metamodel and model files to the project export folder.
        """
        def run_export_action():
            """
            Run the export action in a separate thread.
            """
            try:
                export_folder = utils.get_path(cfg.JSD_MBRS_GENERATOR_FOLDER, cfg.EXPORT_FOLDER)
                logging.info(f'Starting to export metamodel and model files to the "{export_folder}" folder')
                loading_text = f'{cfg.CONSOLE_LOG_LEVEL_TAGS["INFO"]} Exporting, please wait...'
                self.update_loading_animation(loading_text)
                self.window.update_idletasks()

                # Export the metamodel and model to the project folder
                response = TextXGrammar.export()
                if response.status is cfg.OK:
                    response_color = OK_COLOR
                    response_text = f'{cfg.CONSOLE_LOG_LEVEL_TAGS["OK"]} Successfully exported files to the "{export_folder}" folder.'
                elif response.status is cfg.WARNING:
                    response_color = WARNING_COLOR
                    response_text = f'{cfg.CONSOLE_LOG_LEVEL_TAGS["WARN"]} Files exported with warnings to the "{export_folder}" folder.'
                else:
                    response_color = ERROR_COLOR
                    response_text = f'{cfg.CONSOLE_LOG_LEVEL_TAGS["ERROR"]} {utils.add_punctuation(response)}'
                
                # Update the console output
                self.console_output.config(text=response_text, fg=response_color)
            except Exception as e:
                error_message = f'Failed to export the textX grammar metamodel and/or model: {str(e)}'
                logging.error(error_message)
                self.console_output.config(text=f'{cfg.CONSOLE_LOG_LEVEL_TAGS["ERROR"]} {utils.add_punctuation(error_message)}', fg=ERROR_COLOR)
            finally:
                # Reset flag for the next action
                self.busy = False

        # Check if there is any action running
        if self.busy:
            return
        # Run the export in a separate thread
        self.busy = True
        threading.Thread(target=run_export_action).start()

    def help_action(self):
        """
        Function to open the help window.
        """
        try:
            if self.help_window_instance is None or not self.help_window_instance.winfo_exists():
                logging.info('Creating new HelpWindowGUI instance')
                self.help_window_instance = HelpWindowGUI(self)
            else:
                logging.info('Bringing existing HelpWindowGUI instance to the front')
                self.help_window_instance.lift()
        except Exception as e:
            error_message = f'Failed to open help window: {str(e)}'
            logging.error(error_message)
            self.console_output.config(text=f'{cfg.CONSOLE_LOG_LEVEL_TAGS["ERROR"]} {error_message}', fg=ERROR_COLOR)

    def run(self):
        """
        Method for running the main window.
        """
        logging.info('Running main window loop')
        self.window.mainloop()

    def on_type_text(self, event=None):
        """
        Method for handling the key release event.
        """
        logging.debug('Key release event detected')
        if event and event.keysym in cfg.KEYSYMS_TO_IGNORE:
            logging.debug(f'Key "{event.keysym}" is in the list of keys to ignore. Skipping the rest of the code')
            return
        
        self.update_line_numbers(event)
        self.compare_grammar_content()
        self.remove_error_color()
    
    def on_mouse_click(self, event=None):
        """
        Method for handling the mouse click event.
        """
        logging.debug('Mouse click event detected')
        # Handle the mouse click event to call scroll function if scrollbar is clicked
        if event and event.widget.winfo_class() == 'Scrollbar':
            self.on_scroll(event)

    def on_scroll(self, event=None):
        """
        Method for handling the scroll event.
        """
        logging.debug('Scroll event detected. Scheduling line numbers update')
        # Call update line numbers function after small delay
        self.window.after(1, self.update_line_numbers)

    def on_save(self, event=None):
        """
        Method for handling the save event.
        """
        self.save_grammar_action(event)

    def on_paste(self, event=None):
        """
        Method for handling the paste event.
        """
        logging.debug('Paste event detected. Scheduling set color to text')
        self.window.after(1, self.set_color_to_text)

    def on_remove_line(self, event=None):
        """
        Method for handling the remove line event.
        """
        line_number = self.text_editor.index(tk.INSERT).split('.')[0]
        next_line_start = f'{int(line_number) + 1}.0'
        self.text_editor.delete(f'{line_number}.0', next_line_start)

    def on_tab(self, event=None):
        """
        Method for handling the tab event.
        """
        self.text_editor.insert(tk.INSERT, '    ')
        return 'break'

    def on_window_close(self):
        """
        Method for handling the main window close event.
        """
        import os
        logging.info('Handling main window close event')
        self.window.destroy()
        self.window.quit()
        os._exit(0)

    def initial_state(self):
        """
        Set the initial state of the main window.
        """
        self.init_variables()
        self.save_button.config(state=tk.DISABLED)
        self.generate_button.config(state=tk.DISABLED)
        self.export_button.config(state=tk.DISABLED)
        self.circle_canvas.itemconfig(self.circle, outline=BLACK_COLOR, fill=OK_COLOR)
        self.text_editor.delete('1.0', tk.END)
        self.update_line_numbers()
        self.text_editor.config(state=tk.DISABLED, cursor='arrow', background=INITIAL_BACKGROUND_COLOR)
        logging.debug('Main window initial state set')

    def working_state(self):
        """
        Set the working state of the main window.
        """
        self.save_button.config(state=tk.NORMAL)
        self.generate_button.config(state=tk.NORMAL)
        self.export_button.config(state=tk.DISABLED)
        self.text_editor.delete('1.0', tk.END)
        self.update_line_numbers()
        self.text_editor.config(state=tk.NORMAL, cursor='ibeam', background=WORKING_BACKGROUND_COLOR)
        logging.debug('Main window working state set')

    def check_project_dependencies(self):
        """
        Checks the dependencies in the path of the build configuration file.
        Returns True if dependencies are valid.
        """
        logging.info('Checking project dependencies')
        build_tool_dependency = BuildToolDependency(self.project_name, self.project_path, self.build_tool)
        response = build_tool_dependency.check_dependencies()
        self.set_database_driver(response.database_driver)
        if response.status == cfg.OK:
            logging.info('Project dependencies are valid')
            return True
        elif response.status == cfg.WARNING:
            logging.warning(response.message)
            self.initial_state()
            self.console_output.config(text=f'{cfg.CONSOLE_LOG_LEVEL_TAGS["WARN"]} {utils.add_punctuation(response.message)}', fg=WARNING_COLOR)
            return False
        elif response.status is cfg.ERROR:
            logging.error(response.message)
            message = f'{response.message}\n\nWould you like to add the missing dependencies?'
            if messagebox.askyesno('Missing dependencies', message):
                build_tool_dependency.add_missing_dependencies()
                logging.info('Missing dependencies added')
                return True
            else:
                self.initial_state()
                raise Exception(response.message)

    def create_necessary_folders(self):
        """
        Create the necessary folders in the project folder if they don't exist.
        """
        utils.create_folder(self.project_path, cfg.JSD_MBRS_GENERATOR_FOLDER)
        jsd_mbrs_generator_folder_path = utils.get_path(self.project_path, cfg.JSD_MBRS_GENERATOR_FOLDER)
        utils.create_folder(jsd_mbrs_generator_folder_path, cfg.GRAMMAR_FOLDER)
        utils.create_folder(jsd_mbrs_generator_folder_path, cfg.EXPORT_FOLDER)
        utils.create_folder(jsd_mbrs_generator_folder_path, cfg.RESOURCES_FOLDER)

    def update_line_numbers(self, event=None):
        """
        Updates the line numbers in the line number text widget based on the content of the text editor.
        """
        # Return if the text editor is disabled
        if self.text_editor.cget('state') == tk.DISABLED:
            return

        # Update the line numbers
        logging.debug('Updating line numbers in the line number text widget')
        self.line_number_text.config(state=tk.NORMAL)
        self.line_number_text.delete('1.0', tk.END)
        content = self.get_text_editor_content()
        total_lines = content.count('\n') + 1
        line_numbers = ''.join(f'{i}\n' for i in range(1, total_lines))
        self.line_number_text.insert(tk.END, str(line_numbers), 'right_align')
        self.line_number_text.insert(tk.END, str(total_lines), 'right_align')
        self.line_number_text.config(state=tk.DISABLED)
        logging.debug(f'Line numbers updated. Total lines: {total_lines}')
        self.sync_line_number_yview()

    def sync_line_number_yview(self):
        """
        Sync the vertical scrolling of the line number text widget with the text editor's vertical scrolling.
        """
        logging.debug('Syncing line number text widget with text editor yview')
        yview = self.text_editor.yview()
        self.line_number_text.yview_moveto(yview[0])
        logging.debug('Line number text widget yview synced with text editor yview')

    def periodic_update(self):
        """
        Run periodically to update the grammar text inside the text editor.
        """
        self.set_color_to_text()
        self.text_editor.after(self.periodic_update_interval, self.periodic_update)

    def save_file_name(self, event):
        """
        Save the content of the text editor to a file with the specified grammar file name.
        """
        text_content = self.get_text_editor_content()
        grammar_folder_path = utils.get_path(self.project_path, cfg.JSD_MBRS_GENERATOR_FOLDER, cfg.GRAMMAR_FOLDER)
        file_path = utils.get_path(grammar_folder_path, self.grammar_file_name)
        utils.file_exists(grammar_folder_path, self.grammar_file_name)
        utils.write_to_file(file_path, text_content)
        self.circle_canvas.itemconfig(self.circle, fill=OK_COLOR)
        self.grammar_file_content = text_content
        if not event:
            messagebox.showinfo('File Name', f'The grammar "{self.grammar_file_name}" has been saved successfully!')
        logging.info(f'Saved text editor content to "{self.grammar_file_name}"')

    def get_grammar_file_content(self):
        """
        Searches for grammar file in the specified folder and return its content.
        If no grammar files are found, a default content is returned. If multiple grammar files are found, the user is prompted to select one.
        """
        folder_path = utils.get_path(self.project_path, cfg.JSD_MBRS_GENERATOR_FOLDER, cfg.GRAMMAR_FOLDER)
        grammar_array = utils.find_specific_file_regex(folder_path, cfg.JSD_MBRS_GENERATOR_REGEX)
        if len(grammar_array) == 0:
            # No grammar files found, use a default content
            logging.info('No grammar files found. Using a default content')
            self.grammar_file_content = cfg.DEFAULT_CONTENT
        elif len(grammar_array) == 1:
            # Only one grammar file found, read its content
            self.set_grammar_file_name(grammar_array[0])
            grammar_path = utils.get_path(folder_path, self.grammar_file_name)
            self.grammar_file_content = utils.read_file(grammar_path)
            logging.info(f'Read grammar file content from "{self.grammar_file_name}"')
        else:
            # Multiple grammar files found, ask the user to select one
            file_path = filedialog.askopenfilename(initialdir=folder_path, title='Select JSD-MBRS grammar file', filetypes=[('JSD-MBRS Grammar Files', '*.jsdmbrs')])
            if not file_path or not utils.compare_paths(folder_path, file_path):
                raise ValueError('Invalid grammar file selected')
            self.grammar_file_content = utils.read_file(file_path)
            self.set_grammar_file_name(utils.get_base_name(file_path))
            logging.info(f'Multiple grammar files found. Selected "{self.grammar_file_name}"')
        return self.grammar_file_content
    
    def compare_grammar_content(self):
        """
        Compare the content of the text editor with the content of the specified grammar file.
        """
        text_content = self.get_text_editor_content()
        if text_content != self.grammar_file_content:
            logging.debug('Text editor content does not match the grammar file content')
            self.circle_canvas.itemconfig(self.circle, fill=WARNING_COLOR)
        else:
            logging.debug('Text editor content matches the grammar file content')
            self.circle_canvas.itemconfig(self.circle, fill=OK_COLOR)

    def set_color_to_text(self):
        """
        Set the color of the words in the text editor.
        """
        logging.debug('Setting color to text')

        # Set the default font color first
        self.set_default_font_color(DEFAULT_FONT_COLOR)  

        # Apply color to text based on the color mappings
        for words_list, color in self.color_mappings:
            self.apply_color_to_text(words_list, color)

        self.rule_defined_signs_color(RULE_DEFINED_SIGNS_COLOR)
        self.class_name_color(CLASS_NAME_COLOR)
        self.property_value_color(PROPERTY_VALUE_COLOR)
        self.comment_color(COMMENT_COLOR)  # Color comments last to override other colors
        logging.debug('Color set to text')

    def remove_error_color(self):
        """
        Remove the error color from the text editor.
        """
        logging.debug('Removing error color')
        self.text_editor.tag_remove(ERROR_COLOR, '1.0', tk.END)
        logging.debug('Error color removed')

    def set_default_font_color(self, color):
        """
        Set the default font color in the text editor.
        """
        logging.debug('Setting default font color')
        self.text_editor.tag_configure(color, foreground=color)
        self.text_editor.tag_add(color, '1.0', tk.END)
        logging.debug('Default font color set')

    def rule_defined_signs_color(self, color):
        """
        Apply color to rule defined signs in the text editor.
        """
        logging.debug('Applying color to rule defined signs')
        content = self.get_text_editor_content()
        rule_defined_signs = utils.extract_rule_defined_signs_regex(content)
        self.apply_color_to_text(rule_defined_signs, color, check_signs=True)
        logging.debug('Color applied to rule defined signs')

    def class_name_color(self, color):
        """
        Apply color to class names in the text editor.
        """
        logging.debug('Applying color to class names')
        content = self.get_text_editor_content()
        class_names = utils.extract_class_names_regex(content)
        self.apply_color_to_text(class_names, color)
        logging.debug('Color applied to class names')

    def property_value_color(self, color):
        """
        Apply color to property value in the text editor.
        """
        logging.debug('Applying color to property value')
        content = self.get_text_editor_content()
        property_value = utils.extract_property_values_regex(content)
        self.apply_color_to_text(property_value, color)
        logging.debug('Color applied to property value')

    def comment_color(self, color):
        """
        Apply color to comments in the text editor.
        """
        logging.debug('Applying color to comments')
        content = self.get_text_editor_content()
        comments = utils.extract_comments_regex(content)
        self.apply_color_to_text(comments, color)
        logging.debug('Color applied to comments')

    def set_error_color(self, response):
        """
        Set the error color in the text editor based on the error type.
        """
        logging.debug('Setting error color')
        if response.error_class == 'TextXSyntaxError':
            self.syntax_error_color(response)
        elif response.error_class == 'TextXSemanticError':
            if not hasattr(response, 'search_value'):
                self.remove_tags_text_editor(f'{response.error.line}.0', f'{response.error.line}.end')
                self.text_editor.tag_configure(ERROR_COLOR, foreground=ERROR_COLOR)
                self.text_editor.tag_add(ERROR_COLOR, f'{response.error.line}.0', f'{response.error.line}.end')
                return
            self.semantic_error_color(response)
        elif response.error_class == 'SemanticError':
            self.semantic_error_color(response)
        logging.debug('Error color set')

    def syntax_error_color(self, response):
        """
        Highlights the line with a syntax error in the text editor.
        """
        logging.debug('Setting syntax error color')

        def is_near_part_in_line(line_number):
            logging.debug(f'Checking if error near part: {near_part} is in line "{line_number}"')
            start_index = f'{line_number}.0'
            end_index = f'{line_number}.end'
            line_text = self.text_editor.get(start_index, end_index)
            return near_part in line_text if near_part else False

        near_part = response.near_part
        penultimate_line_number = response.error.line - 2
        previous_line_number = response.error.line - 1
        current_line_number = response.error.line
        error_message = response.error_msg

        if is_near_part_in_line(previous_line_number):
            start_index = f'{previous_line_number}.0'
            end_index = f'{previous_line_number}.end'
            response.error_msg = error_message.replace(str(current_line_number), str(previous_line_number))
            response.error.line = previous_line_number
            logging.debug(f'Highlighting previous line: "{previous_line_number}"')
        elif is_near_part_in_line(penultimate_line_number):
            start_index = f'{penultimate_line_number}.0'
            end_index = f'{penultimate_line_number}.end'
            response.error_msg = error_message.replace(str(current_line_number), str(penultimate_line_number))
            response.error.line = penultimate_line_number
            logging.debug(f'Highlighting current line: "{penultimate_line_number}"')
        else:
            start_index = f'{current_line_number}.0'
            end_index = f'{current_line_number}.end'
            logging.debug(f'Highlighting current line: "{current_line_number}"')

        self.remove_tags_text_editor(start_index, end_index)
        self.text_editor.tag_configure(ERROR_COLOR, foreground=ERROR_COLOR)
        self.text_editor.tag_add(ERROR_COLOR, start_index, end_index)
        logging.debug('Syntax error color set')

    def semantic_error_color(self, response):
        """
        Checks if the error's search value is a list or not and according to that call appropriate function.
        """
        search_value = response.error.search_value
        logging.debug(f'Semantic error search value: "{search_value}"')
        if isinstance(search_value, list):
            for value in search_value:
                self.handle_list_semantic_error(response, value)
        else:
            self.apply_semantic_error_color(response, search_value)
        logging.debug('Semantic error color set')

    def handle_list_semantic_error(self, response, value):
        """
        Handles semantic error if the search value is a list.
        """
        logging.debug(f'Handling semantic error for list value: "{value}"')
        if isinstance(value, dict):
            for class_name, search_value in value.items():
                for word in str(search_value).split():
                    self.apply_semantic_error_color(response, word, class_name)
        else:
            self.apply_semantic_error_color(response, value)

    def apply_semantic_error_color(self, response, search_value, class_name=None):
        """
        Apply the semantic error color to the every specified search value in the text editor (check only the line where the error occurred).
        """
        error_line = self.handle_error_type(response, search_value, class_name)
        logging.debug(f'Applying semantic error color for {search_value} in line {error_line}')
        line_text = self.text_editor.get(f'{error_line}.0', f'{error_line}.end')
        if utils.check_words_in_string(search_value, line_text):
            start_index = 0
            while start_index < len(line_text):
                start_index = line_text.find(search_value, start_index)
                if start_index == -1:
                    break
                end_index = start_index + len(search_value)
                if self.is_whole_word(f'{error_line}.{start_index}', f'{error_line}.{end_index}'):
                    logging.debug(f'Highlighting {search_value} from {start_index} to {end_index} in line {error_line}')
                    self.remove_tags_text_editor(f'{error_line}.{start_index}', f'{error_line}.{end_index}')
                    self.text_editor.tag_configure(ERROR_COLOR, foreground=ERROR_COLOR)
                    self.text_editor.tag_add(ERROR_COLOR, f'{error_line}.{start_index}', f'{error_line}.{end_index}')
                    return  # TODO: check if this is ok, if not remove it
                start_index = end_index

    def handle_error_type(self, response, search_value, class_name):
        """
        Handle the error type and return the line where the error occurred.
        """
        error_line = response.error.line
        error_type = response.error.err_type
        logging.debug(f'Handling error type: "{error_type}"')
        if error_type in ['database_name_error', 'database_username_error', 'database_password_error', 'multiple_id_property_error', 'entity_relationships_error']:
            error_line = self.find_line_containing_search_value(response, search_value, class_name)
        logging.debug(f'Error line updated to: {error_line}')
        return error_line

    def find_line_containing_search_value(self, response, search_value, class_name):
        """
        Find the line number containing the specified search value.
        """
        def find_class(class_name, line_text):
            """
            Find the class name in the line text.
            """
            logging.debug('Checking class existence in line')
            if not class_name:
                return True
            class_to_check = utils.extract_class_names_regex(line_text)
            return class_name in class_to_check
        
        class_found = False
        line = response.error.line
        total_lines = int(self.text_editor.index(tk.END).split('.')[0])
        while line <= total_lines:
            logging.debug(f'Searching for "{search_value}" in line {line}')
            line_text = self.text_editor.get(f'{line}.0', f'{line}.end')

            if not class_found :
                class_found = find_class(class_name, line_text)

            if utils.check_words_in_string(search_value, line_text) and class_found:
                logging.debug(f'Found "{search_value}" in line {line}')
                response.error_msg = response.error_msg.replace(str(response.error.line), str(line))
                response.error.line = line
                return line
            line += 1
        return response.error.line
        
    def remove_tags_text_editor(self, start_index, end_index):
        """
        Remove tags from start until end index in the text editor.
        """
        logging.debug(f'Removing tags from text editor from "{start_index}" to "{end_index}"')
        all_tags = self.text_editor.tag_names()
        # Remove each tag from the specific line
        for tag in all_tags:
            self.text_editor.tag_remove(tag, start_index, end_index)
            logging.debug(f'Removed tag "{tag}"')

    def apply_color_to_text(self, text_list, color, check_signs=False):
        """
        Apply the color to the words in the text editor based on the provided parameters.
        """
        logging.debug(f'Applying color "{color}" to text')
        self.text_editor.tag_remove(color, '1.0', tk.END)
        self.text_editor.tag_configure(color, foreground=color)
        for word in text_list:
            start_index = '1.0'
            while True:
                match_start = self.text_editor.search(word, start_index, stopindex=tk.END)
                # If no match is found, break the loop
                if not match_start:
                    break
                end_index = f'{match_start}+{len(word)}c'
                if self.is_whole_word(match_start, end_index) or check_signs:
                    # Apply the color to the word
                    self.text_editor.tag_add(color, match_start, end_index)
                    logging.debug(f'Applied color "{color}" to word "{word}"')
                # Update the start index for the next search
                start_index = end_index

    def is_whole_word(self, start_index, end_index):
        """
        Check if the selected text is a whole word.
        """
        def is_valid_java_char(c):
            """
            Define valid characters for Java variable names.
            """
            return str(c).isalnum() or str(c) in {'$', '_'}
        
        logging.debug(f'Checking if {start_index} to {end_index} is a whole word')
        before_char = '' if start_index == '1.0' else self.text_editor.get(f'{start_index}-1c')
        after_char = self.text_editor.get(f'{end_index}')
        is_whole_word = not (before_char.isalnum() or after_char.isalnum())
        # Check if the before and after characters are not valid Java variable name characters
        is_whole_word = not is_valid_java_char(before_char) and not is_valid_java_char(after_char)
        logging.debug(f'before_char: {before_char}, after_char: {after_char}, Result: {is_whole_word}')
        return is_whole_word
    
    def update_loading_animation(self, loading_text):
        """
        Update the loading animation in the console output if the console is busy.
        """
        if not self.busy:
            return
        logging.debug('Updating loading animation')
        self.symbol_index = (self.symbol_index + 1) % len(cfg.LOADING_SYMBOLS)
        loading_animation = f'{loading_text} {cfg.LOADING_SYMBOLS[self.symbol_index]}'
        self.console_output.config(text=loading_animation, fg=INFORMATION_COLOR)
        self.console_output.after(50, lambda: self.update_loading_animation(loading_text))

    def run_generated_project(self):
        """
        Run the generated project.
        """
        logging.debug('Running generated project')
        if messagebox.askyesno('Run project', 'Do you want to build and run the generated project?'):
            self.busy = True
            self.open_button.config(state=tk.DISABLED)
            self.generate_button.config(state=tk.DISABLED)
            run_generated_project = RunGeneratedProject(self.project_path, self.build_tool)
            response = run_generated_project.run_generated_project()
            if response.status is cfg.ERROR:
                error_message = f'{cfg.CONSOLE_LOG_LEVEL_TAGS["ERROR"]} {utils.add_punctuation(response.message)}'
                self.console_output.config(text=error_message, fg=ERROR_COLOR)
            self.busy = False
            self.open_button.config(state=tk.NORMAL)
            self.generate_button.config(state=tk.NORMAL)

    def get_text_editor_content(self):
        """
        Get the content of the text editor, excluding the last character (newline).
        """
        logging.debug('Retrieving text editor content')
        end_minus_one = self.text_editor.index(f'{tk.END}-1c')
        return self.text_editor.get('1.0', end_minus_one)
    
    def get_cursor_position(self):
        """
        Get the cursor position in the text editor.
        """
        logging.debug(f'Retrieving cursor position')
        cursor_position = self.text_editor.index(tk.INSERT)
        line, col = map(int, cursor_position.split('.'))
        logging.debug(f'Cursor position - line: {line}, column: {col}')
        return cursor_position
    
    def get_last_typed_char(self):
        """
        Get the last character in the text editor after on type event (first char before cursor).
        """
        logging.debug('Getting last typed character')
        cursor_position = self.get_cursor_position()
        last_char_position = f'{cursor_position}-1c'
        last_char = self.text_editor.get(last_char_position, cursor_position)
        logging.debug(f'Last typed character is: "{last_char}"')
        return last_char
    
    def get_project_path(self):
        """
        Get the path of the project.
        """
        logging.debug(f'Retrieving project path: "{self.project_path}"')
        return self.project_path
    
    def get_grammar_file_name(self):
        """
        Get the name of the grammar.
        """
        logging.debug(f'Retrieving grammar name: "{self.grammar_file_name}"')
        return self.grammar_file_name
    
    def set_grammar_file_name(self, grammar_file_name):
        """
        Set the name of the grammar.
        """
        logging.debug(f'Setting grammar name: "{grammar_file_name}"')
        self.grammar_file_name = grammar_file_name

    def set_database_driver(self, database_driver):
        """
        Set the database driver.
        """
        logging.debug(f'Setting database driver: "{database_driver}"')
        self.database_driver = database_driver


class HelpWindowGUI(tk.Toplevel):
    """
    Class for creating the help window.
    """
    def __init__(self, parent):
        """
        Constructor for the HelpWindowGUI class.
        """
        logging.info('Creating HelpWindowGUI instance')
        self.parent = parent
        self.help_text = self.read_help_file()
        self.init_window()

    def init_window(self):
        """
        Initialize the help window.
        """
        logging.info('Initializing help window')
        self.help_window = tk.Toplevel(self.parent.window)
        self.help_window.title(cfg.HELP_WINDOW_TITLE)
        self.help_window.resizable(False, False)
        self.help_window.protocol('WM_DELETE_WINDOW', lambda: self.on_help_window_close(self.help_window))
        self.help_window_font = utils.set_font(cfg.FONT, 11)
        self.help_window.geometry(position_window(self.help_window, cfg.HELP_WINDOW_WIDTH, cfg.HELP_WINDOW_HEIGHT))
        self.help_window.focus_set()
        self.help_window.grab_set()
        self.init_window_components()
        self.update_help_scrolled_text_widget()

    def init_window_components(self):
        """
        Initializes the components of the help window.
        """
        logging.info('Initializing help window components')
        self.init_help_scrolled_text()

    def init_help_scrolled_text(self):
        """
        Initialize the help scrolled text widget.
        """
        self.help_scrolled_text = scrolledtext.ScrolledText(self.help_window, wrap=tk.WORD, font=self.help_window_font, background=INITIAL_BACKGROUND_COLOR)
        self.help_scrolled_text.pack(padx=10, pady=10)
        logging.info('Scrolled text widget initialized')

    def on_help_window_close(self, help_window):
        """
        Method for handling the help window close event.
        """
        logging.info('Handling help window close event')
        self.parent.help_window_instance = None  # Reset the instance reference in the parent
        help_window.destroy()
        self.parent.window.focus_set()
        
    def read_help_file(self):
        """
        Reads the content of the help file located in the resources folder and returns it as a string.
        """
        utils.folder_exists(cfg.RESOURCES_FOLDER)
        utils.file_exists(cfg.RESOURCES_FOLDER, cfg.HELP_FILE)
        logging.info(f'Reading "{cfg.HELP_FILE}" file')
        return utils.read_file(utils.get_path(cfg.RESOURCES_FOLDER, cfg.HELP_FILE))
    
    def update_help_scrolled_text_widget(self):
        """
        Updates the help scrolled text widget with the content of the help file.
        """
        self.help_scrolled_text.insert('1.0', self.help_text)
        self.help_scrolled_text.config(state=tk.DISABLED)
        logging.info(f'Content of "{cfg.HELP_FILE}" file loaded into scrolled text widget')


class SaveWindowGUI(tk.Toplevel):
    """
    Class for creating the save window.
    """
    def __init__(self, parent):
        """
        Constructor for the SaveWindowGUI class.
        """
        logging.info('Creating SaveWindowGUI instance')
        self.parent = parent
        self.init_window()

    def init_window(self):
        """
        Initialize the save window.
        """
        logging.info('Initializing save window')
        self.save_window = tk.Toplevel(self.parent.window)
        self.save_window.title(cfg.SAVE_WINDOW_TITLE)
        self.save_window.resizable(False, False)
        self.save_window.protocol('WM_DELETE_WINDOW', lambda: self.on_save_window_close(self.save_window))
        self.save_window_font = utils.set_font(cfg.FONT, 11)
        self.save_window.geometry(position_window(self.save_window, cfg.SAVE_WINDOW_WIDTH, cfg.SAVE_WINDOW_HEIGHT))
        self.save_window.focus_set()
        self.save_window.grab_set()
        self.save_window.after(1, lambda: config_style(self.save_window, self.save_window_font))
        self.init_window_components()

    def init_window_components(self):
        """
        Initializes the components of the save window.
        """
        logging.info('Initializing save window components')
        self.init_save_label()
        self.init_save_entry()
        self.init_save_button()

    def init_save_label(self):
        """
        Initialize the save label widget.
        """
        grammar_file_name = self.parent.get_grammar_file_name()
        if grammar_file_name:
            label_text = f'Enter the grammar name. If you enter an existing name, the grammar will be overwritten (Currently selected: {grammar_file_name} grammar.):'
        else:
            label_text = 'Enter the grammar name:'
        self.save_label = tk.Label(self.save_window, text=label_text, background=INITIAL_BACKGROUND_COLOR)
        self.save_label.pack(padx=10, pady=10)
        logging.info('Label widget initialized')

    def init_save_entry(self):
        """
        Initialize the save entry widget.
        """
        self.save_entry = tk.Entry(self.save_window, width=50)
        self.save_entry.pack(padx=10, pady=5)
        self.save_entry.bind('<KeyRelease>', self.on_type_text)
        logging.info('Entry widget initialized')

    def init_save_button(self):
        """
        Initialize the save button widget.
        """
        self.submit_button = ttk.Button(self.save_window, text='Save grammar', command=self.save_file_name, compound=tk.TOP, style='Button.TButton', state=tk.DISABLED)
        self.submit_button.pack(pady=10)
        logging.info('Button widget initialized')

    def on_type_text(self, event=None):
        """
        Updates the state of the save button based on the content of the save entry widget.
        """
        if self.get_save_entry_text():
            self.submit_button.config(state=tk.NORMAL)
        else:
            self.submit_button.config(state=tk.DISABLED)

    def on_save_window_close(self, save_window):
        """
        Method for handling the save window close event.
        """
        logging.info('Handling save window close event')
        self.parent.save_window_instance = None  # Reset the instance reference in the parent
        save_window.destroy()
        self.parent.window.focus_set()

    def save_file_name(self):
        """
        Saves the content of the MainWindowGUI text editor to a file with the given file name.
        """
        logging.info('Creating a new grammar file')
        save_entry_text = self.get_save_entry_text()
        file_name = f'{save_entry_text}{cfg.JSD_MBRS_GENERATOR_EXTENSION}'
        if file_name:
            project_path = self.parent.get_project_path()
            text_content = self.parent.get_text_editor_content()
            file_path = utils.get_path(project_path, cfg.JSD_MBRS_GENERATOR_FOLDER, cfg.GRAMMAR_FOLDER, file_name)
            utils.write_to_file(file_path, text_content)
            self.parent.set_grammar_file_name(file_name)
            self.parent.generate_button.config(state=tk.NORMAL)
            self.parent.circle_canvas.itemconfig(self.parent.circle, fill=OK_COLOR)
            self.parent.grammar_file_content = text_content
            self.parent.save_event.set()  # Signal save completion
            logging.info(f'Text editor contents saved to a new file: "{file_name}"')
            messagebox.showinfo('File Name', f'The grammar "{file_name}" has been saved successfully!')
            self.on_save_window_close(self.save_window)
        else:
            logging.warning('Input Error: No file name entered')
            messagebox.showwarning('Input Error', 'Please enter a grammar file name.')

    def get_save_entry_text(self):
        """
        Returns the file name entered in the save entry widget.
        """
        return self.save_entry.get().strip()