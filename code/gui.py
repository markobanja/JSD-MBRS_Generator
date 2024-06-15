import utils
import logging
import config as cfg
import tkinter as tk
import textx_grammar as tg
from tkinter import ttk
from ttkthemes import ThemedStyle

class GUI:
    """
    Class for creating the GUI.
    """
    def __init__(self):
        """
        Constructor for the GUI class.
        """
        logging.info('Creating GUI instance')
        self.init_window()
        self.entity_model = tg.test_run()

    def init_window(self):
        """
        Initialize the main window.
        """
        logging.info('Initializing main window')
        self.window = tk.Tk()
        self.window.title(cfg.TITLE)
        self.window.resizable(False, False)
        self.window.protocol('WM_DELETE_WINDOW', self.on_window_close)
        self.font_name = cfg.FONT
        self.input_text_font = utils.set_font(self.font_name, 11, True)
        self.position_window(cfg.WIDTH, cfg.HEIGHT)
        self.config_style()
        self.init_window_components()
        self.update_line_numbers()

    def position_window(self, width, height):
        """
        Method for positioning the window.
        """
        logging.info('Positioning window')
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x_position = (screen_width - width) // 2
        y_position = (screen_height - height) // 2
        self.window.geometry(f'{width}x{height}+{x_position}+{y_position}')

    def config_style(self):
        """
        Configures the style of the GUI window.
        """
        logging.info('Configuring GUI style')
        style = ThemedStyle(self.window)
        style.set_theme(cfg.THEME_STYLE)
        style.configure('Toolbar.TButton', font=self.input_text_font)

    def init_window_components(self):
        """
        Initializes the window components of the GUI.
        """
        logging.info('Initializing window components')
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
        self.generate_button = ttk.Button(toolbar, text='Generate', command=self.generate_action, compound=tk.TOP, style='Toolbar.TButton', state=tk.NORMAL)
        self.generate_button.grid(row=0, column=0, padx=5)
        toolbar.columnconfigure(1, weight=1)
        toolbar.grid(row=0, column=0, columnspan=6, sticky='ew', pady=5)
        logging.info('Toolbar initialized')

    def init_line_number_text(self):
        """
        Initialize line number text widget.
        """
        self.line_number_text = tk.Text(self.window, font=self.input_text_font, width=3, padx=5, wrap=tk.NONE, state=tk.DISABLED, cursor='arrow', background=utils.convert_rgb_to_hex(cfg.COLORS['background']))
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
        self.text_editor = tk.Text(self.window, wrap=tk.WORD, font=self.input_text_font, height=30, width=80, undo=True, maxundo=-1, state=tk.NORMAL, background=utils.convert_rgb_to_hex(cfg.COLORS['background']))
        self.text_editor.grid(row=1, column=1, padx=10, pady=5, columnspan=2, sticky='nsew')
        self.text_editor.bind('<KeyRelease>', self.type_text)
        logging.info('Text editor widget initialized')
    
    def init_console_frame(self):
        """
        Initialize the console frame and its label component.
        """
        console_frame = ttk.Frame(self.window, borderwidth=2, relief='groove')
        console_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky='nsew')
        self.console_output = tk.Label(console_frame, text=cfg.HELP_BUTTON_TEXT, font=self.input_text_font, wraplength=650, fg=utils.convert_rgb_to_hex(cfg.COLORS['information']))
        self.console_output.pack(padx=10, pady=10, ipady=50)
        console_frame.grid_rowconfigure(0, weight=1)
        console_frame.grid_columnconfigure(0, weight=1)
        logging.info('Console frame initialized')

    def set_window_weights(self):
        """
        Set the column and row weights for the window.
        """
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)
        self.window.rowconfigure(2, weight=1)
        logging.info('Window weights set')

    def generate_action(self):
        """
        Get the names of all entities in the entity model and insert them into the text editor.
        """
        logging.info('Getting entity names')
        entities = ', '.join([f'"{entity.name}"' for entity in self.entity_model.entities])
        self.text_editor.delete('1.0', tk.END)
        self.text_editor.insert(tk.INSERT, entities)
        logging.info('Entity names retrieved and inserted into the text editor')

    def update_line_numbers(self, event=None):
        """
        Updates the line numbers in the line number text widget based on the content of the text editor.
        """
        content = self.text_editor.get('1.0', tk.END)
        total_lines = content.count('\n')
        self.line_number_text.config(state=tk.NORMAL)
        self.line_number_text.delete('1.0', tk.END)
        line_numbers = ''.join(f'{i}\n' for i in range(1, total_lines + 1))
        self.line_number_text.insert(tk.END, line_numbers, 'right_align')
        self.line_number_text.config(state=tk.DISABLED)

    def type_text(self, event=None):
        """
        Handler function for the '<KeyRelease>' event.
        """
        self.update_line_numbers(event)

    def run(self):
        """
        Method for running the GUI.
        """
        logging.info('Running GUI main loop')
        self.window.mainloop()

    def on_window_close(self):
        """
        Method for handling the window close event.
        """
        logging.info('Handling window close event')
        self.window.destroy()
        self.window.quit()
