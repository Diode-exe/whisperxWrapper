import tkinter as tk

class AdvancedSettingsWindow:
    def __init__(self, parent, configuration):
        self.parent = parent
        self.configuration = configuration
        self.window = None
        self.batch_size_label = None
        self.batch_size_entry = None

    def show_window(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title("Advanced Settings")
        self.window.geometry("400x300")

        self.batch_size_label = tk.Label(self.window, text="Batch Size:")
        self.batch_size_label.pack(pady=5)
        self.batch_size_entry = tk.Entry(self.window)
        self.batch_size_entry.insert(0, str(self.configuration.batch_size))
        self.batch_size_entry.pack(pady=5)
