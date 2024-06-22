import utils
import logging
import config as cfg
import tkinter as tk
import textx_grammar as tg
from ttkthemes import ThemedStyle
from tkinter import ttk, scrolledtext, filedialog


OK_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['ok'])
INITIAL_BACKGROUND_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['initial_background'])
WORKING_BACKGROUND_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['working_background'])
INFORMATION_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['information'])
WARNING_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['warning'])
ERROR_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['error'])


def position_window(window, width, height):
    """
    Computes the geometry string for positioning a window at the center of the screen.
    """
    logging.info(f'Positioning {window.title()} window')
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_position = (screen_width - width) // 2
    y_position = (screen_height - height) // 2
    window_geometry = f'{width}x{height}+{x_position}+{y_position}'
    return window_geometry


class MainWindowGUI:
    """
    Class for creating the JSD-MBRS Generator application main window.
    """
    def __init__(self):
        """
        Constructor for the MainWindowGUI class.
        """
        logging.info('Creating MainWindowGUI instance')
        self.help_window_instance = None  # To track the instance of the help window
        self.metamodel = None
        self.model = None
        self.project_path = None
        self.project_name = None
        self.init_window()

    def init_window(self):
        """
        Initialize the main window.
        """
        logging.info('Initializing main window')
        self.window = tk.Tk()
        self.window.title(cfg.MAIN_WINDOW_TITLE)
        self.window.resizable(False, False)
        self.window.protocol('WM_DELETE_WINDOW', self.on_window_close)
        self.input_text_font = utils.set_font(cfg.FONT, 11, True)
        self.window.geometry(position_window(self.window, cfg.MAIN_WINDOW_WIDTH, cfg.MAIN_WINDOW_HEIGHT))
        self.config_style()
        self.init_window_components()
        self.update_line_numbers()

    def config_style(self):
        """
        Configures the style of the main window.
        """
        logging.info('Configuring main window style')
        style = ThemedStyle(self.window)
        style.set_theme(cfg.THEME_STYLE)
        style.configure('Toolbar.TButton', font=self.input_text_font)

    def init_window_components(self):
        """
        Initializes the components of the main window.
        """
        logging.info('Initializing main window components')
        self.init_toolbar()
        self.init_line_number_text()
        self.init_text_editor()
        self.init_console_frame()
        self.set_window_weights()

    def init_toolbar(self):
        """
        Initialize the toolbar with a generate button.
        """
        toolbar = ttk.Frame(self.window)
        self.open_button = ttk.Button(toolbar, text='Open Project', command=self.open_project, compound=tk.TOP, style='Toolbar.TButton')
        self.generate_button = ttk.Button(toolbar, text='Generate', command=self.generate_action, compound=tk.TOP, style='Toolbar.TButton', state=tk.DISABLED)        
        self.export_button = ttk.Button(toolbar, text='Export', command=self.export_action, compound=tk.TOP, style='Toolbar.TButton', state=tk.DISABLED)
        self.help_button = ttk.Button(toolbar, text='Help', command=self.help_action, compound=tk.TOP, style='Toolbar.TButton')

        # Place the buttons in the toolbar
        self.open_button.grid(row=0, column=0, padx=5)
        self.generate_button.grid(row=0, column=1, padx=5)
        self.export_button.grid(row=0, column=2, padx=5)
        self.help_button.grid(row=0, column=5, padx=5)

        # Configure the toolbar
        toolbar.columnconfigure(3, weight=1)
        toolbar.grid(row=0, column=0, columnspan=6, sticky='ew', pady=5)
        logging.info('Toolbar initialized')

    def init_line_number_text(self):
        """
        Initialize line number text widget.
        """
        self.line_number_text = tk.Text(self.window, font=self.input_text_font, width=3, padx=5, wrap=tk.NONE, state=tk.DISABLED, cursor='arrow', background=INITIAL_BACKGROUND_COLOR)
        self.line_number_text.grid(row=1, column=0, padx=5, pady=5, sticky='nsw')
        self.line_number_text.bind('<Key>', lambda event: 'break')
        self.line_number_text.bind('<MouseWheel>', lambda event: 'break')
        self.line_number_text.bind('<B1-Motion>', lambda event: ('break', self.line_number_text.event_generate('<ButtonRelease-1>')))
        self.line_number_text.tag_configure('right_align', justify='right')
        logging.info('Line number text widget initialized')

    def init_text_editor(self):
        """
        Initialize the text editor widget.
        """
        self.text_editor = tk.Text(self.window, wrap=tk.WORD, font=self.input_text_font, height=30, width=80, undo=True, maxundo=-1, state=tk.DISABLED, cursor='arrow', background=INITIAL_BACKGROUND_COLOR)
        self.text_editor.grid(row=1, column=1, padx=10, pady=5, columnspan=2, sticky='nsew')
        self.text_editor.bind('<KeyPress>', self.on_scroll)
        self.text_editor.bind('<KeyRelease>', self.type_text)
        self.text_editor.bind('<MouseWheel>', self.on_scroll)
        self.text_editor.bind('<B1-Motion>', self.on_scroll)
        logging.info('Text editor widget initialized')
    
    def init_console_frame(self):
        """
        Initialize the console frame and its label component.
        """
        console_frame = ttk.Frame(self.window, borderwidth=2, relief='groove')
        console_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky='nsew')
        self.console_output = tk.Label(console_frame, text=cfg.HELP_BUTTON_TEXT, font=self.input_text_font, wraplength=650, fg=INFORMATION_COLOR)
        self.console_output.pack(padx=10, pady=10, ipady=50)
        console_frame.grid_rowconfigure(0, weight=1)
        console_frame.grid_columnconfigure(0, weight=1)
        logging.info('Console frame initialized')

    def set_window_weights(self):
        """
        Set the column and row weights for the main window.
        """
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)
        self.window.rowconfigure(2, weight=1)
        logging.info('Main window weights set')

    def open_project(self):
        """
        Opens a folder and checks if it is a valid Spring Boot application.
        If it is, sets the working state otherwise sets the initial state.
        """
        logging.info('Opening project folder')
        self.project_path = filedialog.askdirectory()
        if not self.project_path:
            logging.warning('No project path selected')
            return

        self.project_name = utils.get_base_name(self.project_path)
        logging.info(f'Checking if folder "{self.project_name}" is a valid Spring Boot application')
        build_tool, is_spring_boot = utils.is_spring_boot_application(self.project_path)
        if not is_spring_boot:
            self.console_output.config(text=f'{cfg.CONSOLE_LOG_LEVEL_TAGS["WARN"]} The selected folder "{self.project_name}" is not a valid Spring Boot application!', fg=WARNING_COLOR)
            self.initial_state()
            logging.warning(f'Folder "{self.project_name}" is not a valid Spring Boot application')
            return

        self.working_state()
        self.console_output.config(text=f'{cfg.CONSOLE_LOG_LEVEL_TAGS["INFO"]} The selected folder "{self.project_name}" is a valid {build_tool} Spring Boot application.', fg=INFORMATION_COLOR)
        self.text_editor.insert(tk.INSERT, 'Hello World!')
        logging.info(f'Folder "{self.project_name}" is a valid Spring Boot application')

    def generate_action(self):
        """
        Get the names of all entities in the model and insert them into the text editor.
        """
        try:
            logging.info('Getting entity names')
            self.metamodel, self.model = tg.test_run()
            entities = ', '.join([f'"{entity.name}"' for entity in self.model.entities])
            self.text_editor.delete('1.0', tk.END)
            self.text_editor.insert(tk.INSERT, entities)
            self.export_button.config(state=tk.NORMAL)
            logging.info('Entity names retrieved and inserted into the text editor')
        except Exception as e:
            error_message = f'Failed to get entity names: {str(e)}'
            logging.error(error_message)
            self.console_output.config(text=f'{cfg.CONSOLE_LOG_LEVEL_TAGS["ERROR"]} {utils.add_punctuation(error_message)}', fg=ERROR_COLOR)
    
    def export_action(self):
        """
        Export the metamodel and model files to the project export folder.
        """
        export_folder = utils.get_path(cfg.JSD_MBRS_GENERATOR_FOLDER, cfg.EXPORT_FOLDER)
        logging.info(f'Starting to export metamodel and model files to the "{export_folder}" folder')
        self.console_output.config(text=f'{cfg.CONSOLE_LOG_LEVEL_TAGS["INFO"]} Exporting, please wait...', fg=INFORMATION_COLOR)
        self.window.update_idletasks()

        # Export the metamodel and model to the project folder
        response = tg.export(self.metamodel, self.model, self.project_path)
        if response is cfg.OK:
            response_color = OK_COLOR
            response_text = f'{cfg.CONSOLE_LOG_LEVEL_TAGS["OK"]} Successfully exported files to the "{export_folder}" folder.'
        elif response is cfg.WARNING:
            response_color = WARNING_COLOR
            response_text = f'{cfg.CONSOLE_LOG_LEVEL_TAGS["WARN"]} Files exported with warnings to the "{export_folder}" folder.'
        else:
            response_color = ERROR_COLOR
            response_text = f'{cfg.CONSOLE_LOG_LEVEL_TAGS["ERROR"]} {utils.add_punctuation(response)}'

        # Update the console output
        self.console_output.config(text=response_text, fg=response_color)
    
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

    def initial_state(self):
        """
        Set the initial state of the main window.
        """
        self.generate_button.config(state=tk.DISABLED)
        self.export_button.config(state=tk.DISABLED)
        self.text_editor.delete('1.0', tk.END)
        self.text_editor.config(state=tk.DISABLED, cursor='arrow', background=INITIAL_BACKGROUND_COLOR)
        self.update_line_numbers()
        logging.debug('Main window initial state set')

    def working_state(self):
        """
        Set the working state of the main window.
        """
        self.generate_button.config(state=tk.NORMAL)
        self.export_button.config(state=tk.DISABLED)
        self.text_editor.delete('1.0', tk.END)
        self.text_editor.config(state=tk.NORMAL, cursor='ibeam', background=WORKING_BACKGROUND_COLOR)
        self.update_line_numbers()
        logging.debug('Main window working state set')

    def update_line_numbers(self, event=None):
        """
        Updates the line numbers in the line number text widget based on the content of the text editor.
        """
        logging.debug('Updating line numbers in the line number text widget.')
        self.line_number_text.config(state=tk.NORMAL)
        self.line_number_text.delete('1.0', tk.END)
        content = self.text_editor.get('1.0', tk.END)
        total_lines = content.count('\n')
        line_numbers = ''.join(f'{i}\n' for i in range(1, total_lines))
        self.line_number_text.insert(tk.END, str(line_numbers), 'right_align')
        self.line_number_text.insert(tk.END, str(total_lines), 'right_align')
        self.line_number_text.config(state=tk.DISABLED)
        logging.debug(f'Line numbers updated. Total lines: {total_lines}.')
        self.sync_line_number_yview()

    def type_text(self, event=None):
        """
        Handler function for the '<KeyRelease>' event.
        """
        self.update_line_numbers(event)

    def on_scroll(self, event=None):
        """
        Handle the scroll event and schedule an update for the line numbers.
        """
        logging.debug('Scroll event detected. Scheduling line numbers update.')
        self.window.after(1, self.update_line_numbers)

    def sync_line_number_yview(self):
        """
        Sync the vertical scrolling of the line number text widget with the text editor's vertical scrolling.
        """
        logging.debug('Syncing line number text widget with text editor yview.')
        yview = self.text_editor.yview()
        self.line_number_text.yview_moveto(yview[0])
        logging.debug('Line number text widget yview synced with text editor yview.')

    def run(self):
        """
        Method for running the main window.
        """
        logging.info('Running main window loop')
        self.window.mainloop()

    def on_window_close(self):
        """
        Method for handling the main window close event.
        """
        logging.info('Handling main window close event')
        self.window.destroy()
        self.window.quit()


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

    def on_help_window_close(self, help_window):
        """
        Method for handling the help window close event.
        """
        logging.info('Handling help window close event')
        self.parent.help_window_instance = None  # Reset the instance reference in the parent
        help_window.destroy()
        self.parent.window.focus_set()
