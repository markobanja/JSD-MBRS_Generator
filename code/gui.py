import tkinter as tk

class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('JSD-MBRS Generator')
        self.window.resizable(False, False)
        self.window.protocol('WM_DELETE_WINDOW', self.on_window_close)
        self.font_name = 'Courier New'
        self.window_position(self.window, 800, 600)

    def run(self):
        self.window.mainloop()

    def on_window_close(self):
        self.window.destroy()
        self.window.quit()

    def window_position(self, window, width, height):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x_position = (screen_width - width) // 2
        y_position = (screen_height - height) // 2
        window.geometry(f'{width}x{height}+{x_position}+{y_position}')
