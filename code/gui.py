import logging
import tkinter as tk


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

    def init_window(self):
        """
        Initialize the main window.
        """
        self.window = tk.Tk()
        self.window.title('JSD-MBRS Generator')
        self.window.resizable(False, False)
        self.window.protocol('WM_DELETE_WINDOW', self.on_window_close)
        self.window_position(self.window, 800, 600)
        self.font_name = 'Courier New'

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

    def window_position(self, window, width, height):
        """
        Method for positioning the window.
        """
        logging.info('Positioning window')
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x_position = (screen_width - width) // 2
        y_position = (screen_height - height) // 2
        window.geometry(f'{width}x{height}+{x_position}+{y_position}')


# NOTE: FOR TESTING ONLY (REMOVE LATER)
if __name__ == '__main__':
    GUI().run()