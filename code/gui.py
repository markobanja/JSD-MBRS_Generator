import utils
import logging
import config as cfg
import tkinter as tk
import textx_grammar as tg
from ttkthemes import ThemedStyle
from tkinter import ttk, scrolledtext, filedialog, messagebox


INITIAL_BACKGROUND_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['initial_background'])
WORKING_BACKGROUND_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['working_background'])
BLACK_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['black'])
OK_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['ok'])
INFORMATION_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['information'])
WARNING_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['warning'])
ERROR_COLOR = utils.convert_rgb_to_hex(cfg.COLORS['error'])


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
        logging.info('Initializing main window variables')
        self.save_window_instance = None  # To track the instance of the save window
        self.help_window_instance = None  # To track the instance of the help window
        self.metamodel = None
        self.model = None
        self.project_path = None
        self.project_name = None
        self.grammar_file_name = None
        self.grammar_file_content = None

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
        config_style(self.window, self.input_text_font)
        self.init_window_components()
        self.initial_state()
    
    def init_window_components(self):
        """
        Initializes the components of the main window.
        """
        logging.info('Initializing main window components')
        self.init_toolbar()
        self.init_line_number_text()
        self.init_text_editor()
        self.init_canvas_circle()
        self.init_console_frame()
        self.set_window_weights()

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

        # Place the buttons in the toolbar
        self.open_button.grid(row=0, column=0, padx=5)
        self.save_button.grid(row=0, column=1, padx=5)
        self.generate_button.grid(row=0, column=2, padx=5)
        self.export_button.grid(row=0, column=3, padx=5)
        self.help_button.grid(row=0, column=5, padx=5)

        # Configure the toolbar
        toolbar.columnconfigure(4, weight=1)
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
        self.text_editor = tk.Text(self.window, wrap=tk.WORD, font=self.input_text_font, height=30, width=80, undo=True, maxundo=-1, cursor='arrow', background=INITIAL_BACKGROUND_COLOR)
        self.text_editor.grid(row=1, column=1, padx=10, pady=5, columnspan=2, sticky='nsew')
        self.text_editor.bind('<KeyPress>', self.on_scroll)
        self.text_editor.bind('<KeyRelease>', self.on_type_text)
        self.text_editor.bind('<MouseWheel>', self.on_scroll)
        self.text_editor.bind('<B1-Motion>', self.on_scroll)
        self.text_editor.bind('<Control-s>', self.save_grammar_action)
        logging.info('Text editor widget initialized')
    
    def init_canvas_circle(self):
        """
        Initialize the canvas circle widget.
        """
        self.circle_canvas = tk.Canvas(self.text_editor, width=10, height=10)
        self.circle = self.circle_canvas.create_oval(2, 2, 10, 10, outline=BLACK_COLOR, fill=OK_COLOR)
        self.circle_canvas.place(relx=1, rely=1, anchor=tk.SE)
        logging.info('Canvas circle widget initialized for text editor')

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

    def open_project_action(self):
        """
        Opens a folder and checks if it is a valid Spring Boot application.
        If it is, sets the working state otherwise sets the initial state.
        """
        try:
            logging.info('Opening project folder')
            self.project_path = filedialog.askdirectory(title='Select Spring Boot project folder')
            if not self.project_path:
                logging.warning('No project path selected')
                return

            self.project_name = utils.get_base_name(self.project_path)
            logging.info(f'Checking if folder "{self.project_name}" is a valid Spring Boot application')
            build_tool, is_spring_boot = utils.is_spring_boot_application(self.project_path)
            if not is_spring_boot:
                self.console_output.config(text=f'{cfg.CONSOLE_LOG_LEVEL_TAGS["WARN"]} The selected folder "{self.project_name}" is NOT a valid Spring Boot application!', fg=WARNING_COLOR)
                logging.warning(f'Folder "{self.project_name}" is NOT a valid Spring Boot application')
                self.initial_state()
                return

            self.working_state()
            self.create_jsdmbrs_directory()
            content = self.get_grammar_file_content()
            self.text_editor.insert(tk.INSERT, content)
            self.update_line_numbers()
            self.console_output.config(text=f'{cfg.CONSOLE_LOG_LEVEL_TAGS["INFO"]} The selected folder "{self.project_name}" is a valid {build_tool} Spring Boot application.', fg=INFORMATION_COLOR)
            logging.info(f'Folder "{self.project_name}" is a valid Spring Boot application')
        except Exception as e:
            error_message = f'Failed to open project: {str(e)}'
            logging.error(error_message)
            self.console_output.config(text=f'{cfg.CONSOLE_LOG_LEVEL_TAGS["ERROR"]} {utils.add_punctuation(error_message)}', fg=ERROR_COLOR)

    def save_grammar_action(self, event=None):
        """
        Save the grammar file using the current file name if set; otherwise, prompt for a new file name using SaveWindowGUI.
        """
        try:
            # If the file name is already set, save it
            if self.grammar_file_name is not None:
                logging.info(f'Saving to "{self.grammar_file_name}" grammar file')
                self.save_file_name(event)
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
            self.update_line_numbers()
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

    def run(self):
        """
        Method for running the main window.
        """
        logging.info('Running main window loop')
        self.window.mainloop()

    def on_type_text(self, event=None):
        """
        Update the line numbers and canvas color when the user types text in the text editor.
        """
        if event.keysym not in cfg.KEYSYMS_TO_IGNORE:
            self.update_line_numbers(event)
            self.compare_grammar_content()

    def on_scroll(self, event=None):
        """
        Handle the scroll event and schedule an update for the line numbers.
        """
        logging.debug('Scroll event detected. Scheduling line numbers update')
        self.window.after(1, self.update_line_numbers)

    def on_window_close(self):
        """
        Method for handling the main window close event.
        """
        logging.info('Handling main window close event')
        self.window.destroy()
        self.window.quit()

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
        content = self.text_editor.get('1.0', tk.END)
        total_lines = content.count('\n')
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
    
    def save_file_name(self, event):
        """
        Save the content of the text editor to a file with the specified grammar file name.
        """
        text_content = self.get_text_editor_content()
        file_path = f'{self.project_path}/{cfg.JSD_MBRS_GENERATOR_FOLDER}/{self.grammar_file_name}'
        utils.write_to_file(file_path, text_content)
        self.circle_canvas.itemconfig(self.circle, fill=OK_COLOR)
        self.grammar_file_content = text_content
        if not event:
            messagebox.showinfo('File Name', f'The grammar "{self.grammar_file_name}" has been saved successfully!')
        logging.info(f'Saved grammar file content to "{self.grammar_file_name}"')

    def get_grammar_file_content(self):
        """
        Searches for grammar file in the specified folder and return its content.
        If no grammar files are found, a default content is returned. If multiple grammar files are found, the user is prompted to select one.
        """
        folder_path = utils.get_path(self.project_path, cfg.JSD_MBRS_GENERATOR_FOLDER)
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

    def create_jsdmbrs_directory(self):
        """
        Create the JSD-MBRS directory if it does not exist.
        """
        utils.create_folder(self.project_path, cfg.JSD_MBRS_GENERATOR_FOLDER)

    def get_text_editor_content(self):
        """
        Get the content of the text editor, excluding the last character (newline).
        """
        logging.debug('Retrieving text editor content')
        end_minus_one = self.text_editor.index(f'{tk.END}-1c')
        return self.text_editor.get('1.0', end_minus_one)

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
        config_style(self.save_window, self.save_window_font)
        self.save_window.focus_set()
        self.save_window.grab_set()
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
        logging.info('Entry widget initialized')

    def init_save_button(self):
        """
        Initialize the save button widget.
        """
        self.submit_button = ttk.Button(self.save_window, text='Save grammar', command=self.save_file_name, compound=tk.TOP, style='Button.TButton')
        self.submit_button.pack(pady=10)
        logging.info('Button widget initialized')

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
        file_name = f'{self.save_entry.get().strip()}{cfg.JSD_MBRS_GENERATOR_EXTENSION}'
        if file_name:
            project_path = self.parent.get_project_path()
            text_content = self.parent.get_text_editor_content()
            file_path = f'{project_path}/{cfg.JSD_MBRS_GENERATOR_FOLDER}/{file_name}'
            utils.write_to_file(file_path, text_content)
            self.parent.set_grammar_file_name(file_name)
            self.parent.circle_canvas.itemconfig(self.parent.circle, fill=OK_COLOR)
            self.parent.grammar_file_content = text_content
            logging.info(f'Saved "{file_name}" file to "{file_path}"')
            messagebox.showinfo('File Name', f'The grammar "{file_name}" has been saved successfully!')
            self.on_save_window_close(self.save_window)
        else:
            logging.warning('Input Error: No file name entered')
            messagebox.showwarning('Input Error', 'Please enter a grammar file name.')
